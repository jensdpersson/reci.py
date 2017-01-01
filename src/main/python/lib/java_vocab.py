from reci_spi import Vocabulary
from reci_spi import Directive
import glob

import subprocess
def java(eval):
    cmd = ["java", eval]
    print cmd
    p = subprocess.Popen(cmd, \
                         stdout=subprocess.PIPE, \
                         stderr=subprocess.PIPE)
    (odata, edata) = p.communicate()
    return p.returncode

class Javadoc(Directive):
  def realize(self, folder):
    pass

class Vocab(Vocabulary):
  def __init__(self):
    self.ns = 'http://recipy.hoverview.org/javadoc'
    self.elms = {
      'javadoc': Javadoc
    }
