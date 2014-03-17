'''
Created on Mar 14, 2014

@package: patch praha
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the PATCH and PUT method combination for ACL access.
'''

from acl.core.impl.processor.assembler.index_access import IndexAccessHandler
from ally.http.spec.server import HTTP_PUT, HTTP_POST
from ally.container.ioc import injected
from ally.container.support import setup
from ally.design.processor.handler import Handler
from ally.container import wire


# --------------------------------------------------------------------

@injected
@setup(Handler, name='indexAccessPatch')
class IndexAccessPatchHandler(IndexAccessHandler):
    '''
    Handler that patches PATCH for PUT.
    '''
    input_methods = [HTTP_POST, HTTP_PUT, 'PATCH']; wire.config('input_methods', doc='''
    @rtype: list[string]
    The HTTP method names that can have an input model in order to be processed by ACL.
    ''')
    
    def mergeAccess(self, invoker, methodHTTP):
        '''
        @see: IndexAccessHandler.mergeAccess
        '''
        if methodHTTP == HTTP_PUT: super().mergeAccess(invoker, 'PATCH')
        super().mergeAccess(invoker, methodHTTP)