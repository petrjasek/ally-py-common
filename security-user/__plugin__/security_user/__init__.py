'''
Created on Jul 15, 2011

@package: security user
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Nistor Gabriel

Contains the user security authentication setup files.
'''

# --------------------------------------------------------------------

NAME = 'ally-security-user'
VERSION = '1.0'
AUTHOR = 'Gabriel Nistor'
AUTHOR_EMAIL = 'gabriel.nistor@sourcefabric.org'
KEYWORDS = ['Ally', 'REST', 'plugin', 'security', 'user']
DESCRIPTION = 'Provides the the user security'
LONG_DESCRIPTION = '''Authentication services based on the human resources users.'''
INSTALL_REQUIRES = ['ally-gateway-acl >= 1.0', 'ally-gui-action >= 1.0', 'ally-hr-user >= 1.0', 'ally-security-rbac >= 1.0']
