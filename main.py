"""
Main Tester Script
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

import os
import sys
import threading

from worktoy.utilities import ExceptionInfo, typeCast, textFmt

from pyvot import KeyNum, EventNum
from yolo_dev import runTests, yolo
from threading import _shutdown as shutdown  # noqa


def tester00() -> int:
  """
  Hello World!
  """
  stuff = [os, sys, print, object, 'Hello world!']
  for item in stuff:
    if print(item):
      break
  else:
    return 0
  return 1


def tester01(*args, ) -> int:
  """
  Testing the presence of minescript.
  """

  with ExceptionInfo(ImportError) as info:
    import minescript
  print(info.report)
  for item in sys.path:
    print(os.path.abspath(item))
  return 0


def tester02() -> int:
  """
  Testing bit & operator
  """

  def fromStr(num: str) -> int:
    out = 0
    for i, char in enumerate(reversed(num)):
      out += (2 ** i if char == '1' else 0)
    return out

  def log2Ceil(num: int) -> int:
    castedNum = typeCast(int, num)
    if castedNum < 0:
      raise ValueError("""Complex numbers are not supported.""")
    if castedNum == 0:
      raise ZeroDivisionError
    if castedNum == 1:
      return 0
    return 1 + log2Ceil(int(castedNum / 2))

  def toStr(num: int, length: int = None) -> str:
    if length is None:
      return toStr(num, log2Ceil(num))
    castedNum = typeCast(int, num)
    if castedNum < 0:
      raise ValueError("""Signed integers not supported!""")
    bits = []
    for i in range(length):
      bits.append('1' if (castedNum & (2 ** i)) else '0')
    bits.reverse()
    return ''.join(bits)

  a = 69
  b = 420
  ab16 = a * 2 ** 16 + b
  print("""a = %d""" % a)
  print("""b = %d""" % b)
  print("""ab16 = %d""" % ab16)
  print("""a in bits    = %16s""" % toStr(a, 16))
  print("""b in bits    = %16s""" % toStr(b, 16))
  print("""a & b        = %16s""" % toStr(a & b, 16))
  print("""a | b        = %16s""" % toStr(a | b, 16))
  print("""a ^ b        = %16s""" % toStr(a ^ b, 16))
  print('-' * 48)
  print("""a in bits    = %16s""" % toStr(a, 16))
  print("""b in bits    = %32s""" % toStr(b, 16))
  print("""ab16 in bits = %32s""" % toStr(ab16, 32))
  print("""ab16 & a: %s""" % (ab16 & a))
  return 0


def tester03(*args) -> int:
  """
  Testing bit | operator
  """
  test = 'True' if KeyNum.LEFT_ALT == KeyNum.ALT else 'False'
  print("""KeyNum.LEFT_ALT == KeyNum.ALT: %s""" % test)
  test = 'True' if KeyNum.ALT == KeyNum.LEFT_ALT else 'False'
  print("""KeyNum.ALT == KeyNum.LEFT_ALT: %s""" % test)
  return 0


def tester04() -> int:
  """
  Testing the EventNum"""

  numSpec = """<br>%s"""
  keySpec = """<tab>%s"""
  for eventNum in EventNum:
    cls = eventNum.minescriptType
    if not isinstance(cls, type):
      continue
    print(textFmt(numSpec % eventNum.name))
    for key in eventNum.keys:
      print(textFmt(keySpec % key))
  return 0


def tester05() -> int:
  print("""7.3 %% 1: %s""" % (7.3 % 1))

  return 0


if __name__ == '__main__':
  yolo(runTests, tester05, )
  print('Main done!')
