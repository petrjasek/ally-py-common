'''
Created on Mar 14, 2014

@package: patch praha
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the processor setup patches.
'''

from ally.container import ioc, wire

from acl.core_patch.impl.processor.assembler.index_access import IndexAccessPatchHandler

from ..gateway_acl.patch_ally_core import indexAccess


# --------------------------------------------------------------------
@wire.wire(IndexAccessPatchHandler)
@ioc.replace(indexAccess)
def indexAccessPatch(): return IndexAccessPatchHandler()