'''
Created on Jan 21, 2013

@package: security user
@copyright 2011 Sourcefabric o.p.s.
@license http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

API for user rbac services.
'''

from ally.api.config import service
from security.rbac.api.rbac import IRbacPrototype

from gui.action.api.category import IActionCategoryGetPrototype
from hr.user.api.user import User


# --------------------------------------------------------------------
@service(('RBAC', User), ('CATEGORY', User))
class IUserRbacService(IRbacPrototype, IActionCategoryGetPrototype):
    '''
    Provides the user RBAC service.
    '''
