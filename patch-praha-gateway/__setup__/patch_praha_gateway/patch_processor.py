'''
Created on Mar 14, 2014

@package: patch praha gateway
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Nistor Gabriel

Provides the gateway processor patch.
'''

from ally.container import ioc

from ..ally_gateway.processor import gatewayRepository, gatewayAuthorizedRepository


# --------------------------------------------------------------------
@ioc.before(gatewayRepository)
def patchGatewayRepository():
    gatewayRepository().nameCollection = 'collection'
    
@ioc.before(gatewayAuthorizedRepository)
def patchGatewayAuthorizedRepository():
    gatewayAuthorizedRepository().nameCollection = 'collection'