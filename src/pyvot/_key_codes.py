"""
KeyNum enumerates the key codes as defined by GLFW.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.keenum import KeeNum, Kee

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Self


class KeyNum(KeeNum):
  """
  KeyNum enumerates the key codes as defined by GLFW.
  """

  SPACE = Kee[int](32)
  D0 = Kee[int](48)
  D1 = Kee[int](49)
  D2 = Kee[int](50)
  D3 = Kee[int](51)
  D4 = Kee[int](52)
  D5 = Kee[int](53)
  D6 = Kee[int](54)
  D7 = Kee[int](55)
  D8 = Kee[int](56)
  D9 = Kee[int](57)
  K_A = Kee[int](65)
  K_B = Kee[int](66)
  K_C = Kee[int](67)
  K_D = Kee[int](68)
  K_E = Kee[int](69)
  K_F = Kee[int](70)
  K_G = Kee[int](71)
  K_H = Kee[int](72)
  K_I = Kee[int](73)
  K_J = Kee[int](74)
  K_K = Kee[int](75)
  K_L = Kee[int](76)
  K_M = Kee[int](77)
  K_N = Kee[int](78)
  K_O = Kee[int](79)
  K_P = Kee[int](80)
  K_Q = Kee[int](81)
  K_R = Kee[int](82)
  K_S = Kee[int](83)
  K_T = Kee[int](84)
  K_U = Kee[int](85)
  K_V = Kee[int](86)
  K_W = Kee[int](87)
  K_X = Kee[int](88)
  K_Y = Kee[int](89)
  K_Z = Kee[int](90)
  ESCAPE = Kee[int](256)
  ENTER = Kee[int](257)  # Interchangeable with RETURN
  RETURN = Kee[int](257)  # Interchangeable with ENTER
  TAB = Kee[int](258)
  BACKSPACE = Kee[int](259)
  INSERT = Kee[int](260)
  DELETE = Kee[int](261)
  RIGHT = Kee[int](262)
  ARROW_RIGHT = Kee[int](262)  # Interchangeable with RIGHT
  LEFT = Kee[int](263)
  ARROW_LEFT = Kee[int](263)  # Interchangeable with LEFT
  DOWN = Kee[int](264)
  ARROW_DOWN = Kee[int](264)  # Interchangeable with DOWN
  UP = Kee[int](265)
  ARROW_UP = Kee[int](265)  # Interchangeable with UP
  PAGE_UP = Kee[int](266)  # NOT interchangeable with UP
  PAGE_DOWN = Kee[int](267)  # NOT interchangeable with DOWN
  HOME = Kee[int](268)
  END = Kee[int](269)
  CAPS_LOCK = Kee[int](280)  # NOT recommended
  SCROLL_LOCK = Kee[int](281)  # NOT recommended
  NUM_LOCK = Kee[int](282)  # NOT recommended
  PRINT_SCREEN = Kee[int](283)  # NOT recommended
  PAUSE = Kee[int](284)  # NOT recommended
  MENU = Kee[int](348)  # NOT recommended
  #  Function keys
  F1 = Kee[int](290)
  F2 = Kee[int](291)
  F3 = Kee[int](292)
  F4 = Kee[int](293)
  F5 = Kee[int](294)
  F6 = Kee[int](295)
  F7 = Kee[int](296)
  F8 = Kee[int](297)
  F9 = Kee[int](298)
  F10 = Kee[int](299)
  F11 = Kee[int](300)
  F12 = Kee[int](301)
  #  Keypad keys
  KP_0 = Kee[int](320)
  KP_1 = Kee[int](321)
  KP_2 = Kee[int](322)
  KP_3 = Kee[int](323)
  KP_4 = Kee[int](324)
  KP_5 = Kee[int](325)
  KP_6 = Kee[int](326)
  KP_7 = Kee[int](327)
  KP_8 = Kee[int](328)
  KP_9 = Kee[int](329)
  KP_DECIMAL = Kee[int](330)
  KP_DIVIDE = Kee[int](331)
  KP_MULTIPLY = Kee[int](332)
  KP_SUBTRACT = Kee[int](333)
  KP_ADD = Kee[int](334)
  KP_ENTER = Kee[int](335)
  KP_EQUAL = Kee[int](336)
  #  Modifier keys
  LEFT_SHIFT = Kee[int](340)
  RIGHT_SHIFT = Kee[int](344)
  LEFT_ALT = Kee[int](342)
  RIGHT_ALT = Kee[int](346)
  #  #  CTRL aliases
  LEFT_CTRL = Kee[int](341)
  LEFT_CONTROL = Kee[int](341)
  RIGHT_CTRL = Kee[int](345)
  RIGHT_CONTROL = Kee[int](345)
  #  #  META aliases
  LEFT_META = Kee[int](343)
  LEFT_COMMAND = Kee[int](343)
  LEFT_CMD = Kee[int](343)
  LEFT_WIN = Kee[int](343)
  LEFT_SUPER = Kee[int](343)
  RIGHT_META = Kee[int](347)
  RIGHT_COMMAND = Kee[int](347)
  RIGHT_CMD = Kee[int](347)
  RIGHT_WIN = Kee[int](347)
  RIGHT_SUPER = Kee[int](347)
  #  Agnostic modifiers
  ALT = Kee[int](2 ** 9 * 342 + 346)
  CTRL = Kee[int](2 ** 9 * 341 + 345)
  CONTROL = Kee[int](2 ** 9 * 341 + 345)
  SHIFT = Kee[int](2 ** 9 * 340 + 344)
  META = Kee[int](2 ** 9 * 343 + 347)
  COMMAND = Kee[int](2 ** 9 * 343 + 347)
  CMD = Kee[int](2 ** 9 * 343 + 347)
  SUPER = Kee[int](2 ** 9 * 343 + 347)
  WIN = Kee[int](2 ** 9 * 343 + 347)

  @classmethod
  def fromText(cls, text: str) -> Self:
    if not str.replace(text, ' ', ''):
      return cls.fromText('SPACE')
    versions = (text.upper(), text.replace('_', ''), text)
    for version in versions:
      for member in cls:
        if version == member.name:
          return member
    infoSpec = """No KeyNum member matches the text '%s'!"""
    info = infoSpec % text
    raise ValueError(info)

  @classmethod
  def fromValue(cls, value: int) -> Self:
    if 0 <= value <= 9:
      return cls.fromText('KP_%d' % value)  # Keypad numbers
    for member in cls:
      if value == member.value:
        return member
    infoSpec = """No KeyNum member matches the value '%s'!"""
    info = infoSpec % value
    raise ValueError(info)

  @classmethod
  def _resolveOther(cls, other: Any) -> Self:
    if isinstance(other, cls):
      return other
    if isinstance(other, str):
      try:
        textOther = cls.fromText(other)
      except ValueError:
        return NotImplemented
      else:
        return textOther
    if isinstance(other, int):
      try:
        valueOther = cls.fromValue(other)
      except ValueError:
        return NotImplemented
      else:
        return valueOther
    return NotImplemented

  def matches(self, other: Any) -> bool:
    otherKeyNum = self._resolveOther(other)
    if otherKeyNum is NotImplemented:
      return NotImplemented
    if self.value == otherKeyNum.value:
      return True
    #  Handle agnostic modifier keys by value
    if self.value < 2 ** 9 == otherKeyNum.value < 2 ** 9:
      return False
    if self.value < 2 ** 9:
      return otherKeyNum.matches(self)
    sides = (self.value // (2 ** 9), self.value % (2 ** 9))
    return True if otherKeyNum.value in sides else False

  def __eq__(self, other: Any) -> bool:
    otherKeyNum = self._resolveOther(other)
    if otherKeyNum is NotImplemented:
      return NotImplemented
    return True if self.value == otherKeyNum.value else False

  def __hash__(self, ) -> int:
    if self.value < 2 ** 9:
      return hash((type(self).__name__, self.value), )
    raise TypeError("""Agnostic modifier keys are unhashable!""")
