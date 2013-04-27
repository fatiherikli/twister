from distutils.core import setup

setup(name='Twister',
      version='0.2',
      description='Websocket PUB/SUB implementation',
      author='Fatih Erikli',
      author_email='fatiherikli@gmail.com',
      url='https://github.com/fatiherikli/twister',
      packages=['twister'],
      install_requires=[
          'ws4py==0.3.0-beta',
          'gevent==0.13.8',
      ]
)
