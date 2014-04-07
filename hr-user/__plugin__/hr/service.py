'''
Created on Jan 9, 2012

@package: human resource/user
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Contains the setup user services.
'''

from ..plugin.registry import registerService
from .database import binders
from ally.container import support, bind, ioc
from ally.cdm.spec import ICDM
from ally.cdm.support import ExtendPathCDM
from __plugin__.cdm.service import contentDeliveryManager

# --------------------------------------------------------------------

SERVICES = 'hr.user.api.**.I*Service'

bind.bindToEntities('hr.user.impl.**.*Alchemy', binders=binders)
support.createEntitySetup('hr.user.impl.**.*')
support.listenToEntities(SERVICES, listeners=registerService)
support.loadAllEntities(SERVICES)

# --------------------------------------------------------------------

@ioc.entity
def cdmAvatar() -> ICDM:
    '''
    The content delivery manager (CDM) for the avatars.
    '''
    return ExtendPathCDM(contentDeliveryManager(), 'avatar/%s')
