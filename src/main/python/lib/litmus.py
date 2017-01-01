
from xml.dom.minidom import parse

def firstChild(elm, name):
    children = elm.getElementsByTagName(name)
    if children:
        return children[0].firstChild.data
    return None

class Test:
    def __init__(self, elm):
        self.synopsis = firstChild(elm, 'synopsis')
        self.action = firstChild(elm, 'action')
        self.facit = firstChild(elm, 'facit')

class Campaign:
    def __init__(self, file):
        dom = parse(file)
        self.tests = []
        testelms = dom.getElementsByTagName('test')
        for testelm in testelms:
            self.tests.append(Test(testelm))
        
        
if __name__ == '__main__':
    #tests
    cam = Campaign('src/test/litmus/testcampaign.xml')
    assert hasattr(cam, 'tests'), 'No tests property in campaign'
    exp = [
        ['First synopsis', 'first_action(),', 'FIRSTFACIT'],
        ['Second synopsis', 'second_action(),', 'SECONDFACIT']
        ]
    i = 0
    for t in exp:
        assert exp[i][0] == cam.tests[i].synopsis
        assert exp[i][1] == cam.tests[i].action
        assert exp[i][2] == cam.tests[i].facit
        i = i+1
        
        
        
