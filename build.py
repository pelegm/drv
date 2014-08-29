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
    def __init__(self, name, code, figure=None):
        self.name = name
        self.code = code
        self.figure = figure

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


examples = ['3d6', 'risk']


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
        code = ""
        kwargs = {}
        for line in tds[1:]:
            if line[:2] == "#:":
                key, value = line[3:].split("::")
                kwargs[key] = value
            else:
                code += line + "\n"
        tests.append(Test(test_name, code, **kwargs))
    example  = Example(example_name, example_intro, *tests)

    example.run()
    data = dict(example=example)
    html = template.render(**data)
    with open('examples/{}.html'.format(example.name), 'w') as example_file:
        print "Writing {}".format(example_file.name)
        example_file.write(html)

