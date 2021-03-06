'''
Created on Sep 3, 2012

@package: security user
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

The API specifications for the user authentication.
'''

from ally.api.config import service, call, INSERT, GET, DELETE
from ally.api.type import Iter
from datetime import datetime
from gateway.api.gateway import Gateway
from security.api.domain_security import modelSecurity

from hr.user.api.user import User


# --------------------------------------------------------------------
@modelSecurity(name='Authentication', id='Token')
class Token:
    '''
    Model for the authentication request.
    '''
    Token = str

@modelSecurity
class Authentication(Token):
    '''
    Model for the authentication data.
    '''
    HashedToken = str
    UserName = str

@modelSecurity(id='Session')
class Login:
    '''
    The login model.
    '''
    Session = str
    User = User
    CreatedOn = datetime
    AccessedOn = datetime

# --------------------------------------------------------------------

@service
class IAuthenticationService:
    '''
    The service that provides the authentication.
    '''

    @call(method=GET)
    def getGateways(self, session:Login.Session) -> Iter(Gateway):
        '''
        Provides the authenticated gateways for the provided session, if the session is invalid an error is raised.
        '''
        
    @call(method=INSERT)
    def requestLogin(self) -> Token:
        '''
        Create a token in order to authenticate.
        '''

    @call(method=INSERT)
    def performLogin(self, authentication:Authentication) -> Login:
        '''
        Called in order to authenticate
        '''
        
    @call(method=DELETE)
    def performLogout(self, session:Login) -> bool:
        '''
        Called in order to terminate the login session.
        '''
        
    # ----------------------------------------------------------------

    @call(filter='authenticated')
    def isAuthenticatedUser(self, authId:User, userId:User) -> bool:
        '''
        Checks if the authenticated user id is the same with the filtered user id. 
        '''
