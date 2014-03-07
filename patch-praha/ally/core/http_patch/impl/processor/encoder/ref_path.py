'''
Created on Mar 6, 2014

@package: patch praha
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the collection references paths.
'''

import logging
from urllib.parse import urlencode

from ally.api.extension import IterPart
from ally.api.type import Type, Iter
from ally.container.ioc import injected
from ally.core.impl.processor.encoder.base import ExportingSupport
from ally.core.spec.transform import ISpecifier, ITransfrom
from ally.design.processor.attribute import requires, defines, optional
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessor
from ally.support.util_spec import IDo
from collections import OrderedDict


# --------------------------------------------------------------------
log = logging.getLogger(__name__)

# --------------------------------------------------------------------

class Invoker(Context):
    '''
    The invoker context.
    '''
    # ---------------------------------------------------------------- Required
    doEncodePath = requires(IDo)

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

refPathExport = ExportingSupport(Support)
# The encoding path support export.

@injected
class RefPathAttributeEncode(HandlerProcessor):
    '''
    Implementation for a handler that provides the collection references paths.
    '''
    
    nameFirst = 'first'
    # The reference attribute name.
    nameLast = 'last'
    # The reference attribute name.
    namePrev = 'previous'
    # The reference attribute name.
    nameNext = 'next'
    # The reference attribute name.
    
    def __init__(self):
        assert isinstance(self.nameFirst, str), 'Invalid first reference name %s' % self.nameFirst
        assert isinstance(self.nameLast, str), 'Invalid last reference name %s' % self.nameLast
        assert isinstance(self.namePrev, str), 'Invalid previous reference name %s' % self.namePrev
        assert isinstance(self.nameNext, str), 'Invalid next reference name %s' % self.nameNext
        super().__init__()
        
    def process(self, chain, invoker:Invoker, create:Create, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Create the the collection references paths.
        '''
        assert isinstance(invoker, Invoker), 'Invalid invoker %s' % invoker
        assert isinstance(create, Create), 'Invalid create %s' % create
        
        if not isinstance(create.objType, Iter): return
        # The type is not for a collection, nothing to do, just move along
        if Create.encoder in create and create.encoder is not None: return 
        # There is already an encoder, nothing to do.
       
        if create.specifiers is None: create.specifiers = []
        create.specifiers.append(AttributeRefPath(self, invoker))

# --------------------------------------------------------------------

class AttributeRefPath(ISpecifier):
    '''
    Implementation for a @see: ISpecifier for paths.
    '''
    
    def __init__(self, handler, invoker):
        '''
        Construct the paths attributes.
        '''
        assert isinstance(handler, RefPathAttributeEncode), 'Invalid next reference name %s' % handler
        assert isinstance(invoker, Invoker), 'Invalid invoker %s' % invoker
        assert isinstance(invoker.doEncodePath, IDo), 'Invalid path encode %s' % invoker.doEncodePath
        
        self.handler = handler
        self.invoker = invoker
        
    def populate(self, obj, specifications, support):
        '''
        @see: IAttributes.populate
        '''
        assert isinstance(specifications, dict), 'Invalid specifications %s' % specifications
        assert isinstance(support, Support), 'Invalid support %s' % support
        
        if not isinstance(obj, IterPart): return
        assert isinstance(obj, IterPart)
        if obj.offset is None or obj.limit is None or obj.total is None: return
        
        offsets = OrderedDict()
        if obj.offset - obj.limit >= 0:
            offsets[self.handler.nameFirst] = 0
        if obj.offset - obj.limit >= 0:
            offsets[self.handler.namePrev] = obj.offset - obj.limit
        if obj.offset + obj.limit < obj.total:
            offsets[self.handler.nameNext] = obj.offset + obj.limit
        if obj.offset + obj.limit < obj.total:
            offsets[self.handler.nameLast] = obj.total - obj.limit

        if offsets:
            attributes = specifications.get('attributes')
            if attributes is None: attributes = specifications['attributes'] = OrderedDict()
            elif not isinstance(attributes, OrderedDict): attributes = specifications['attributes'] = OrderedDict(attributes)
            assert isinstance(attributes, dict), 'Invalid attributes %s' % attributes
            path = '%s?' % self.invoker.doEncodePath(support)
            reqParams = []
            if support.parameters:
                for name, value in support.parameters:
                    if name in ('offset', 'maxResults', 'total'): continue
                    reqParams.append((name, value))
            reqParams.append(('maxResults', obj.limit))
            for name, offset in offsets.items():
                attributes[name] = path + urlencode(reqParams + [('offset', offset)])
