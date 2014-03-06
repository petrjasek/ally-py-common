'''
Created on Mar 6, 2014

@package: patch praha
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the processor setup patches.
'''

from __setup__.ally_core_http.processor import updateHeadersCors, \
    headersCorsAllow
from ally.container import ioc


# --------------------------------------------------------------------
@ioc.after(updateHeadersCors)
def updateHeadersCorsForAuthorization():
    headersCorsAllow().add('Authorization')

