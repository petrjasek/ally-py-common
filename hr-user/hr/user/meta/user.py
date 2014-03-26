'''
Created on Aug 23, 2011

@package: hr user
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mihai Balaceanu

Contains the SQL alchemy meta for user API.
'''

from ally.api.validate import validate, ReadOnly, Mandatory, Unique, EMail,\
    PhoneNumber, UserName
from sqlalchemy.dialects.mysql.base import INTEGER
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.schema import Column
from sqlalchemy.sql.expression import case
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.types import String, DateTime, Boolean
from hr.meta.metadata_hr import Base
from hr.user.api.user import User

# --------------------------------------------------------------------

@validate(Mandatory(User.Password), ReadOnly(User.CreatedOn), UserName(User.UserName),
          EMail(User.EMail), PhoneNumber(User.PhoneNumber))
class UserMapped(Base, User):
    '''
    Provides the mapping for User entity.
    '''
    __tablename__ = 'user'
    __table_args__ = dict(mysql_engine='InnoDB', mysql_charset='utf8')
    
    Id = Column('id', INTEGER(unsigned=True), primary_key=True)
    UserName = Column('user_name', String(150), nullable=False)
    FirstName = Column('first_name', String(255))
    LastName = Column('last_name', String(255))
    @hybrid_property
    def FullName(self):
        if self.FirstName is None: return self.LastName
        if self.LastName is None: return self.FirstName
        return '%s %s' % (self.FirstName, self.LastName)
    EMail = Column('email', String(255), unique=True)
    PhoneNumber = Column('phone_number', String(255))
    CreatedOn = Column('created_on', DateTime, nullable=False, default=current_timestamp())
    Active = Column('active', Boolean, nullable=False, default=True)
    # Expression for hybrid ------------------------------------
    @FullName.expression
    def FullName(cls):  # @NoSelf
        return case([(cls.FirstName == None, cls.LastName)], else_=
                    case([(cls.LastName == None, cls.FirstName)], else_=cls.FirstName + ' ' + cls.LastName))
    # Non REST model attribute --------------------------------------
    password = Column('password', String(255), nullable=False)

validate(Unique(UserMapped.EMail))(UserMapped)
