'''
Created on Mar 6, 2014

@package: ally core
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the option decoding.
'''

from ally.api.operator.type import TypeProperty, TypeOption
from ally.api.type import Type, Input
from ally.container.ioc import injected
from ally.design.processor.attribute import requires, defines
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessor
from ally.api.option import Slice
from ally.support.api.util_service import isCompatible

# --------------------------------------------------------------------

class Invoker(Context):
    '''
    The invoker context.
    '''
    # ---------------------------------------------------------------- Defined
    namedArguments = defines(set, doc='''
    @rtype: set(string)
    The input names that are required to be provided as key arguments.
    ''')

class Decoding(Context):
    '''
    The decoding context.
    '''
    # ---------------------------------------------------------------- Defined
    property = defines(TypeProperty, doc='''
    @rtype: TypeProperty
    The option property that represents the decoding.
    ''')
    # ---------------------------------------------------------------- Required
    input = requires(Input)
    type = requires(Type)    

class Parameter(Context):
    '''
    The parameter context.
    '''
    # ---------------------------------------------------------------- Required
    path = requires(list)
     
# --------------------------------------------------------------------

@injected
class OptionDecode(HandlerProcessor):
    '''
    Implementation for a handler that provides the primitive properties values encoding.
    '''
    
    def process(self, chain, decoding:Decoding, parameter:Parameter, invoker:Invoker, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Populate the option type decoding.
        '''
        assert isinstance(decoding, Decoding), 'Invalid decoding %s' % decoding
        assert isinstance(invoker, Invoker), 'Invalid invoker %s' % invoker
        assert isinstance(parameter, Parameter), 'Invalid parameter %s' % parameter
        
        if isinstance(decoding.type, TypeProperty) and isinstance(decoding.type.parent, TypeOption):
            assert isinstance(decoding.type, TypeProperty)
            assert isinstance(decoding.input, Input), 'Invalid input %s' % input

            if isCompatible(Slice.limit, decoding.type):
                parameter.path.pop()
                parameter.path.append('maxResults')

            decoding.property = decoding.type
            decoding.type = decoding.type.type
            
            if invoker.namedArguments is None: invoker.namedArguments = set()
            invoker.namedArguments.add(decoding.input.name)