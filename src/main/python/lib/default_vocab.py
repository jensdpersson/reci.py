
from reci_spi import Vocabulary
from reci_spi import Directive

import os

class Recipe(Directive):
    def set_artifact(self, artifact):
        self.artifact = artifact

    def set_project(self, project):
        self.project = project

    def realize(self, dir):
        self.subrealize(dir)

class Folder(Directive):
    def set_name(self, name):
        self.name = name

    def realize(self, dir):
        newdir = os.path.join(dir, self.name)
        if not os.path.exists(newdir):
            os.makedirs(newdir)
        self.subrealize(newdir)

import glob
import shutil

class Copies(Directive):
    def set_of(self, of):
        self.of = of
        self.files = glob.glob(of)

    def realize(self, dir):
        #print "Copy to "  + dir
        for file in self.files:
            self.copy(file, dir)

    def copy(self, src, dst):
        if os.path.isdir(src):
            for sub in os.listdir(src):
                src2 = os.path.join(src, sub)
                dst2 = os.path.join(dst, sub)
                if os.path.isdir(src2) and not os.path.exists(dst2):
             #       print "mkdir(%s)" % (dst2,)
                    os.mkdir(dst2)
                self.copy(src2, dst2)
        elif os.path.isfile(src):
            #print src + " -> " + dst
            shutil.copy(src, dst)

import realize
class Artifact(Directive):
    def __init__(self):
        Directive.__init__(self)
        self.project = ""
        self.name = ""
        self.min = ""
        self.max = ""
        self.org = ""

    def set_project(self, project):
        self.project = project

    def set_name(self, name):
        self.name = name

    def set_min(self, min):
        self.min = min

    def set_max(self, max):
        self.max = max

    def set_org(self, org):
        self.org = org

    def realize(self, dir):
        if not self.project:
            self.project = self._project
        spec = ":".join([self.org, self.project, self.name, self.min, self.max])
        artifact = realize.Artifact(spec)
        #print "Realizing %s in %s " % (spec, dir)
        artifact.realize(dir)

    def __str__(self):
        return self.spec


import tarfile
import tempfile
class Tarball(Directive):
    def set_name(self, name):
        self.name = name

    def realize(self, dir):
        tmp = tempfile.mkdtemp()
        self.subrealize(tmp)
        qname = os.path.join(dir, self.name)
        #print "Creating tarball %s" % (qname,)
        tarball = tarfile.open(qname, "w")
        for file in os.listdir(tmp):
            tarball.add(os.path.join(tmp, file), file)
        tarball.close()

    #def _filter(self, tarinfo):
import re
class IndexXml(Directive):

    def __init__(self):
        Directive.__init__(self)
        self.xslpi = None
        self.exclude = None

    def set_xslpi(self, xslpi):
        self.xslpi = xslpi

    def set_exclude(self, exclude):
        self.exclude = re.compile(exclude)

    def realize(self, dir):
        f = open(os.path.join(dir, 'index.xml'), 'w')
        if self.xslpi:
            f.write('<?xml-stylesheet href="%s" type="text/xsl"?>' % (self.xslpi,))
        f.write('<dir name="%s">\n' % (dir,))
        for file in os.listdir(dir):
            if file == 'index.xml':
                continue
            if self.exclude and self.exclude.search(file):
                continue
            path = os.path.join(dir, file)
            if os.path.isfile(path):
                f.write('<file name="%s"/>\n' % (file))
            elif os.path.isdir(path):
                f.write('<dir name="%s"/>\n' % (file))
        f.write('</dir>')

import urllib
from urlparse import urlparse
class Download(Directive):
    def __init__(self):
        Directive.__init__(self)
        self.uri = None

    def set_uri(self, uri):
        self.uri = uri

    def realize(self, dir):
        #TODO urllib.request.urlopen in py3
        #rsp = urllib2.urlopen(self.uri)
        name = None
        url = urlparse(self.uri)
        if url.path:
            name = url.path.split("/")[-1]
        else:
            raise "No name to give to downloaded file at " + self.uri
        #f = open(os.path.join(dir, name), "w")
        ok = urllib.urlretrieve(self.uri, os.path.join(dir, name))
        


class Vocab(Vocabulary):
    def __init__(self):
	self.ns = 'http://recipy.hoverview.org/default'
        self.elms = {
            'recipe': Recipe,
            'folder': Folder,
            'copies': Copies,
            'artifact': Artifact,
            'tarball': Tarball,
            'index-xml': IndexXml,
            'download': Download
        }
