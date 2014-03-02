'''
Created on Feb 27, 2014

@package: patch praha
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the encode setup patches.
'''

from __setup__.ally_core.parsing_rendering import updateBlocksDefinitions, \
    blocksDefinitions
from ally.container import ioc

from ally.core.http_patch.impl.index import BLOCKS_PATCH


# --------------------------------------------------------------------
@ioc.after(updateBlocksDefinitions)
def updateBlocksDefinitionsWithSelf():
    blocksDefinitions().update(BLOCKS_PATCH)
