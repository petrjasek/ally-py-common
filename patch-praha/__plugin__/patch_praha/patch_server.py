'''
Created on Feb 19, 2013

@package: patch praha
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the ally core http setup patch.
'''

from __setup__.ally_core_http.server import root_uri_resources
from __setup__.ally_http.server import server_scheme
from ally.container import ioc


# --------------------------------------------------------------------
@ioc.replace(root_uri_resources)
def patch_root_uri_resources(): return None

@ioc.replace(server_scheme)
def patch_server_scheme(): return 'https'