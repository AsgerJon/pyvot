"""
EventHandler instances describes a reaction to a particular event.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

import minescript
import worktoy

if TYPE_CHECKING:  # pragma: no cover
  from typing import Callable, Any
