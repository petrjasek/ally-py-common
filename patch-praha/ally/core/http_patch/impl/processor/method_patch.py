'''
Created on Mar 7, 2014

@package: ally core
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the PATCH and PUT method combination.
'''

from ally.container.ioc import injected
from ally.design.processor.attribute import requires
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessor
from ally.http.spec.server import HTTP_PUT


# --------------------------------------------------------------------
class Request(Context):
    '''
    The request context.
    '''
    # ---------------------------------------------------------------- Required
    method = requires(str)

class Response(Context):
    '''
    The response context.
    '''
    # ---------------------------------------------------------------- Optional
    isSuccess = requires(bool)
    allows = requires(set)
    
# --------------------------------------------------------------------

@injected
class MethodPatchHandler(HandlerProcessor):
    '''
    Implementation for a processor that provides the PATCH and PUT method combination.
    '''
    
    def __init__(self):
        super().__init__()

    def process(self, chain, request:Request, response:Response, **keyargs):
        '''
        Provide the allowed mehtods.
        '''
        assert isinstance(request, Request), 'Invalid request %s' % request
        assert isinstance(response, Response), 'Invalid response %s' % response
        if response.isSuccess is False: return  # Skip in case the response is in error
        
        if response.allows and HTTP_PUT in response.allows: response.allows.add('PATCH')
        if request.method == 'PATCH': request.method = HTTP_PUT
        