import base64
from datetime import datetime

from cryptography import exceptions
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from oslo_config import cfg
from oslo_log import log as logging

from hamal.utils import options
from hamal.i18n import _LE
import hamal.conf


CONF = hamal.conf.CONF

LOG = logging.getLogger(__name__)


class VMwareRSALicense(object):
    """Used for create a license with signature"""

    def __init__(self):
        self.private_key_file = CONF.vmware_rsa_license.private_key_file
        self.public_key_file = CONF.vmware_rsa_license.public_key_file
        self._private_key = None
        self._public_key = None

    def loading_private_key(self, serialize=False, password=None):
        with open(self.private_key_file, 'rb') as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=password,
                backend=default_backend()
            )
        
        if not serialize:
            self._private_key = private_key
        else:
            pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )

            self._private_key = pem
    
    def loading_public_key(self, serialize=False):
        with open(self.public_key_file, 'rb') as key_file:
            public_key = serialization.load_der_public_key(
                key_file.read(),
                backend=default_backend()
            )
        
        if not serialize:
            self._public_key = public_key
        else:
            pem = public_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            self._public_key = pem
    
    def encrypt_message(self, message):
        if self._public_key is None:
            self.loading_public_key()
        ciphertext = self._public_key.encrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return ciphertext
    
    def decrypt_message(self, message):
        if self._private_key is None:
            self.loading_private_key()
        plaintext = self._private_key.decrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return plaintext

    def sign_a_license(self, server_nums=0, expired_at=datetime.utcnow()):
        msg = 'server_nums:{0}, expired_at:{1}'.format(server_nums, expired_at)

        if self._private_key is None:
            self.loading_private_key()
        signature = self._private_key.sign(
            msg,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        new_license = {'signature': signature, 'message': msg}
        return base64.b64encode(str(new_license))
    
    def verify_license_signature(self, license):
        license = eval(base64.b64decode(license))
        signature = license.get('signature')
        message = license.get('message')

        if self._public_key is None:
            self.loading_public_key()
        try:
            if hasattr(self._public_key, 'verify'):
                self._public_key.verify(
                    signature,
                    message,
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                    hashes.SHA256()
                )
            
            # if the version of cryptography == 1.3.x
            # we should use verifier function to verify sign
            elif hasattr(self._public_key, 'verify'):
                verifier = self._public_key. verifier(
                    signature,
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                    hashes.SHA256()
                )
                verifier.update(message)
                verifier.verify()
            return True
        except exceptions.InvalidSignature:
            LOG.exception(_LE("License signature invalid"))
            return False
