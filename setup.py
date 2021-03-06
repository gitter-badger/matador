from setuptools import setup, find_packages

# Work around mbcs bug in distutils.
# http://bugs.python.org/issue10945
import codecs
try:
    codecs.lookup('mbcs')
except LookupError:
    ascii = codecs.lookup('ascii')
    func = lambda name, enc=ascii: {True: enc}.get(name=='mbcs')
    codecs.register(func)

setup(
    name='Matador',
    version='1.5.0',
    author='Owen Campbell',
    author_email='owen.campbell@empiria.co.uk',
    entry_points={
        'console_scripts': [
            'matador = matador.management:execute_command',
        ],
    },
    options={
        'build_scripts': {
            'executable': '/usr/bin/env python3',
        },
    },
    url='http://www.empiria.co.uk',
    packages=find_packages(),
    install_requires=['pyyaml', 'dulwich'],
    license='The MIT License (MIT)',
    description='Change management for Agresso systems',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English'
        ]
    )
