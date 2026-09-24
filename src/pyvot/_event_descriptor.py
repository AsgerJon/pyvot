"""
EventDescriptor encapsulates 'EventQueue' in the descriptor protocol.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from threading import Thread
from typing import TYPE_CHECKING

from minescript import EventQueue
from worktoy.desc import Field
from worktoy.utilities import maybe
from worktoy.waitaminute import TypeException

from . import RingBuffer

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Self, Callable


class EventDescriptor:
  """
  EventDescriptor encapsulates 'EventQueue' in the descriptor protocol.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables

  #  Fallback Variables
  __fallback_capacity__ = 32

  #  Private Variables
  __buffer_capacity__ = None
  __field_name__ = None
  __field_owner__ = None
  __ring_buffer__ = None
  __is_locked__ = None
  __allow_run__ = None
  __event_callback__ = None
  __run_thread__ = None

  #  Public Variables
  name = Field()
  owner = Field()
  ring = Field()
  isLocked = Field()
  allowRun = Field()
  eventCallback: Callable = Field()
  runThread = Field()
  eventType = Field()

  #  Virtual Variables

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @name.GET
  def _getName(self, ) -> str:
    return self.__field_name__

  @owner.GET
  def _getOwner(self, ) -> type:
    return self.__field_owner__

  def _createRingBuffer(self, ) -> None:
    capacity = maybe(self.__buffer_capacity__, self.__fallback_capacity__)
    self.__ring_buffer__ = RingBuffer(capacity)

  @ring.GET
  def _getRingBuffer(self, **kwargs) -> RingBuffer:
    if self.__ring_buffer__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createRingBuffer()
      return self._getRingBuffer(_recursion=True)
    if isinstance(self.__ring_buffer__, RingBuffer):
      return self.__ring_buffer__
    raise TypeException('__ring_buffer__', self.__ring_buffer__, RingBuffer)

  @isLocked.GET
  def _getIsLocked(self, ) -> bool:
    return True if self.__is_locked__ else False

  @allowRun.GET
  def _getAllowRun(self, ) -> bool:
    return True if self.__allow_run__ else False

  @eventCallback.GET
  def _getEventCallback(self, ) -> Callable:
    if self.__event_callback__ is None:
      def decorator(callMeMaybe: Callable) -> Callable:
        self.__event_callback__ = callMeMaybe
        return callMeMaybe

      return decorator
    return self.__event_callback__

  @runThread.GET
  def _getRunThread(self, **kwargs) -> Thread:
    if self.__run_thread__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self.__run_thread__ = Thread(target=self.worker, daemon=True)
      return self._getRunThread(_recursion=True)
    if isinstance(self.__run_thread__, Thread):
      return self.__run_thread__
    raise TypeException('__run_thread__', self.__run_thread__, Thread)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @isLocked.SET
  def _setLockedState(self, value: bool, ) -> None:
    self.__is_locked__ = True if value else False

  def toggleLock(self, ) -> None:
    currentState = True if self.isLocked else False
    self.isLocked = False if currentState else True

  def lock(self, ) -> Self:
    self.isLocked = True
    return self

  def unLock(self, ) -> Self:
    self.isLocked = False
    return self

  def updateValue(self, value: float) -> None:
    with self.lock():
      self.ring.append(value)

  def worker(self, queue: EventQueue = None) -> None:
    if queue is None:
      queue = EventQueue()
    event = queue.get()
    callback = self.eventCallback
    callback(event)
    if self.allowRun:
      return self.worker(queue)
    return None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __enter__(self, ) -> Self:
    return self

  def __exit__(self, _, exc: BaseException, __) -> None:
    self.unLock()
    if isinstance(exc, BaseException):
      raise exc

  def __get__(self, instance: Any, owner: type) -> Any:
    if instance is None:
      return self
    last5 = self.ring[-5:]
    weight5 = [2 ** i for i, _ in enumerate(last5)]
    weightedAverage = sum(v * w for v, w in zip(last5, weight5))
    return weightedAverage / sum(weight5)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, callMeMaybe: Callable) -> None:
    self.__event_callback__ = callMeMaybe

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
