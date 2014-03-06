'''
Created on Mar 5, 2014

@package: distribution-ally-user-management
@copyright: 2014 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mugur Rus

Populates the database with the default users.
'''

import hashlib
from ally.container import app, support
from hr.user.api.user import IUserService, QUser, User

# --------------------------------------------------------------------

@app.populate
def populateDefaultUsers():
    userService = support.entityFor(IUserService)
    assert isinstance(userService, IUserService)
    
    for name in (('User', 'Admin'),):
        loginName = name[1].lower()
        users = userService.getAll(limit=1, q=QUser(userName=loginName))
        try: user = next(iter(users))
        except StopIteration:
            user = User()
            user.UserName = loginName
            user.FirstName = name[0]
            user.LastName = name[1]
            user.EMail = '%s.%s@email.addr' % name
            user.Password = hashlib.sha512(bytes(loginName, 'utf-8')).hexdigest()
            user.Id = userService.insert(user)
