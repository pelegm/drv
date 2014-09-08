from distutils.core import setup


data = {}
data['author'] = "Peleg Michaeli"
data['author_email'] = 'freepeleg@gmail.com'
data['name'] = "DRV"
data['version'] = '0.1.2dev'
data['packages'] = ['drv', 'drv.dice']
data['license'] = "UNLICENSE"
data['description'] = "Discrete random variables in Python made easy."
data['long_description'] = open('README.txt', 'r').read()
data['url'] = "http://github.com/pelegm/drv"
data['platforms'] = ["Linux"]
data['requires'] = ['numpy', 'scipy']


setup(**data)

