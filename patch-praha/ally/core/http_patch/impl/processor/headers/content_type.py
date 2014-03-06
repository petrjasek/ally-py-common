'''
Created on Mar 6, 2014

@package: ally http
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the content type header decoding/encoding.
'''

from ally.container.ioc import injected
from ally.design.processor.attribute import requires
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessor
from ally.http.spec.headers import CONTENT_TYPE, HeadersDefines
        
# --------------------------------------------------------------------

class ResponseContentEncode(Context):
    '''
    The response content context.
    '''
    # ---------------------------------------------------------------- Required
    type = requires(str)

# --------------------------------------------------------------------

@injected
class ContentTypeResponseEncodeHandler(HandlerProcessor):
    '''
    Implementation for a processor that provides the encoding of content type HTTP request header.
    '''

    def process(self, chain, response:HeadersDefines, responseCnt:ResponseContentEncode, **keyargs):
        '''
        @see: HandlerProcessor.process
        
        Encodes the content type for the response.
        '''
        assert isinstance(responseCnt, ResponseContentEncode), 'Invalid response content %s' % responseCnt

        if responseCnt.type: CONTENT_TYPE.encode(response, responseCnt.type)