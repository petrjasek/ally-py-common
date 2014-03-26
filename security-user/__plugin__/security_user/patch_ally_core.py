'''
Created on Feb 26, 2013

@package: superdesk security
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the ally core setup patch.
'''

from ally.container import support, ioc
import logging

from security.user.core.impl.processor import assembler


# --------------------------------------------------------------------
log = logging.getLogger(__name__)

# --------------------------------------------------------------------

try:
    from __setup__ import ally_core  # @UnusedImport
except ImportError: log.info('No ally core component available, thus no need to register user ACL assemblers to it')
else:
    from ..gateway_acl.patch_ally_core import indexFilter, assemblyIndex, updateAssemblyIndex

    # The assembler processors
    filterUserInject = support.notCreated  # Just to avoid errors
    support.createEntitySetup(assembler)
    
    # ----------------------------------------------------------------
    
    @ioc.after(updateAssemblyIndex)
    def updateAssemblyIndexForUserFilterInject():
        assemblyIndex().add(filterUserInject(), before=indexFilter())
