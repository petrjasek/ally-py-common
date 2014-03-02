'''
Created on Feb 28, 2014

@author: chupy
'''

from setuptools import setup
from setuptools.command.develop import develop
from os.path import os
from distutils.errors import DistutilsOptionError
from urllib.parse import parse_qs
from pip.vcs.git import Git

# --------------------------------------------------------------------

class AllyDevelop(develop):
    ''' Provides the ally packages development install.'''
    
    description = 'install ally packages in \'development mode\''
    
    user_options = develop.user_options + [
        ('add=', None, 'Additional git repositories to fetch ally packages, in order to provide more then one git repository '\
         'then provide a pipe \'|\' separator between the git URLs. The git URLs need to be identical to those in \'-e\' command.')
        ]
    
    def initialize_options(self):
        self.add = None
        super().initialize_options()
    
    def run(self):
        if not self.add: return
        folder = os.path.dirname(self.egg_path)
        for path in self.add.split('|'):
            url = urlsplit(path)
            badFragment = False
            if url.fragment:
                fragments = parse_qs(url.fragment)
                if not 'egg' in fragments: badFragment = True
            if badFragment:
                raise DistutilsOptionError('Missing the git URL egg fragment ex:\'https://github.com/../somwhere#eqq=somwhere\'')
            
            Git(path).obtain(os.path.join(folder, fragments[0]))
        
        print("================================================", self.add)
        
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
      cmdclass={'develop': AllyDevelop}
      )
