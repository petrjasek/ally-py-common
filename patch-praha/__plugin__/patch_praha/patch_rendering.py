'''
Created on Feb 27, 2014

@package: patch praha
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the encode setup patches.
'''

from __setup__.ally_core.parsing_rendering import updateBlocksDefinitions, \
    blocksDefinitions, content_types_json, content_types_xml
from ally.container import ioc

from ally.core.http_patch.impl.index import BLOCKS_PATCH


# --------------------------------------------------------------------

@ioc.replace(content_types_json)
def replace_content_types_json() -> dict:
    '''
    The JSON content types, a map that contains as a key the recognized mime type and as a value the normalize mime type,
    if none then the same key mimie type will be used for response
    '''
    return {
            'text/json':'application/json',
            'application/json':None,
            'json':'application/json',
            None:'application/json'
            }

@ioc.replace(content_types_xml)
def replace_content_types_xml() -> dict:
    '''
    The XML content types, a map that contains as a key the recognized mime type and as a value the normalize mime type,
    if none then the same key mimie type will be used for response
    '''
    return {
            'text/xml':'application/xml',
            'text/plain':'application/xml',
            'application/xml':None,
            'xml':'application/xml'
            }

# --------------------------------------------------------------------

@ioc.after(updateBlocksDefinitions)
def updateBlocksDefinitionsWithSelf():
    blocksDefinitions().update(BLOCKS_PATCH)
