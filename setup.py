from distutils.core import setup


data = {}
data['author'] = "Peleg Michaeli"
data['name'] = "DiceRV"
data['version'] = '0.1.0dev'
data['packages'] = ['drv', 'drv.game']
data['license'] = 'LICENSE'
data['long_description'] = open('README.txt', 'r').read()
data['url'] = "http://github.com/pelegm/dicerv"


setup(**data)

