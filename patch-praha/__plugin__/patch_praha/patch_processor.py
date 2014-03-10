'''
Created on Mar 6, 2014

@package: patch praha
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the processor setup patches.
'''

import logging

from __setup__.ally_core.processor import methodAllow
from __setup__.ally_core_http.processor import updateHeadersCors, \
    headersCorsAllow, read_from_params, updateAssemblyResources, \
    assemblyResources
from __setup__.ally_http.processor import contentTypeResponseEncode
from ally.container import ioc
from ally.design.processor.handler import Handler

from ally.core.http_patch.impl.processor.headers.content_type import ContentTypeResponseEncodeHandler
from ally.core.http_patch.impl.processor.method_patch import MethodPatchHandler


# --------------------------------------------------------------------
log = logging.getLogger(__name__)

# --------------------------------------------------------------------

@ioc.replace(read_from_params)
def patch_read_from_params(): return False

try: from __setup__.ally_assemblage.processor import read_from_params as assemblage_read_from_params
except: log.info('No assemblage present, thus no patching will occur for it.')
else:
    @ioc.replace(assemblage_read_from_params)
    def patch_assemblage_read_from_params(): return False
    
# --------------------------------------------------------------------

@ioc.replace(contentTypeResponseEncode)
def contentTypeResponseEncodeNoCharSet() -> Handler: return ContentTypeResponseEncodeHandler()

@ioc.entity
def methodPatch() -> Handler: return MethodPatchHandler()

# --------------------------------------------------------------------

# TODO: remove this when the gateway is UP.
@ioc.after(updateHeadersCors)
def updateHeadersCorsForAuthorization():
    headersCorsAllow().add('Authorization') 

@ioc.after(updateAssemblyResources)
def updateAssemblyResourcesPatch():
    assemblyResources().add(methodPatch(), after=methodAllow())
