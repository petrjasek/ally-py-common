'''
Created on Mar 6, 2012

@package: hr user
@copyright: 2011 Sourcefabric o.p.s.
@license http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mihai Balaceanu

Implementation for user services.
'''

from ally.api.criteria import AsLike, AsBoolean
from ally.api.validate import validate
from ally.container import wire
from ally.container.ioc import injected
from ally.container.support import setup
from ally.internationalization import _
from functools import reduce
from sql_alchemy.impl.entity import EntityServiceAlchemy
from sql_alchemy.support.util_service import insertModel
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.expression import or_

from ally.api.error_p1 import ConflictError, InvalidError
from hr.user.api.user import IUserService, QUser, User, Password
from hr.user.meta.user import UserMapped


# --------------------------------------------------------------------
@injected
@setup(IUserService, name='userService')
@validate(UserMapped)
class UserServiceAlchemy(EntityServiceAlchemy, IUserService):
    '''
    Implementation for @see: IUserService
    '''
    default_user_type_key = 'standard'; wire.config('default_user_type_key', doc='''
    Default user type for users without specified the user type key''')
    allNames = {UserMapped.UserName, UserMapped.FullName, UserMapped.EMail, UserMapped.PhoneNumber}

    def __init__(self):
        '''
        Construct the service
        '''
        assert isinstance(self.default_user_type_key, str), 'Invalid default user type %s' % self.default_user_type_key
        assert isinstance(self.allNames, set), 'Invalid all name %s' % self.allNames
        EntityServiceAlchemy.__init__(self, UserMapped, QUser, all=self.queryAll, inactive=self.queryInactive)
    
    def getAll(self, q=None, **options):
        '''
        @see: IUserService.getAll
        '''
        if q is None: q = QUser(inactive=False)
        elif QUser.inactive not in q: q.inactive = False
        # Making sure that the default query is for active.
        return super().getAll(q, **options)

    def update(self, user):
        '''
        @see: IUserService.update
        '''
        assert isinstance(user, User), 'Invalid user %s' % user
        user.UserName = user.UserName.lower()
        self.checkUser(user, user.Id)
            
        return  super().update(user)

    def insert(self, user):
        '''
        @see: IUserService.insert
        '''
        assert isinstance(user, User), 'Invalid user %s' % user
        user.UserName = user.UserName.lower()
        self.checkUser(user)
        
        userDb = insertModel(UserMapped, user, password=user.Password)
        assert isinstance(userDb, UserMapped), 'Invalid user %s' % userDb
        return userDb.Id
   
    def changePassword(self, id, password):
        '''
        @see: IUserService.changePassword
        '''
        assert isinstance(password, Password), 'Invalid password change %s' % password
        try: userDb = self.session().query(UserMapped).filter(UserMapped.Id == id).one()
        except NoResultFound: raise InvalidError(_('Invalid old password'), Password.OldPassword)
        assert isinstance(userDb, UserMapped), 'Invalid user %s' % userDb
        
        userDb.password = password.NewPassword

    # ----------------------------------------------------------------
    
    def checkUser(self, user, userId=None):
        ''' Checks if the user name is not conflicting with other users names.'''
        if User.Active not in user or user.Active:
            sql = self.session().query(UserMapped.Id).filter(UserMapped.UserName == user.UserName)
            sql = sql.filter(UserMapped.Active == True)
            if userId is not None: sql = sql.filter(UserMapped.Id != userId)
            if sql.count() > 0: raise ConflictError(_('There is already an active user with this name'), User.UserName)
    
    def queryAll(self, sql, crit):
        '''
        Processes the all query.
        '''
        assert isinstance(crit, AsLike), 'Invalid criteria %s' % crit
        filters = []
        if AsLike.like in crit:
            for col in self.allNames: filters.append(col.like(crit.like))
        elif AsLike.ilike in crit:
            for col in self.allNames: filters.append(col.ilike(crit.ilike))
        sql = sql.filter(reduce(or_, filters))
        return sql
            
    def queryInactive(self, sql, crit):
        '''
        Processes the inactive query.
        '''
        assert isinstance(crit, AsBoolean), 'Invalid criteria %s' % crit
        return sql.filter(UserMapped.Active == (crit.value is False))
