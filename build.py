"""
.. build.py

Building the GitHub page for DiceRV.
"""

import jinja2 as j2
import StringIO
import sys


############################
## ----- Jinja Init ----- ##
############################

env = j2.Environment(extensions=['jinja2_highlight.HighlightExtension'])
env.loader = j2.FileSystemLoader('templates/')


##########################
## ----- Examples ----- ##
##########################

class Test(object):
    def __init__(self, name, code):
        self.name = name
        self.code = code

    def run(self):
        _code_out = StringIO.StringIO()
        sys.stdout = _code_out
        exec self.code
        self.output = _code_out.getvalue()
        sys.stdout = sys.__stdout__


class Example(object):
    def __init__(self, name, intro, *tests):
        self.name = name
        self.intro = intro
        self.tests = tests


    def run(self):
        for test in self.tests:
            test.run()


examples = []
_3d6_mean = Test('3d6 mean', code="""
import drv.game.base
dice = drv.game.base.ndk(3, 6)
print dice.mean
""")
_3d6_std = Test('3d6 standard deviation', code="""
import drv.game.base
dice = drv.game.base.ndk(3, 6)
print dice.std
""")
_3d6_intro = "Rolling three 6-sided dice, checking the results."
_3d6 = Example('3d6', _3d6_intro, _3d6_mean, _3d6_std)
examples = [_3d6]


template = env.get_template('index.html')


data = {}
data['author'] = "Peleg Michaeli"
data['intro'] = "Hi. This is the github page of the DiceRV project"
data['title'] = "DiceRV"


data['baseurl'] = '/dicerv'
data['github_url'] = 'http://github.com/pelegm/dicerv'


html = template.render(**data)


with open('index.html', 'w') as html_file:
    print "Writing {}".format('index.html')
    html_file.write(html)


examples = ['3d6']


template = env.get_template('example.html')
for example_name in examples:
    test_filename = 'tests/{}.py'.format(example_name)
    with open(test_filename, 'r') as test_file:
        test_data = test_file.read()
    test_datas = test_data.split("#####\n")
    example_intro = test_datas[0][3:].strip()
    tests = []
    for td in test_datas[1:]:
        tds = td.split("\n")
        test_name = tds[0][3:].strip()
        code = "\n".join(tds[1:])
        tests.append(Test(test_name, code))
    example  = Example(example_name, example_intro, *tests)

    example.run()
    data = dict(example=example)
    html = template.render(**data)
    with open('examples/{}.html'.format(example.name), 'w') as example_file:
        print "Writing {}".format(example_file.name)
        example_file.write(html)

