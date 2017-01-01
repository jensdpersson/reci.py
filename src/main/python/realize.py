#!/usr/bin/env python

import os.path

class Realizer:
    def realize(self, artifact, todir):
        raise Exception("Must override Realizer.realize")

import reci_api
class RecipyBuilder(Realizer):
    def __init__(self, basedir):
        self.basedir = basedir

    def name(self):
        return "Reci.py builder"

    def realize(self, artifact, todir):
        path = os.path.join(self.basedir, artifact.project)
        #print "Looking for " + path
        if os.path.exists(path):
            return reci_api.realize(artifact.project, artifact.pkg, path, todir)
        else:
            return False

class Artifact:
    def __init__(self, spec):
        (self.org, self.project, self.pkg, self.min, self.max) = spec.split(':')
        self.spec = spec

    def realize(self, todir):
        ok = False
        for realizer in realizers:
            #print "Asking %s to realize artifact %s"\
            #    % (realizer.name(), self.spec)
            ok = realizer.realize(self, todir)
            if ok:
                return ok
        raise Exception("No realizer able to realize %s" % (self,))

    def __str__(self):
        return self.spec

realizers = [
             RecipyBuilder("..")

            #Hatchfile,
             #M2Pom,
             #IvyAntfile,
             #LocalFolder,
             #M2Repo,
             #Download
             ]
             #[realizers]
             # m2repo http...
             # gitrepo ssh:....
