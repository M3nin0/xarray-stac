import os
from setuptools import find_packages, setup

readme = open('README.rst').read()
history = open('CHANGES.rst').read()

docs_require = [
]

tests_require = []

extras_require = {
}
extras_require['all'] = [req for exts, reqs in extras_require.items() for req in reqs]

setup_requires = [
]

install_requires = [
    'xarray',
    'stac.py',
    'pandas'
]

packages = find_packages()

g = {}
with open(os.path.join('xarray_stac', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='xarray_stac',
    version=version,
    description=__doc__,
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/x-rst',
    keywords=['STAC', 'datacube', 'xarray'],
    license='MIT',
    author='Felipe Carlos',
    author_email='felipe.carlos@inpe.br',
    url='https://github.com/M3nin0/xarray-stac',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Console :: Curses  ',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
)
