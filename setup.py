'''
Created on Feb 28, 2014

@author: chupy
'''

from setuptools import setup

# --------------------------------------------------------------------

setup(platforms=['all'],
      zip_safe=True,
      license='GPL v3',
      url='http://www.sourcefabric.org/en/superdesk/',
      author='Gabriel Nistor',
      author_email='gabriel.nistor@sourcefabric.org',
      classifiers=['Development Status :: 4 - Beta'],
      description='The ally user management',
      install_requires=['ally-core-http == 1.0', 'ally-plugin >= 1.0', 'ally-hr-user >= 1.0', 'ally-security-user >= 1.0', 'ally-indexing-provider >= 1.0', 'ally-service-assemblage >= 1.0', 'ally-patch-praha'],
      keywords=['Ally', 'user', 'management', 'service'],
      long_description='The components that represent the basic ally user management.',
      name='ally-user-management',
      packages=[],
      version='1.0',
      dependency_links=[
        'git+https://github.com/sourcefabric/Ally-Py/tree/master/components#egg=ally_core_http-1.0'
        ]
      )

