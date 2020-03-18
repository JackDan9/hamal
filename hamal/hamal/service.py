# Copyright

"""Generic Node base class for all workers that run on hosts."""

import os
import sys

from oslo_concurrency import processutils
from oslo_log import log as logging
import oslo_messaging as messaging
from oslo_service import service
from oslo_utils import importutils

import hamal.conf
from hamal import baserpc
from hamal import exception
from hamal.i18n import _
from hamal import rpc
from hamal.wsgi import common as wsgi_common
from hamal.wsgi import server as wsgi


LOG = logging.getLogger(__name__)

CONF = hamal.conf.CONF
CONF.import_opt('host', 'hamal.engine.manager')

SERVICE_MANAGERS = {
    'hamal-engine': 'hamal.engine.manager.EngineManager',
}


class Service(service.Service):
    """Service object for binaries running on hosts.

    A service takes a manager and enables rpc by listening to queues based
    on topic. It also periodically runs tasks on the manager and reports
    it state to the database services table.
    """

    def __init__(self, host, binary, topic, manager, *args, **kwargs):
        super(Service, self).__init__()
        self.host = host
        self.binary = binary
        self.topic = topic
        self.manager_class_name = manager
        manager_class = importutils.import_class(self.manager_class_name)
        self.manager = manager_class(host=self.host, *args, **kwargs)
        self.saved_args, self.saved_kwargs = args, kwargs
        self.rpcserver = None

    def start(self):
        if CONF.use_rpc:
            target = messaging.Target(topic=self.topic, server=self.host)

            endpoints = [
                self.manager,
                baserpc.BaseRPCAPI(self.manager.service_name),
            ]

            endpoints.extend(self.manager.additional_endpoints)

            self.rpcserver = rpc.get_server(target, endpoints)
            self.rpcserver.start()

        self.tg.add_dynamic_timer(self.periodic_tasks,
                                  initial_delay=None,
                                  periodic_interval_max=30)
        LOG.info("Started service %s on host %s.", self.binary, self.host)

    def __getattr__(self, key):
        manager = self.__dict__.get('manager', None)
        return getattr(manager, key)

    @classmethod
    def create(cls, host=None, binary=None, topic=None, manager=None):
        """Instantiates class and passes back application object.

        :param host: defaults to CONF.host
        :param binary: defaults to basename of executable
        :param manager: defaults to CONF.<topic>_manager

        """
        if not host:
            host = CONF.host
        if not binary:
            binary = os.path.basename(sys.argv[0])
        if not topic:
            topic = binary.rpartition('hamal-')[2]
        if not manager:
            manager = SERVICE_MANAGERS.get(binary)

        service_obj = cls(host, binary, topic, manager)

        return service_obj

    def stop(self):
        if self.rpcserver:
            try:
                self.rpcserver.stop()
                self.rpcserver.wait()
            except Exception:
                pass

        try:
            self.manager.cleanup_host()
        except Exception:
            LOG.exception('Service error occurred during cleanup_host')
            pass

        super(Service, self).stop()

    def periodic_tasks(self, raise_on_error=False):
        """Tasks to be run at a periodic interval."""
        # TODO(gcb) Need add real context whe we have context support
        return self.manager.periodic_tasks({'context': 'name'},
                                           raise_on_error=raise_on_error)


class WSGIService(service.ServiceBase):
    """Provides ability to launch API from a 'paste' configuration."""

    def __init__(self, name, loader=None, use_ssl=False):
        """Initialize, but do not start the WSGI server.

        :param name: The name of the WSGI server given to the loader.
        :param loader: Loads the WSGI application using the given name.
        :returns: None

        """
        self.name = name
        self.manager = self._get_manager()
        self.loader = loader or wsgi_common.Loader()
        self.app = self.loader.load_app(name)
        self.host = getattr(CONF, '%s_listen' % name, "0.0.0.0")
        self.port = getattr(CONF, '%s_listen_port' % name, 9278)
        self.workers = (getattr(CONF, '%s_workers' % name, None) or
                        processutils.get_worker_count())
        if self.workers and self.workers < 1:
            worker_name = '%s_workers' % name
            msg = (_("{0} value of {1} is invalid, must be greater than 0.") %
                   (worker_name, self.workers))
            raise exception.InvalidInput(msg)

        self.use_ssl = use_ssl or CONF.use_ssl
        self.server = wsgi.Server(name,
                                  self.app,
                                  host=self.host,
                                  port=self.port,
                                  use_ssl=self.use_ssl)

    def _get_manager(self):
        """Initialize a Manager object appropriate for this service.

        Use the service name to look up a Manager subclass from the
        configuration and initialize an instance. If no class name
        is configured, just return None.

        :returns: a Manager instance, or None.

        """
        fl = '%s_manager' % self.name
        if fl not in CONF:
            return None

        manager_class_name = CONF.get(fl, None)
        if not manager_class_name:
            return None

        manager_class = importutils.import_class(manager_class_name)
        return manager_class()

    def start(self):
        """Start serving this service using loaded configuration.

        Also, retrieve updated port number in case '0' was passed in, which
        indicates a random port should be used.

        :returns: None

        """
        if self.manager:
            self.manager.init_host()
        self.server.start()
        self.port = self.server.port

    def stop(self):
        """Stop serving this API.

        :returns: None

        """
        self.server.stop()

    def wait(self):
        """Wait for the service to stop serving this API.

        :returns: None

        """
        self.server.wait()

    def reset(self):
        """ResZet server greenpool size to default.

        :returns: None

        """
        self.server.reset()


def process_launcher():
    return service.ProcessLauncher(CONF)


_launcher = None


def serve(server, workers=None):
    global _launcher
    if _launcher:
        raise RuntimeError(_('serve() can only be called once'))

    _launcher = service.launch(CONF, server, workers=workers)


def wait():
    _launcher.wait()


def get_launcher():
    return process_launcher()
