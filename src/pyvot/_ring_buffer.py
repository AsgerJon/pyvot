"""
RingBuffer provides a performant circular buffer implementation.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from collections import deque

from worktoy.utilities import typeCast
from worktoy.waitaminute import TypeException
from worktoy.waitaminute.dispatch import TypeCastException

if TYPE_CHECKING:  # pragma: no cover
  from typing import Generic, TypeVar, List, Iterator


class RingBuffer:
  """
  RingBuffer provides a performant circular buffer implementation.
  """

  def __init__(self, capacity: int, *args: float) -> None:
    self._buffer = deque(maxlen=capacity)
    for arg in args:
      self.append(arg)

  def append(self, item: float) -> None:
    if isinstance(item, float):
      return self._buffer.append(item)
    try:
      floatValue = typeCast(float, item)
    except TypeCastException as typeCastException:
      raise TypeException('item', item, float) from typeCastException
    else:
      self._buffer.append(floatValue)

  def __getitem__(self, index: int) -> float:
    if index < 0:
      return self[len(self) + index]
    if index < len(self):
      return self._buffer[index]
    raise IndexError("""Index '%d' out of range.""" % index)

  def __len__(self) -> int:
    return len(self._buffer)

  def __iter__(self) -> Iterator[float]:
    yield from self._buffer
