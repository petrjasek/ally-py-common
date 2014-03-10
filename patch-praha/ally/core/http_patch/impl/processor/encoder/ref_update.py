'''
Created on Mar 10, 2014

@package: patch praha
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the update reference.
'''

import logging

from ally.api.config import UPDATE
from ally.api.operator.type import TypeModel
from ally.api.type import Type, TypeNone
from ally.container.ioc import injected
from ally.core.impl.processor.encoder.base import ExportingSupport
from ally.core.spec.resources import Converter
from ally.core.spec.transform import ITransfrom
from ally.design.processor.attribute import requires, defines
from ally.design.processor.context import Context
from ally.design.processor.execution import Chain
from ally.design.processor.handler import HandlerProcessor


# --------------------------------------------------------------------
log = logging.getLogger(__name__)

# --------------------------------------------------------------------

class Invoker(Context):
    '''
    The invoker context.
    '''
    # ---------------------------------------------------------------- Defined
    hideProperties = defines(bool, doc='''
    @rtype: boolean
    Indicates that the properties of model rendering should be hidden (not rendering).
    ''')
    # ---------------------------------------------------------------- Required
    invokerGet = requires(Context)
    target = requires(TypeModel)
    method = requires(int)

class Create(Context):
    '''
    The create encoder context.
    '''
    # ---------------------------------------------------------------- Defined
    encoder = defines(ITransfrom)
    # ---------------------------------------------------------------- Required
    objType = requires(Type)

class Support(Context):
    '''
    The support context.
    '''
    # ---------------------------------------------------------------- Defined
    nodesValues = defines(dict, doc='''
    @rtype: dictionary{Context: object}
    The values used in constructing the paths indexed by corresponding node.
    ''')
    # ---------------------------------------------------------------- Required
    converterContent = requires(Converter)
    
# --------------------------------------------------------------------

pathUpdaterSupportEncodeExport = ExportingSupport(Support)
# The path updater support export.

@injected
class RefUpdateEncode(HandlerProcessor):
    '''
    Implementation for a handler that provides the update reference.
    '''
    
    def __init__(self):
        super().__init__()
        
    def process(self, chain, invoker:Invoker, create:Create, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Create the the update reference.
        '''
        assert isinstance(chain, Chain), 'Invalid chain %s' % chain
        assert isinstance(invoker, Invoker), 'Invalid invoker %s' % invoker
        assert isinstance(create, Create), 'Invalid create %s' % create
        
        if invoker.method != UPDATE or invoker.invokerGet is None: return
        if create.objType is TypeNone: return 
        if invoker.target is None or invoker.target.propertyId is None: return
        assert isinstance(invoker.target, TypeModel)
        
        create.objType = invoker.target.propertyId
        invoker.hideProperties = True
        
        chain.onFinalize(self.finalize)
        
    def finalize(self, final, create, invoker, **keyargs):
        ''' Wrap the encoder to simulate the returned property id.'''
        assert isinstance(create, Create), 'Invalid create %s' % create
        if create.encoder:
            create.encoder = EncoderPathUpdater(create.encoder, invoker)

# --------------------------------------------------------------------

class EncoderPathUpdater(ITransfrom):
    '''
    Implementation for a @see: ITransfrom that updates the path before encoding .
    '''
    
    def __init__(self, encoder, invoker):
        '''
        Construct the path updater for property value.
        '''
        assert isinstance(encoder, ITransfrom), 'Invalid property encoder %s' % encoder
        
        self.encoder = encoder
        self.invoker = invoker
        
    def transform(self, value, target, support):
        '''
        @see: ITransfrom.transform
        '''
        assert isinstance(support, Support), 'Invalid support %s' % support
        assert isinstance(support.converterContent, Converter), \
        'Invalid converter %s' % support.converterContent
        if self.invoker.node.parent not in support.nodesValues: return
        # Update the value and simulate the property id return.
        value = support.nodesValues[self.invoker.node.parent]
        value = support.converterContent.asValue(value, self.invoker.target.propertyId)
        self.encoder.transform(value, target, support)

        
