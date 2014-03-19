'''
Created on Mar 19, 2014

@package: patch praha
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the parsing/rendering setup patches.
'''

from __setup__.ally_core.parsing_rendering import renderJSON
from ally.container import ioc


# --------------------------------------------------------------------
@ioc.before(renderJSON)
def patchRenderJSON():
    renderJSON().nameCollection = 'collection'
