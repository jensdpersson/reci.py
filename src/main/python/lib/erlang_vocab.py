
from reci_spi import Vocabulary
from reci_spi import Directive
import glob
from os import listdir
from os.path import isfile, join

import subprocess
def erl(eval, pa=None):
    cmd = ["erl"]
    if pa:
        for a in pa:
            cmd.extend(["-pa", a])
    cmd.extend(["-eval", eval])
    cmd.extend(["-s", "init", "stop"])
    #print cmd
    p = subprocess.Popen(cmd, \
                         stdout=subprocess.PIPE, \
                         stderr=subprocess.PIPE)
    (odata, edata) = p.communicate()
    #print edata
    #print odata
    return p.returncode

'''
 Generates the edoc documentation html for the source given.
'''
class Edoc(Directive):
    def __init__(self):
        self.src = "src/main/erlang/*.erl"

    def set_src(self, src):
        self.src = src

    def realize(self, dir):
        mods = ""
        for file in glob.glob(self.src):
            if mods != "":
                mods += ","
            mods += '"' + file + '"'
        eval = 'edoc:files([%s],[{dir, "%s"}])' % (mods, dir)
        erl(eval)


class Beamfiles(Directive):
    def __init__(self):
        Directive.__init__(self)
        self.src = "src/main/erlang/*.erl"
        self.includes = []
        self.pa = []
        self.pz = []
        self.flags = []

    def set_src(self, src):
        self.src = src

    def add_include(self, include):
        #print "include1 " + include
        self.includes.append(include)

    def add_codepathprefix(self, include):
        self.pa.append(include)

    def add_codepathsuffix(self, include):
        self.pz.append(include)

    def add_flag(self, flag):
        self.flags.append(flag)

    def realize(self, dir):
        self.subrealize(dir)

        self.files = glob.glob(self.src)
        cmd = ["erlc", "-o", dir]
        cmd.extend(self.flags)
        for include in self.includes:
            #print "include " + include
            cmd.extend(["-I", include])
        for include in self.pa:
            cmd.extend(["-pa", include])
        for include in self.pz:
            cmd.extend(["-pz", include])
        cmd.extend(self.files)

        #print cmd
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        for line in p.stdout.readlines():
            print line
        return p.returncode

import tempfile
class Includes(Directive):
    def realize(self, dir):
        path = tempfile.mkdtemp()
        self.subrealize(path)
        self.parent.add_include(path)

class CodePathPrefix(Directive):
    def realize(self, dir):
        path = tempfile.mkdtemp()
        self.subrealize(path)
        self.parent.add_codepathprefix(path)

class CodePathSuffix(Directive):
    def realize(self, dir):
        path = tempfile.mkdtemp()
        self.subrealize(path)
        self.parent.add_codepathsuffix(path)

class Flags(Directive):

    text = ""
    def add_text(self, text):
        self.text += text

    def realize(self, dir):
        self.parent.add_flag(self.text)


import os.path
class Eunit(Beamfiles):
    def __init__(self):
        Beamfiles.__init__(self)
        self.set_src("src/test/erlang/*")
        self.ebindir = "target/ebin"
        self.xslpi = None

    def set_ebin(self, ebindir):
        self.add_codepathprefix(ebindir)
        self.ebindir = ebindir

    def set_src(self, tests):
        Beamfiles.set_src(self, tests )
        self.tests = tests

    def set_xslpi(self, xslpi):
        self.xslpi = xslpi

    def realize(self, dir):
        tmp = tempfile.mkdtemp()
        Beamfiles.realize(self, tmp)
        testlist = []
        for path in glob.glob(self.tests):
            file = os.path.basename(path)
            #print "Test candidate " + file
            module = file.rpartition("_tests")[0]
            #will be emtpy string if substring not found
            if module:
                testlist.append(module)
        #print "Testing %s" % (testlist,)
        eval = 'eunit:test([' + str(','.join(testlist)) \
            + '], [{report, {eunit_surefire, [{dir, "' + dir + '"}]}}])'
        erl(eval, [self.ebindir,tmp])
        if self.xslpi:
            for f in listdir(dir):
                fpath = join(dir, f)
                if isfile(fpath) and f.endswith(".xml"):
                    myFile = open(join(dir, f))
                    firstLine = myFile.readline()
                    newFirstLine = "<?xml-stylesheet type='text/xsl' href='%s'?>" % (self.xslpi,)
                    rest = ''.join(myFile.readlines())
                    myFile.close()
                    myFile = open(fpath, 'w')
                    myFile.write(newFirstLine+rest);
                    myFile.close()

class Verdict(Directive):
     def __init__(self):
	Directive.__init__(self)
	self.specs = "src/test/litmus/erlang/*"

     def set_testspecs(self, specs):
	self.specs = specs

     def realize(self, dir):
        import litmus
    	for spec in glob.glob(self.specs):
		    cam = litmus.Campaign(spec)
		    #res = verdict.
		    for test in cam.tests:
		        print "running %s " % (test.synopsis,)
		        data = (test.facit, test.action)
		        evalstr = "%s=%s" % data
		        res = erl(evalstr)
		        if res == 0:
		            print "OK!"
		        else:
       		            print "Result %s" % (res,)
		    #execute the tests
		#campaign.run(dir)
        #leta efter funktioner som heter test_X,
        #med erl -eval m(...)
        #anse testet heta X. Kor alla sana funktioner,
        #en i taget, med eval. En krasch r en fail, ta med stacken.
        #fulskriv resultat till fil. hmm. eller sa far detta ske i
        #erlang i en verdict.erl i alla fall.

        #eval = 'edoc:files([%s],[{dir, "%s"}])' % (mods, dir)

import zipfile

class Escript(Directive):
    def __init__(self):
        Directive.__init__(self)
        self.main = None

    def set_filename(self, filename):
        self.filename = filename

    def set_main(self, main):
        self.main = main

    def realize(self, dir):
        tmp = tempfile.NamedTemporaryFile()
        z = zipfile.ZipFile(tmp, 'w')
        d = tempfile.mkdtemp()
        self.subrealize(d)
        for f in os.listdir(d):
            qf = os.path.join(d, f)
            #print 'adding ' + qf
            z.write(qf, f)
        z.close()

        if self.main:
            emus = ', {emu_args, "-escript main %s"}' % (self.main,)
        else:
            emus = ''
        parms = (os.path.join(dir, self.filename), tmp.name, emus)
        cmd = 'ok = escript:create("%s", [shebang, {archive, "%s"} %s])' % parms

        print cmd
        erl(cmd)

class Vocab(Vocabulary):
    def __init__(self):
	self.ns = 'http://recipy.hoverview.org/erlang'
        self.elms = {
            'edoc': Edoc,
            'beamfiles': Beamfiles,
            'eunit-reports': Eunit,
            'includes':Includes,
            'codepathprefix': CodePathPrefix,
            'codepathsuffix': CodePathSuffix,
            'flags': Flags,
            'escript-archive': Escript
        }

    def check_deps(self):
        self.unmet = None
