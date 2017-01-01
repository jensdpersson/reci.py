
from reci_spi import Vocabulary
from reci_spi import Directive

import subprocess
import os.path
import os


def xsltproc(xsl, src, dst, logko):
    cmd = ["xsltproc"]
    if logko:
        cmd.extend(["-v"])
    cmd.extend(["-o", dst, xsl, src])
    print os.path.exists(xsl)
    print "issuing command %s" % (cmd,)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    for line in p.stdout.readlines():
        print line
    return p.returncode

import glob
class XSLTOutput(Directive):

	def set_xsl(self, xsl):
	    self.xsl = xsl
		
	def set_src(self, src):
	    self.src = src
		
	def set_ext(self, ext):
	    self.ext = ext

        def set_log(self, logko):
            self.logko = logko

	def realize(self, todir):
           self.subrealize(todir)
           for f in glob.glob(self.src):
            name = os.path.basename(f)
            (name, ext) = os.path.splitext(name)
            name = ".".join([name, self.ext])
            tofile = os.path.sep.join([todir, name])
            if hasattr(self, "logko"):
                log = self.logko
            else:
                log = False
            xsltproc(self.xsl, f, tofile, log)

import tempfile
class XSLTemplate(Directive):
    name = None
    def set_name(self, name):
        self.name = name

    def realize(self, todir):
        path = tempfile.mkdtemp()
        self.subrealize(path)
        subs = os.listdir(path)
        if self.name:
           xsl = self.name
        else:
           xsl = subs[0]
        self.parent.set_xsl(os.path.join(path, xsl))

class Validation:
    def realize(self, todir):
        pass

class Vocab(Vocabulary):
    def __init__(self):
        self.ns = 'http://recipy.hoverview.org/xml'
        self.elms = {
            'xsltoutput': XSLTOutput,
            'xsltemplate':XSLTemplate,
            'validation': Validation
        }
		

