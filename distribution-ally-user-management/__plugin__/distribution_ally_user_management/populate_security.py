'''
Created on Mar 14, 2014

@package: ally user management
@copyright: 2014 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Populates the security configurations.
'''

from io import BytesIO
import pkgutil

from ally.api.error import InputError
from ally.container import ioc, support, app
from ally.container.impl.proxy import proxyWrapFor, IProxyHandler, \
    registerProxyHandler, ProxyFilter
from security.rbac.api.role import IRoleService, Role

from hr.user.api.user import IUserService
from security.user.api.user_rbac import IUserRbacService

from ..gui_core.service import configurationStreams
from ..hr import service


# --------------------------------------------------------------------
@ioc.before(configurationStreams)
def updateConfigurationStreamsForDistribution():
    content = pkgutil.get_data('__plugin__.distribution_ally_user_management', 'security_configuration.xml')
    configurationStreams().append(('file://.../security_configuration.xml', BytesIO(content)))

@ioc.replace(ioc.entityOf('userService', module=service))
def userService(original):
    class AutoRolesProxy(IProxyHandler):
        ''' Automatically assign roles to new created users.'''
        
        def __init__(self, userRbacService):
            self.userRbacService = userRbacService
        
        def handle(self, execution):
            userId = execution.invoke()
            self.userRbacService.addRole(userId, 'Admin')
            return userId
            
    ioc.initialize(original)
    service = proxyWrapFor(original)
    handler = AutoRolesProxy(support.entityFor(IUserRbacService))
    handler = ProxyFilter(handler, 'insert')
    registerProxyHandler(handler, service)
    return service

@app.populate(app.DEVEL)
def updateUsersRoles():
    return
    roleService = support.entityFor(IRoleService)
    assert isinstance(roleService, IRoleService)
    
    try: roleService.getById('Admin')
    except InputError:
        role = Role()
        role.Name = 'Admin'
        role.Description = 'Full access role'
        roleService.insert(role)
        
    userService = support.entityFor(IUserService)
    assert isinstance(userService, IUserService)
    
    userRbacService = support.entityFor(IUserRbacService)
    assert isinstance(userRbacService, IUserRbacService)
    
    for userId in userService.getAll(): userRbacService.addRole(userId, 'Admin')
