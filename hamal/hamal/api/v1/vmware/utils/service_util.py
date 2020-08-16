# Copyright 2020 Hamal, Inc.

"""
Utility function for the vSphere API

See com.vmware.apputils.vim25.ServiceUtil in the java API.
"""

from pyVmomi import vim, vmodl


def  build_full_traversal():
    """
    Builds a traversal spec that will recurse through all objects .. or at 
    least I think it does. additions welcome.

    See com.vmware.apputils.vim25.ServiceUtil.buildFullTraversal in the java
    API. Extended by Sebastian Tello's examples from pyshpere to reach networks
    and datastores.
    """

    TraversalSpec = vmodl.query.PropertyCollector.TraversalSpec
    SelectionSpec = vmodl.query.PropertyCollector.SelectionSpec

    # Recurse through all resourcepools
    rpToRp = TraversalSpec(name='rpToRp', type=vim.ResourcePool,
                           path="resourcePool", skip=False)
    
    rpToRp.selectSet.extend(
        (
            SelectionSpec(name="rpToRp"),
            SelectionSpec(name="rpToVm"),
        )
    )

    rpToVm = TraversalSpec(name="rpToVm", type=vim.ResourcePool, 
                           path="vm", skip=False)
    
    # Traversal through resourcepool branch
    crToRp = TraversalSpec(name="crToRp", type=vim.ComputeResource,
                           path="resourcePool", skip=False)
    crToRp.selectSet.extend(
        (
            SelectionSpec(name='rpToRp'),
            SelectionSpec(name='rpToVm'),
        )
    )

    # Traversal through host branch
    crToH = TraversalSpec(name="crToH", type=vim.ComputeResource,
                          path='host', skip=False)

    # Traversal through hostFolder branch
    dcToHf = TraversalSpec(name='dcToHf', type=vim.Datacenter,
                           path='hostFolder', skip=False)
    dcToHf.selectSet.extend(
        (
            SelectionSpec(name='visitFolders'),
        )
    )

    # Traversal through vmFolder branch
    dcToVmf = TraversalSpec(name='dcToVmf', type=vim.Datacenter, 
                            path='vmFolder', skip=False)
    dcToVmf.selectSet.extend(
        (
            SelectionSpec(name='visitFolders'),
        )
    )

    # Traversal through network folder branch 
    dcToNet = TraversalSpec(name='dcToNet', type=vim.Datacenter,
                            path='networkFolder', skip=False)
    dcToNet.selectSet.extend(
        (
            SelectionSpec(name='visitFolders'),
        )
    )

    # Traversal through datastore branch
    dcToDs = TraversalSpec(name='dcToDs', type=vim.Datacenter,
                           path='datastore', skip=False)
    dcToDs.selectSet.extend(
        (
            SelectionSpec(name='visitFolders'),
        )
    )

    # Recurse through all hosts
    hToVm = TraversalSpec(name='hToVm', type=vim.HostSystem,
                          path='vm', skip=False)
    hToVm.selectSet.extend(
        (
            SelectionSpec(name='visitFolders'),
        )
    )

    # Recurse through the folders
    visitFolders = TraversalSpec(name='visitFolders', type=vim.Folder,
                                 path='childEntity', skip=False)
    visitFolders.selectSet.extend(
        (
            SelectionSpec(name='visitFolders'),
            SelectionSpec(name='dcToHf'),
            SelectionSpec(name='dcToVmf'),
            SelectionSpec(name='dcToNet'),
            SelectionSpec(name='crToH'),
            SelectionSpec(name='crToRp'),
            SelectionSpec(name='dcToDs'),
            SelectionSpec(name='hToVm'),
            SelectionSpec(name='rpToVm'),
        )
    )

    fullTraversal = SelectionSpec.Array(
        (visitFolders, dcToHf, dcToVmf, dcToNet, crToH, crToRp, dcToDs, rpToRp, hToVm, rpToVm)
    )

    return fullTraversal
