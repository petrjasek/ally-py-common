'''
Created on Mar 19, 2014

@package: patch praha
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the resources setup patches.
'''

from __setup__.ally_core.resources import assemblyAssembler
from __setup__.ally_core_http.resources import updateAssemblyAssemblerForHTTPCore, \
    pathGetAccesible
from ally.container import ioc
from ally.core.http.impl.processor.assembler.path_get_accessible import PathGetAccesibleHandler
from ally.design.processor.handler import Handler
from ally.http.spec.server import HTTP_PUT, HTTP_POST


# --------------------------------------------------------------------
@ioc.entity
def pathGetAccesiblePost() -> Handler:
    b = PathGetAccesibleHandler()
    b.method = HTTP_POST
    return b

@ioc.entity
def pathGetAccesiblePut() -> Handler:
    b = PathGetAccesibleHandler()
    b.method = HTTP_PUT
    return b

# --------------------------------------------------------------------

@ioc.after(updateAssemblyAssemblerForHTTPCore)
def updateAssemblyAssemblerForAccessiblePatch():
    assemblyAssembler().add(pathGetAccesiblePost(), pathGetAccesiblePut(), after=pathGetAccesible())
