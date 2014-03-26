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
    assemblyResources, statusCodeToStatus, statusCodeToText
from __setup__.ally_http.processor import contentTypeResponseEncode
from ally.container import ioc
from ally.core.spec.codes import INPUT_ERROR, DELETE_ERROR, INPUT_ID_ERROR
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

@ioc.before(statusCodeToText)
def updateStatusCodeToText():
    statusCodeToText()[INPUT_ERROR.code] = lambda method, hasContent: None if hasContent else 'Not Found'
    # Changing to HTTP code 402 Not Found
    
@ioc.before(statusCodeToStatus)
def updateStatusCodeToStatus():
    statusCodeToStatus()[INPUT_ID_ERROR.code] = 404
    statusCodeToStatus()[INPUT_ERROR.code] = lambda method, hasContent: 400 if hasContent else 404
    # Changing to HTTP code 402 Not Found
    statusCodeToStatus()[DELETE_ERROR.code] = 204
    # Changing to HTTP code 204 regardless of the delete is success or not.

# TODO: remove this when the gateway is UP.
@ioc.after(updateHeadersCors)
def updateHeadersCorsForAuthorization():
    headersCorsAllow().add('Authorization') 

@ioc.after(updateAssemblyResources)
def updateAssemblyResourcesPatch():
    assemblyResources().add(methodPatch(), after=methodAllow())
