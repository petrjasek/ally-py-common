'''
Created on Feb 27, 2014

@package: patch praha
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides HTTP patch specifications for indexes. 
'''

from ally.assemblage.http.impl.processor.assembler import ACTION_STREAM
from ally.core.impl.index import ADJUST_STANDARD
from ally.core.impl.processor.render import json, xml
from ally.indexing.spec.model import Block, Action
from ally.indexing.spec.perform import skip, feed, feedName


# --------------------------------------------------------------------
ADJUST_SELF_DISCARD = 'self discard'  # The action name to get the self reference discard.

# --------------------------------------------------------------------
# Provides the HTTP block definitions.
BLOCKS_PATCH = {}

BLOCKS_PATCH[json.PATTERN_JSON_START_ADJUST % ADJUST_SELF_DISCARD] = \
Block(
      Action(json.ACTION_JSON_ADJUST,
             feed(json.SIND_ATTRS),
             skip(json.IND_DECL)),
      Action(ACTION_STREAM,
             feed(json.IND_DECL)),
      )
BLOCKS_PATCH[json.PATTERN_JSON_END_ADJUST % ADJUST_SELF_DISCARD] = json.BLOCKS_JSON[json.PATTERN_JSON_END_ADJUST % ADJUST_STANDARD]


BLOCKS_PATCH[xml.PATTERN_XML_START_ADJUST % ADJUST_SELF_DISCARD] = \
Block(
      Action(xml.ACTION_XML_ADJUST,
             skip(xml.IND_DECL),
             feed(xml.SIND_NAME), skip(xml.EIND_NAME), feedName(xml.VAR_XML_NAME),
             skip(xml.EIND_ATTRS), feedName(xml.VAR_XML_ATTRS),
             feed(xml.EIND_TAG)),
      Action(ACTION_STREAM,
             feed(xml.EIND_TAG)),
      )
BLOCKS_PATCH[xml.PATTERN_XML_END_ADJUST % ADJUST_SELF_DISCARD] = xml.BLOCKS_XML[xml.PATTERN_XML_END_ADJUST % ADJUST_STANDARD]