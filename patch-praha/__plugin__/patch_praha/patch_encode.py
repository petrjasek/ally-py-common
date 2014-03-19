'''
Created on Feb 26, 2014

@package: patch praha
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the encode setup patches.
'''

from __setup__.ally_core.encode import assemblyEncode, modelEncode, \
    assemblyEncodeExport, collectionEncode, updateAssemblyExtensionAttribute, \
    assemblyExtensionAttribute, propertyEncode, extensionAttributeEncode
from __setup__.ally_core_http.encode import updateAssemblyEncodeWithPath, \
    updateAssemblyEncodeExportForPath
from ally.container import ioc
from ally.design.processor.handler import Handler

from ally.core.http_patch.impl.processor.encoder.ref_path import RefPathAttributeEncode, \
    refPathExport
from ally.core.http_patch.impl.processor.encoder.ref_update import RefUpdateEncode
from ally.core.http_patch.impl.processor.encoder.self_path import SelfPathAttributeEncode, \
    selfPathExport
from ally.core.http_patch.impl.processor.encoder.slice_rename import SliceRenameAttributeEncode


# --------------------------------------------------------------------
@ioc.entity
def selfPathAttributeEncode() -> Handler: return SelfPathAttributeEncode()

@ioc.entity
def refPathAttributeEncode() -> Handler: return RefPathAttributeEncode()

@ioc.entity
def refUpdateEncode() -> Handler: return RefUpdateEncode()

@ioc.entity
def sliceRenameAttributeEncode() -> Handler: return SliceRenameAttributeEncode()

# --------------------------------------------------------------------
    
@ioc.after(updateAssemblyExtensionAttribute)
def updateAssemblyExtensionAttributePatch():
    assemblyExtensionAttribute().add(sliceRenameAttributeEncode(), before=propertyEncode())

@ioc.after(updateAssemblyEncodeWithPath)
def updateAssemblyEncodeWithPatch():
    assemblyEncode().add(selfPathAttributeEncode(), before=modelEncode())
    assemblyEncode().add(refPathAttributeEncode(), before=collectionEncode())
    assemblyEncode().add(refUpdateEncode(), before=extensionAttributeEncode())

@ioc.after(updateAssemblyEncodeExportForPath)
def updateAssemblyEncodeExportForSelPath():
    assemblyEncodeExport().add(selfPathExport, refPathExport)
