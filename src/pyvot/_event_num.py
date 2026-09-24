"""
EventNum enumerates the event types in minescript.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.desc import Field
from worktoy.keenum import Kee, KeeNum

from minescript import _EVENT_CONSTRUCTORS as eventDict  # noqa

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Iterator


class EventNum(KeeNum):
  """
  EventNum enumerates the event types in minescript.
  """

  minescriptType = Field()
  keys = Field()

  KEY = Kee[str]('key')
  MOUSE = Kee[str]('mouse')
  CHAT = Kee[str]('chat')
  ADD_ENTITY = Kee[str]('add_entity')
  BLOCK_UPDATE = Kee[str]('block_update')
  TAKE_ITEM = Kee[str]('take_item')
  DAMAGE = Kee[str]('damage')
  EXPLOSION = Kee[str]('explosion')
  CHUNK = Kee[str]('chunk')
  WORLD = Kee[str]('world')

  @minescriptType.GET
  def _getMinescriptType(self, ) -> type:
    return eventDict[self.value]

  @keys.GET
  def _getKeys(self, ) -> Iterator[str]:
    data = self.minescriptType.__dataclass_fields__
    for key, val in data.items():
      yield key
