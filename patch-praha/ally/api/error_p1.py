'''
Created on Feb 24, 2014

@package: hr user
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mihai Balaceanu

Patching for errors, this needs to be moved to ally-api.
'''
# TODO: Gabriel: Move to ally-api at the right moment.
from ally.api.error import InputError

# --------------------------------------------------------------------

class ConflictError(InputError):
    ''' Error raise when there is a conflict of model data.'''
    
    def __init__(self, msg, target=None):
        super().__init__(msg, target)
        
class InvalidError(InputError):
    ''' Error raise when there is an invalid model data.'''
    
    def __init__(self, msg, target=None):
        super().__init__(msg, target)