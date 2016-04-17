from setuptools import setup, find_packages


__version__ = "0.0.1"

description = "A buildout recipe to create .deb packages"

setup(
    name='vdt.recipe.debian',
    version=__version__,
    description=description,
    long_description=description,
    classifiers=[
        "Framework :: Buildout",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='',
    author='Martijn Jacobs',
    author_email='martijn@devopsconsulting.nl',
    url='https://github.com/devopsconsulting/vdt.recipe.debian',
    license='',
    # include all packages in the egg, except the test package.
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    # for avoiding conflict have one namespace for all apc related eggs.
    namespace_packages=['vdt', 'vdt.recipe'],
    # include non python files
    include_package_data=True,
    zip_safe=False,
    # specify dependencies
    install_requires=[
        'setuptools',
        'zc.buildout',
        'vdt.versionplugin.buildout>=0.0.2'
    ],
    # mark test target to require extras.
    extras_require={
        'test': [
        ]
    },
    # generate scripts
    entry_points={
        'console_scripts': ['debianize = vdt.recipe.debian.debianize:debianize'],  # noqs
        'zc.buildout': ['default = vdt.recipe.debian.config:CreateConfig']
    },

)
