'''
Created on Mar 6, 2012

@package: hr user
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mihai Balaceanu

The API specifications for the user.
'''

from ally.api.config import service, query, UPDATE, call
from ally.api.criteria import AsLikeOrdered, AsDateTimeOrdered, AsLike, \
    AsBoolean
from ally.support.api.entity_ided import IEntityService, QEntity, Entity
from datetime import datetime

from hr.api.domain_hr import modelHR
from ally.api.type import Reference


# --------------------------------------------------------------------
@modelHR
class User(Entity):
    '''    
    Provides the user model.
    '''
    UserName = str
    EMail = str
    FirstName = str
    LastName = str
    FullName = str
    PhoneNumber = str
    Avatar = Reference
    CreatedOn = datetime
    Active = bool
    Password = str

@modelHR
class Password:
    '''
    Separate model for changing password actions.
    '''
    OldPassword = str
    NewPassword = str

# --------------------------------------------------------------------

@query(User)
class QUser(QEntity):
    '''
    Query for user model.
    '''
    userName = AsLikeOrdered
    email = AsLikeOrdered
    firstName = AsLikeOrdered
    lastName = AsLikeOrdered
    fullName = AsLikeOrdered
    phoneNumber = AsLikeOrdered
    createdOn = AsDateTimeOrdered
    inactive = AsBoolean
    all = AsLike

# --------------------------------------------------------------------

@service((Entity, User), (QEntity, QUser))
class IUserService(IEntityService):
    '''
    User model service interface
    '''
    
    @call(method=UPDATE)
    def changePassword(self, id:User.Id, password:Password):
        '''
        Changes user password
        '''
