from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='ruconlluconv',
    version='1.1.0',
    description='Converter from different russian POS datasets to CoNLL-U format',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/shkarupa-alex/ruconlluconv',
    author='Shkarupa Alex',
    author_email='shkarupa.alex@gmail.com',
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'ruconlluconv-gicr=ruconlluconv.gicr:main',
            'ruconlluconv-oc=ruconlluconv.oc:main',
            'ruconlluconv-rnc=ruconlluconv.rnc:main',
            'ruconlluconv-slr=ruconlluconv.slr:main',
            'ruconlluconv-str=ruconlluconv.str:main',

            'ruconlluconv-space-dataset=ruconlluconv.space.dataset:main',
            'ruconlluconv-space-vocab=ruconlluconv.space.vocab:main',
            'ruconlluconv-space-train=ruconlluconv.space.train:main',
            'ruconlluconv-space-predict=ruconlluconv.space.predict:main',
        ],
    },
    install_requires=[
        'conllu>=1.2.1',
    ],
    test_suite='nose.collector',
    tests_require=[
        'nose',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
