"""
EventUpdate encapsulates 'EventQueue' instances in the descriptor
protocol, which returns the most recent value from '__get__', and updates
the value on the event triggering.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.mcls import BaseObject

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Callable


class EventUpdate(BaseObject):
  """
  EventUpdate encapsulates 'EventQueue' instances in the descriptor
  protocol, which returns the most recent value from '__get__', and updates
  the value on the event triggering.
  """

  def workerFactory(self, ) -> Callable:
    pass

  def __get__(self, instance: Any, owner: type) -> Any:
    if instance is None:
      return self
    raise NotImplementedError
