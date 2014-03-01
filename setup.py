'''
Created on Feb 28, 2014

@author: chupy
'''

from setuptools import setup
from setuptools.command.develop import develop

# --------------------------------------------------------------------

class CustomDevelopCommand(develop):
    """Customized setuptools install command - prints a friendly greeting."""
    
    user_options = develop.user_options + [
        # Select installation scheme and set base director(y|ies)
        ('home=', None,
         "(Unix only) home directory to install under")
        ]
    
    def __init__(self, dist):
        print("-------------------", dist)
        super().__init__(dist)
    
    def run(self):
        print("================================================")
        install.run(self)
        
setup(platforms=['all'],
      zip_safe=True,
      license='GPL v3',
      url='http://www.sourcefabric.org/en/superdesk/',
      author='Gabriel Nistor',
      author_email='gabriel.nistor@sourcefabric.org',
      classifiers=['Development Status :: 4 - Beta'],
      description='The ally user management',
      keywords=['Ally', 'user', 'management', 'service'],
      long_description='The components that represent the basic ally user management.',
      name='ally-user-management',
      version='1.0',
    cmdclass={
      'develop': CustomDevelopCommand,
      },
      )

