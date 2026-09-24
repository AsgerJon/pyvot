"""
EventTypes encapsulates the minescript event types.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from abc import ABC

import minescript


class EventTypes(ABC):
  pass


EventTypes.register(minescript.KeyEvent)
EventTypes.register(minescript.MouseEvent)
EventTypes.register(minescript.ChatEvent)
EventTypes.register(minescript.AddEntityEvent)
EventTypes.register(minescript.BlockUpdateEvent)
EventTypes.register(minescript.TakeItemEvent)
EventTypes.register(minescript.DamageEvent)
EventTypes.register(minescript.ExplosionEvent)
EventTypes.register(minescript.ChunkEvent)
EventTypes.register(minescript.WorldEvent)
