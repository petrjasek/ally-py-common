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
from ally.container import support, bind

# --------------------------------------------------------------------

SERVICES = 'hr.user.api.**.I*Service'

bind.bindToEntities('hr.user.impl.**.*Alchemy', binders=binders)
support.createEntitySetup('hr.user.impl.**.*')
support.listenToEntities(SERVICES, listeners=registerService)
support.loadAllEntities(SERVICES)
