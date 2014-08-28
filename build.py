"""
.. build.py

Building the GitHub page for DiceRV.
"""

import jinja2


with open('index.html.tpl', 'r') as tpl_file:
    tpl = tpl_file.read()


template = jinja2.Template(tpl)


data = {}
data['author'] = "Peleg Michaeli"
data['intro'] = "Hi. This is the github page of the DiceRV project"
data['title'] = "DiceRV"


data['baseurl'] = '/dicerv'
data['github_url'] = 'http://github.com/pelegm/dicerv'


html = template.render(**data)


with open('index.html', 'w') as html_file:
    html_file.write(html)

