'''
Created on Mar 6, 2014

@package: patch praha
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the decode setup patches.
'''

from __setup__.ally_core_http.decode import optionDecode
from ally.container import ioc
from ally.design.processor.handler import Handler

from ally.core.http_patch.impl.processor.decoder.parameter.option import OptionDecode


# --------------------------------------------------------------------
@ioc.replace(optionDecode)
def optionDecodeReplace() -> Handler: return OptionDecode()
