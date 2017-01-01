
import os
import os.path
from os.path import realpath
import sys

#Recursive Compilation Invocation in Python.
#Lightweight hatchfile variant.

#Core concepts.

#Loader - creates Recipe objects from recipe files

class Locator:
    def locate(self, project, target):
        return None

class RelativePathLocator(Locator):
    def __init__(self, pattern):
        self.pattern = pattern

    def locate(self, project, target):
        file = self.pattern % {'project':project, 'target':target}
        if os.path.exists(file):
            #print "Realizing artifact from recipe in " + file
            return file
        else:
            print "Recipe file not found as " + file
        return None

locator = RelativePathLocator("src/build/recipy/%(project)s-%(target)s.xml")

class Stack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self, expected=None):
        val = self.stack.pop()
        if expected and expected != val:
            raise Exception("Unexpected stack contents " + val)
        return val

    def peek(self):
        return self.stack[-1]


from reci_spi import Vocabulary
from reci_spi import Directive

class Wrapper(Directive):
    def realize(self, dir):
        self.subrealize(dir)
        return True

from xml import sax
import xml.sax.handler
class Loader(xml.sax.handler.ContentHandler):
    def __init__(self):
        self.prefixes = {}

    def load(self, filepath, project, target):
        self.stack = Stack()
        self.project = project
        self.target = target
        parser = sax.make_parser()
        parser.setContentHandler(self)
        parser.setFeature(xml.sax.handler.feature_namespaces, 1)
        self.stack.push(Wrapper())
        parser.parse(filepath)
        return self.stack.pop()

    def startPrefixMapping(self, prefix, uri):
        #print "vocabs " + str(vocabs)
        vocab = vocabs.get(uri)
        if vocab:
            self.prefixes[prefix] = vocab
        else:
            raise Exception("No vocabulary loaded for namespace " + uri)

    def endPrefixMapping(self, prefix):
        del self.prefixes[prefix]

    def startElementNS(self, (uri, localname), qname, attrs):
        #print "vocabs " + str(vocabs)
        vocab = vocabs.get(uri)
        if vocab:
            elm = vocab.resolve(localname)
            if not elm:
                raise Exception("No handler for element {%s:%s}" % (uri,localname))
            if vocab.unmet:
                raise Exception("Vocabulary for element {%s:%s} has unmet dependencies %s"\
                    % (uri,localname,vocab.unmet))
            self.stack.push(elm)
            elm._project = self.project
            elm._target = self.target
            for (aturi, atlocalname) in attrs.getNames():
                aqname = attrs.getQNameByName((aturi, atlocalname))
                getattr(elm, "set_" + atlocalname)(attrs.getValueByQName(aqname))
        else:
            raise Exception("No vocabulary loaded for namespace " + uri)

    def endElementNS(self, (uri, localname), qname):
 #       print "end " + localname
        elm = self.stack.pop()
        parent = self.stack.peek()
        #methodname = "add_" + localname
        #if hasattr(parent, methodname):
        #    getattr(parent, methodname)(elm)
        #else:
        parent.add(elm)

    def characters(self, characters):
    #    print "LIMSMNED " + characters
        elm = self.stack.peek()
        if hasattr(elm, "add_text"):
            elm.add_text(characters)

libdir = os.path.join(os.path.dirname(__file__),'lib')
sys.path.append(libdir)

vocabs = {}
#vocabmodules = ['default', 'erlang', 'xmlmacro', 'xml']
for vocabname in os.listdir(libdir):
    if vocabname.endswith('_vocab.py'):
        vocabname = vocabname[:-3]
    else:
        continue
    vocabmodule = __import__(vocabname)
    vocabobject = vocabmodule.Vocab()
    #print 'adding vocab ' + vocabobject.ns
    vocabobject.check_deps()
    if vocabobject.unmet:
        print "The vocabulary %s has unmet dependencies: %s"\
            % (vocabobject.ns, vocabobject.unmet)
    #print 'added vocab %s for ns %s' % (vocabobject, vocabobject.ns)
    vocabs[vocabobject.ns] = vocabobject
    #print 'added vocab %s for ns %s' % (vocabobject, vocabobject.ns)
    #print "vocabs " + str(vocabs)

loader = Loader()

def realize(project, target, rundir, todir):
    todir = os.path.abspath(todir)
    #print "reci.py(%s, %s, %s, %s)" % (project, target, rundir, todir)
    oldcwd = os.getcwd()
    #print "chdir " + rundir
    os.chdir(rundir)
    file = locator.locate(project, target)
    ok = False
    if(file):
        stream = open(file, "r")
        recipe = loader.load(stream, project, target)
        ok = recipe.realize(todir)
    #print "chdir " + oldcwd
    os.chdir(oldcwd)
    return ok
