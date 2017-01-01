from reci_spi import Directive
from reci_spi import Vocabulary

class HelloWorld(Directive):
  def realize(self, dir):
    print "Hello World!"

class Vocab(Vocabulary):
  def __init__(self):
    self.ns = 'http://recipy.hoverview.org/bollhav'
    self.elms = {
      'helloworld': HelloWorld
    }
