from setuptools import setup


dependencies = (
    'py2neo>3,<4',
)


setup(
    name='lazy_py2neo',
    version='2019.3.7',
    author='Bart Broere',
    email='mail@bartbroere.eu',
    py_modules=['lazy_py2neo'],
    install_requires=dependencies,
    description=open('README.md', 'r').read(),
)
