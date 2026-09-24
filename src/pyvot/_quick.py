"""
Quick provides quick run
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

import minescript

if TYPE_CHECKING:  # pragma: no cover
  from typing import Self


class Quick:
  def __enter__(self, ) -> Self:
    queue = minescript.EventQueue()
