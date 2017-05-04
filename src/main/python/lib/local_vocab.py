from reci_spi import Vocabulary
from reci_spi import Directive

import os

class Vocab(Vocabulary):
  def __init__(self):
      self.ns = "http://recipy.hoverview.org/local"
  def resolve(self, localname):
      raise "notyet"
