"""
Control provides keybinds for controlling the PyVot application.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import time
from threading import Thread
from math import floor, ceil
from typing import TYPE_CHECKING

from worktoy.desc import Field
from worktoy.utilities import maybe, textFmt
from worktoy.waitaminute import TypeException

from . import KeyBind, KeyNum

if TYPE_CHECKING:  # pragma: no cover
  from typing import Dict, Callable, Optional, Iterator

from minescript import EventQueue, player_position, player_orientation, \
  player_set_orientation, KeyEvent, player_press_attack, \
  player_press_pick_item, player_press_use


class Control:
  """
  Control provides keybinds for controlling the PyVot application.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __keybind_register__ = None

  #  Fallback Variables
  __fallback_allow__ = True

  #  Private Variables
  __yaw_step__ = 45
  __pitch_step__ = 5
  __pitch_click__ = 1
  __run_thread__ = None
  __allow_run__ = None

  #  Public Variables
  yaw = Field()
  pitch = Field()
  xf = Field()
  yf = Field()
  zf = Field()
  runThread = Field()
  allowRun = Field()

  #  Virtual Variables
  yawStep = Field()
  pitchStep = Field()
  pitchClick = Field()
  nearestYaw = Field()
  nearestPitch = Field()

  #  Keybinds
  #  #  Numpads
  kp1 = KeyBind(KeyNum.KP_1)
  kp2 = KeyBind(KeyNum.KP_2)
  kp3 = KeyBind(KeyNum.KP_3)
  kp4 = KeyBind(KeyNum.KP_4)
  kp5 = KeyBind(KeyNum.KP_5)
  kp6 = KeyBind(KeyNum.KP_6)
  kp7 = KeyBind(KeyNum.KP_7)
  kp8 = KeyBind(KeyNum.KP_8)
  kp9 = KeyBind(KeyNum.KP_9)
  #  #  Letters
  kR = KeyBind(KeyNum.K_R)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def getKeyBinds(cls, ) -> Dict[int, KeyBind]:
    return maybe(cls.__keybind_register__, dict())

  @allowRun.GET
  def _getAllowRun(self) -> bool:
    flag = maybe(self.__allow_run__, self.__fallback_allow__)
    return True if flag else False

  def _createThread(self, ) -> None:
    self.__run_thread__ = Thread(target=self.worker, daemon=True)

  @runThread.GET
  def _getRunThread(self, **kwargs) -> Thread:
    if self.__run_thread__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createThread()
      return self._getRunThread(_recursion=True)
    if isinstance(self.__run_thread__, Thread):
      return self.__run_thread__
    name, value = '__run_thread__', self.__run_thread__
    raise TypeException(name, value, Thread)

  @yaw.GET
  def _getYaw(self) -> float:
    return player_orientation()[0]

  @pitch.GET
  def _getPitch(self) -> float:
    return player_orientation()[1]

  @xf.GET
  def _getXf(self) -> float:
    return player_position()[0]

  @yf.GET
  def _getYf(self) -> float:
    return player_position()[1]

  @zf.GET
  def _getZf(self) -> float:
    return player_position()[2]

  @yawStep.GET
  def _getTurnIncrement(self) -> float:
    return self.__yaw_step__

  @nearestYaw.GET
  def _getNearestYaw(self) -> float:
    yaw = self.yaw
    step = self.yawStep
    return round(yaw / step) * step

  @pitchClick.GET
  def _getPitchClick(self) -> float:
    return self.__pitch_click__

  @pitchStep.GET
  def _getPitchIncrement(self) -> float:
    if self.pitch ** 2 < 75 ** 2:
      return self.__pitch_step__
    return self.__pitch_click__

  @nearestPitch.GET
  def _getNearestPitch(self) -> float:
    pitch = self.pitch
    step = self.pitchStep
    return round(pitch / step) * step

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @kp5
  def _snapDown(self, event: KeyEvent, ) -> bool:
    print("Snap down event received:", event)
    if not event.action:
      return False
    pitch90 = self.pitch + 90
    if float.is_integer(pitch90 / self.pitchStep):
      return player_set_orientation(self.yaw, pitch90 + self.pitchStep - 90)
    pitch90floor = (pitch90 // self.pitchStep) * self.pitchStep - 90
    pitch90ceil = pitch90floor + self.pitchStep
    pitches = (pitch90floor, pitch90ceil)
    return player_set_orientation(self.yaw, max(pitches))

  @kp8
  def _snapUp(self, event: KeyEvent, ) -> bool:
    if not event.action:
      return False
    pitch90 = self.pitch + 90
    if float.is_integer(pitch90 / self.pitchStep):
      return player_set_orientation(self.yaw, pitch90 - self.pitchStep - 90)
    pitch90floor = (pitch90 // self.pitchStep) * self.pitchStep - 90
    pitch90ceil = pitch90floor + self.pitchStep
    pitches = (pitch90floor, pitch90ceil)
    return player_set_orientation(self.yaw, min(pitches))

  @kp7
  def _peakDown(self, event: KeyEvent, ) -> bool:
    if not event.action:
      return False
    pitch90 = self.pitch + 90
    if float.is_integer(pitch90 / self.pitchClick):
      return player_set_orientation(self.yaw, pitch90 + self.pitchClick - 90)
    pitch90floor = (pitch90 // self.pitchClick) * self.pitchClick - 90
    pitch90ceil = pitch90floor + self.pitchClick
    pitches = (pitch90floor, pitch90ceil)
    return player_set_orientation(self.yaw, max(pitches))

  @kp9
  def _peakUp(self, event: KeyEvent, ) -> bool:
    if not event.action:
      return False
    pitch90 = self.pitch + 90
    if float.is_integer(pitch90 / self.pitchClick):
      return player_set_orientation(self.yaw, pitch90 - self.pitchClick - 90)
    pitch90floor = (pitch90 // self.pitchClick) * self.pitchClick - 90
    pitch90ceil = pitch90floor + self.pitchClick
    pitches = (pitch90floor, pitch90ceil)
    return player_set_orientation(self.yaw, min(pitches))

  @kp4
  def _snapLeft(self, event: KeyEvent, ) -> bool:
    if not event.action:
      return False
    if self.yaw % self.yawStep:
      yawLeft = (floor(self.yaw / self.yawStep)) * self.yawStep
    else:
      yawLeft = self.yaw - self.yawStep
    if yawLeft < -180:
      return player_set_orientation(yawLeft + 360, self.pitch)
    if yawLeft > 180:
      return player_set_orientation(yawLeft - 360, self.pitch)
    return player_set_orientation(yawLeft, self.pitch)

  @kp6
  def _snapRight(self, event: KeyEvent, ) -> bool:
    if not event.action:
      return False
    if self.yaw % self.yawStep:
      yawRight = (floor(self.yaw / self.yawStep) + 1) * self.yawStep
    else:
      yawRight = self.yaw + self.yawStep
    if yawRight < -180:
      return player_set_orientation(yawRight + 360, self.pitch)
    if yawRight > 180:
      return player_set_orientation(yawRight - 360, self.pitch)
    return player_set_orientation(yawRight, self.pitch)

  @kp1
  def _attack(self, event: KeyEvent) -> bool:
    return player_press_attack(True if event.action else False)

  @kp2
  def _pickBlock(self, event: KeyEvent, ) -> bool:
    return player_press_pick_item(True if event.action else False)

  @kR
  @kp3
  def _stopPickBlock(self, event: KeyEvent, ) -> bool:
    return player_press_use(True if event.action else False)

  @classmethod
  def registerKeyBind(cls, keyBind: KeyBind) -> None:
    existing = cls.getKeyBinds()
    existing[keyBind.key] = keyBind
    cls.__keybind_register__ = existing

  def resolveKeyBind(self, event: KeyEvent) -> None:
    keyBinds = self.getKeyBinds()
    bindFromKey = keyBinds.get(event.key, None)
    bindFromScanCode = keyBinds.get(event.scan_code, None)
    bind = maybe(bindFromKey, bindFromScanCode)
    if bind is not None:
      callback = bind.__get__(self, type(self))
      callback(event)

  def worker(self, queue: EventQueue = None, **kwargs) -> None:
    if queue is None:
      queue = EventQueue()
      queue.register_key_listener()
      print("""Control worker started.""")
    event = queue.get()
    self.resolveKeyBind(event)
    if self.allowRun:
      try:
        return self.worker(queue, _=(kwargs.get('_', -1) + 1) % 1000, )
      except RecursionError as recursionError:
        tr = """maximum recursion depth"""
        if tr not in str(recursionError):
          raise recursionError
        time.sleep(0.01)
        return self.worker(queue, _=0)
    return None

  def run(self) -> None:
    print("""Control run started.""")
    self.worker01()

  def worker01(self) -> None:
    queue = EventQueue()
    queue.register_key_listener()
    print("""Control worker01 started.""")
    while self.allowRun:
      event = queue.get()
      self.resolveKeyBind(event)
    else:
      print("""Worker reached allowRun == False, stopping...""")
