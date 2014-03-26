'''
Created on Aug 23, 2011

@package: security user
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Nistor Gabriel

Contains the SQL alchemy meta for authentication API.
'''

from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import String, DateTime

from hr.meta.metadata_hr import Base
from hr.user.meta.user import UserMapped

from ..api.authentication import Token, Login


# --------------------------------------------------------------------
class TokenMapped(Base, Token):
    '''
    Provides the mapping for Token authentication entity.
    '''
    __tablename__ = 'authentication_token'
    __table_args__ = dict(mysql_engine='InnoDB')

    Token = Column('token', String(190), primary_key=True)

    # Non REST model attributes --------------------------------------
    requestedOn = Column('requested_on', DateTime, nullable=False)

class LoginMapped(Base, Login):
    '''
    Provides the mapping for Login entity.
    '''
    __tablename__ = 'authentication_login'
    __table_args__ = dict(mysql_engine='InnoDB')

    Session = Column('session', String(190), primary_key=True)
    User = Column('fk_user_id', ForeignKey(UserMapped.Id), nullable=False)
    CreatedOn = Column('created_on', DateTime, nullable=False)
    AccessedOn = Column('accessed_on', DateTime, nullable=False)

