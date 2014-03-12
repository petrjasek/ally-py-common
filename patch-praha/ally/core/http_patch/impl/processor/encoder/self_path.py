'''
Created on Feb 26, 2014

@package: patch praha
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the self path for a model.
'''

import logging

from ally.container.ioc import injected
from ally.core.impl.processor.encoder.base import ExportingSupport
from ally.core.spec.transform import ISpecifier, ITransfrom
from ally.design.processor.attribute import requires, defines, optional
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessor
from ally.support.util_spec import IDo

from ally.core.http_patch.impl.index import ADJUST_SELF_DISCARD
from urllib.parse import urlencode
from ally.api.operator.type import TypeModel
from ally.api.type import Type


# --------------------------------------------------------------------
log = logging.getLogger(__name__)

# --------------------------------------------------------------------

class Invoker(Context):
    '''
    The invoker context.
    '''
    # ---------------------------------------------------------------- Required
    node = requires(Context)
    doEncodePath = requires(IDo)

class Node(Context):
    '''
    The node context.
    '''
    # ---------------------------------------------------------------- Required
    invokersGet = defines(dict)
    invokersUpdate = requires(dict)
    invokersDelete = requires(dict)

class Create(Context):
    '''
    The create encoder context.
    '''
    # ---------------------------------------------------------------- Defined
    specifiers = defines(list, doc='''
    @rtype: list[ISpecifier]
    The specifiers for attributes with the paths.
    ''')
    # ---------------------------------------------------------------- Optional
    encoder = optional(ITransfrom)
    # ---------------------------------------------------------------- Required
    objType = requires(Type)

class Support(Context):
    '''
    The support context.
    '''
    # ---------------------------------------------------------------- Defined
    parameters = defines(list)  # This is actually required but beacouse of the export bug it is put on defined.
    
# --------------------------------------------------------------------

selfPathExport = ExportingSupport(Support)
# The encoding path support export.

@injected
class SelfPathAttributeEncode(HandlerProcessor):
    '''
    Implementation for a handler that provides the self path for a model.
    '''
    
    nameRef = 'href'
    # The reference attribute name.
    
    def __init__(self):
        assert isinstance(self.nameRef, str), 'Invalid reference name %s' % self.nameRef
        super().__init__(Node=Node)
        
    def process(self, chain, invoker:Invoker, create:Create, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Create the self path.
        '''
        assert isinstance(create, Create), 'Invalid create %s' % create
        assert isinstance(invoker, Invoker), 'Invalid invoker %s' % invoker
        assert isinstance(invoker.node, Node), 'Invalid node %s' % invoker.node
        
        if Create.encoder in create and create.encoder is not None: return 
        # There is already an encoder, nothing to do.
        if not isinstance(create.objType, TypeModel): return
        assert isinstance(create.objType, TypeModel)
        
        if create.objType.propertyId:
            invokerSelf = invoker.node.invokersGet.get(create.objType.propertyId)
            if invokerSelf is None: invokerSelf = invoker.node.invokersDelete.get(create.objType.propertyId)
        else: invokerSelf = None
        if invokerSelf is None: invokerSelf = invoker.node.invokersUpdate.get(create.objType)

        if not invokerSelf: return  # No invoker available
        assert isinstance(invokerSelf, Invoker), 'Invalid invoker %s' % invokerSelf
       
        if create.specifiers is None: create.specifiers = []
        create.specifiers.append(AttributeSelfPath(self.nameRef, invokerSelf))

# --------------------------------------------------------------------

class AttributeSelfPath(ISpecifier):
    '''
    Implementation for a @see: ISpecifier for paths.
    '''
    
    def __init__(self, nameRef, invoker):
        '''
        Construct the paths attributes.
        '''
        assert isinstance(nameRef, str), 'Invalid reference name %s' % nameRef
        assert isinstance(invoker, Invoker), 'Invalid invoker %s' % invoker
        assert isinstance(invoker.doEncodePath, IDo), 'Invalid path encode %s' % invoker.doEncodePath
        
        self.nameRef = nameRef
        self.invoker = invoker
        
    def populate(self, obj, specifications, support):
        '''
        @see: IAttributes.populate
        '''
        assert isinstance(specifications, dict), 'Invalid specifications %s' % specifications
        
        attributes = specifications.get('attributes')
        if attributes is None: attributes = specifications['attributes'] = {}
        assert isinstance(attributes, dict), 'Invalid attributes %s' % attributes
        pathSelf = self.invoker.doEncodePath(support)
        if Support.parameters in support and support.parameters:
            assert isinstance(support, Support)
            pathSelf = '%s?%s' % (pathSelf, urlencode(support.parameters))
         
        attributes[self.nameRef] = self.invoker.doEncodePath(support)
        specifications['adjust'] = ADJUST_SELF_DISCARD
