'''
Created on Mar 7, 2014

@package: patch praha
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the slice limit rename.
'''

import logging

from ally.api.extension import IterPart
from ally.api.type import Type
from ally.container.ioc import injected
from ally.design.processor.attribute import requires, defines
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessor
from ally.support.api.util_service import isCompatible


# --------------------------------------------------------------------
log = logging.getLogger(__name__)

# --------------------------------------------------------------------

class Create(Context):
    '''
    The create encoder context.
    '''
    # ---------------------------------------------------------------- Defined
    name = defines(str, doc='''
    @rtype: string
    The name of create.
    ''')
    # ---------------------------------------------------------------- Required
    objType = requires(Type)

# --------------------------------------------------------------------

@injected
class SliceRenameAttributeEncode(HandlerProcessor):
    '''
    Implementation for a handler that provides the slice limit rename.
    '''
    
    def __init__(self):
        super().__init__()
        
    def process(self, chain, create:Create, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Provides the slice limit rename.
        '''
        assert isinstance(create, Create), 'Invalid create %s' % create
        
        if not isCompatible(IterPart.limit, create.objType): return
        create.name = 'maxResults'
