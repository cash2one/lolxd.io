from setuptools import setup

setup(
      name='lolxd',
      version='0',
      license='MIT',
      description='League of Legends live match statistics',
      author='Mads Damgaard Pedersen',
      author_email='?',
      maintainer='Carl Bordum Hansen',
      maintainer_email='carl@bordum.dk',
      url='https://github.com/damgaard22/lolxd.io.git',
      install_requires=[
            'Flask>=0.12',
            'requests>=2.13.0'
      ]
)
