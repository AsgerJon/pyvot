"""
KeyBind instances represent a mapping from one keyboard key to any
number of functions. It implements the descriptor protocol, meaning it
should be instantiated in another class, which then decorates methods
defined within that class body.

The keyboard key can be set immediately at instantiation by passing either
a string, an integer or a KeyNum instance. Strings are case-insensitive
and underscores are ignored.

- Default string resolution:
By default, if any enumeration in 'KeyNum' matches the string when
ignoring case and underscores, that enumeration member is used. This
applies ahead the following.

- Single character digit strings '0' - '9'
It resolves to the key-pad keys, assuming the top-row number keys retain
their default minecraft mapping to positions on the hotbar. Same with
function-keys. The top-row number keys are named 'D0', 'D1', ... 'D9',
the function keys are named verbatim: 'F1', 'F2', ... 'F12', and the
default key-pad keys are named 'KP_0', 'KP_1', ... 'KP_9'.

- Special strings:
'ENTER' and 'RETURN' both match to the enter key, whereas 'KP_ENTER'
matches to the keypad enter key.

'SPACE' matches to the space bar, as does a white-space-only string.

'UP', 'DOWN', 'LEFT' and 'RIGHT' match to the respective arrow keys,
otherwise named 'ARROW_UP', 'ARROW_DOWN', 'ARROW_LEFT' and 'ARROW_RIGHT',
respectively. Meaning that 'UP' is interchangeable with 'ARROW_UP',
but *not* with 'PAGE_UP'.

Modifier keys are enumerated separately for each side:
'LEFT_MOD' and 'RIGHT_MOD' for 'MOD' being any of: 'SHIFT', 'CTRL',
'ALT' and 'META'. The modifier keys additionally have the following
aliases (with side specification omitted):
- 'CONTROL' for 'CTRL'
- 'SUPER', 'WIN', 'CMD' and 'COMMAND' for 'META'
Additionally, passing just the modifier name without side specification
(e.g. 'SHIFT') will match to both left and right variants.

Passing an integer matches to the GLFW assigned value for the key, unless
it is 0 - 9, (which are not assigned by GLFW), in which case it matches to
the top-row number keys. Passing an integer not assigned by GLFW other
than the digits 0 - 9 will raise a ValueError.

Finally, the most explicit way is to pass a KeyNum enumeration member
directly.

Example:

  class App:
    enterKey = KeyBind('enter')  # same as 'RETURN' or KeyNum.ENTER
    rightControl = KeyBind(KeyNum.RIGHT_CONTROL)
    altKey = KeyBind('ALT')  # matches both left and right ALT keys
    keyPad5 = KeyBind('5')  # matches KeyNum.KP_5
    func5 = KeyBind('F5')  # matches KeyNum.F5
    row0 = KeyBind('D0')  # matches KeyNum.D0: Top-row number key 0


    @enterKey
    def onEnterPress(self):
      print("Enter key was pressed!")
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from minescript import KeyEvent
from worktoy.desc import Field
from worktoy.mcls import BaseObject
from worktoy.utilities import maybe
from worktoy.dispatch import overload
from worktoy.waitaminute import WriteOnceError, MissingVariable

from . import KeyNum

if TYPE_CHECKING:  # pragma: no cover
  from typing import Dict, Callable, Type, TypeAlias, Any

  Callbacks: TypeAlias = tuple[Callable, ...]


class KeyBind(BaseObject):
  """
  KeyBind instances represent a mapping from one keyboard key to any
  number of functions.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables

  #  Fallback Variables

  #  Private Variables
  __call_backs__ = None
  __key_value__ = None

  #  Public Variables
  callbacks = Field()
  key = Field()

  #  Virtual Variables

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @key.GET
  def _getKey(self) -> int:
    if self.__key_value__ is None:
      desc = type(self).key
      raise MissingVariable(desc, '__key_value__', KeyNum)
    return self.__key_value__.value

  @callbacks.GET
  def _getCallbacks(self) -> Callbacks:
    return maybe(self.__call_backs__, ())

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @key.SET
  def _setKey(self, keyValue: KeyNum) -> None:
    if self.__key_value__ is not None:
      desc = type(self).key
      raise WriteOnceError(desc, self.__key_value__, keyValue)
    self.__key_value__ = keyValue

  def _addCallback(self, callMeMaybe: Callable) -> Callable:
    existing = (*self.callbacks,)
    self.__call_backs__ = (*existing, callMeMaybe)
    return callMeMaybe

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __call__(self, callMeMaybe: Callable) -> Callable:
    return self._addCallback(callMeMaybe)

  def __get__(self, instance: Any, owner: type, ) -> Any:
    if instance is None:
      return self

    def callback(*args, **kwargs) -> None:
      for callMeMaybe in self.callbacks:
        callMeMaybe(instance, *args, **kwargs)

    return callback

  def __set_name__(self, owner: type, name: str, ) -> None:
    self.__field_owner__ = owner
    self.__field_name__ = name
    try:
      self.__field_owner__.registerKeyBind(self)
    except AttributeError:
      pass

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(KeyNum)
  def __init__(self, keyNum: KeyNum) -> None:
    self.__key_value__ = keyNum

  @overload(int)
  def __init__(self, keyValue: int) -> None:
    self.__init__(KeyNum.fromValue(keyValue))

  @overload(str)
  def __init__(self, keyName: str) -> None:
    modNums = (num for num in KeyNum if 'LEFT' in num.name)
    modNames = (num.name.replace('LEFT_', '') for num in modNums)
    if keyName in modNames:
      leftNum = 'LEFT_%s' % keyName
      rightNum = 'RIGHT_%s' % keyName

    self.__init__(KeyNum.fromName(keyName))

  @overload()
  def __init__(self) -> None:
    pass

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def callback(self, event: KeyEvent) -> None:
    for callMeMaybe in self.callbacks:
      callMeMaybe(event)
