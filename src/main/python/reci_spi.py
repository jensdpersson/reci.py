
#Vocabulary - a factory for elements, identified by a namespace.
class Vocabulary:
    def reg(self, ns):
	vocabs[ns] = self

    def resolve(self, localname):
        elm = self.elms.get(localname)
        if elm:
            return elm()
        return None

    def check_deps(self):
        self.unmet = None

class Directive:
    def __init__(self):
        self.subs = []
        self.parent = None
        self._project = None
        self._target = None

    def realize(self, intodir):
        raise Exception("realize method must be overridden in " + str(self))

    def add(self, sub):
        self.subs.append(sub)
        sub.parent = self

    def subrealize(self, todir):
        for sub in self.subs:
            sub.realize(todir)
