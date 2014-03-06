'''
Created on Mar 6, 2014

@package: patch praha
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the processor setup patches.
'''

from __setup__.ally_core_http.processor import updateHeadersCors, \
    headersCorsAllow, updateAssemblyResources, assemblyResources
from __setup__.ally_http.processor import contentTypeResponseEncode
from ally.container import ioc
from ally.design.processor.handler import Handler

from ally.core.http_patch.impl.processor.headers.content_type import ContentTypeResponseEncodeHandler


# --------------------------------------------------------------------
@ioc.entity
def contentTypeResponseEncodeNoCharSet() -> Handler: return ContentTypeResponseEncodeHandler()

# --------------------------------------------------------------------

@ioc.after(updateAssemblyResources)
def updateAssemblyResourcesForPatch():
    assemblyResources().replace(contentTypeResponseEncode(), contentTypeResponseEncodeNoCharSet())
                            
@ioc.after(updateHeadersCors)
def updateHeadersCorsForAuthorization():
    headersCorsAllow().add('Authorization')

