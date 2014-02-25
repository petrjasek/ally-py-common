'''
Created on Jan 17, 2012

@package: human resource/user 
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the database settings.
'''

from ally.container import ioc

from hr.meta.metadata_hr import meta

from ..sql_alchemy.db_application import metas, bindApplicationSession


# --------------------------------------------------------------------
@ioc.entity
def binders(): return [bindApplicationSession]

# --------------------------------------------------------------------

@ioc.before(metas)
def updateMetasForHumanResource(): metas().append(meta)
