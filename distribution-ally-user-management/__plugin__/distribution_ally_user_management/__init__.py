'''
Created on Jul 15, 2011

@package: distribution ally user management
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the distutlis setup for the collection of plugins that represent the user management.
'''

# --------------------------------------------------------------------

NAME = 'ally-user-management'
VERSION = '1.0'
DESCRIPTION = 'The ally user management'
AUTHOR = 'Gabriel Nistor'
AUTHOR_EMAIL = 'gabriel.nistor@sourcefabric.org'
KEYWORDS = ['Ally', 'user', 'management', 'service']
LONG_DESCRIPTION = '''The components that represent the basic ally user management.'''
CLASSIFIERS = ['Development Status :: 4 - Beta']
INSTALL_REQUIRES = ['ally-core-http >= 1.0', 'ally-plugin >= 1.0', 'ally-gui-core >= 1.0',
                    'ally-hr-user >= 1.0', 'ally-security-user >= 1.0', 'ally-indexing-provider >= 1.0',
                    'ally-patch-praha', 'ally-patch-praha-gateway >= 1.0', 'ally-http-mongrel2-server >= 1.0',
                    'ally-documentation >= 1.0', 'ally-service-assemblage >= 1.0']
__extra__ = dict(package_data={'__plugin__.distribution_ally_user_management': ['security/*']})
