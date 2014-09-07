from distutils.core import setup


data = {}
data['author'] = "Peleg Michaeli"
data['name'] = "DRV"
data['version'] = '0.1.0dev'
data['packages'] = ['drv', 'drv.dice']
data['license'] = 'LICENSE'
data['long_description'] = open('README.txt', 'r').read()
data['url'] = "http://github.com/pelegm/drv"


setup(**data)

