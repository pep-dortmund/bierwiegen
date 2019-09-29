from setuptools import setup

setup(
    name='bierwiegen',
    version='0.0.1',
    authors='Sascha Dungs, Maximilian Noethe',
    packages=[
        'bierwiegen',
    ],
    install_requires=[
        'RPi.GPIO',
        'pyyaml',
    ],
    entry_points={
        'gui_scripts': [
            'bierwiegen = bierwiegen.__main__:main',
        ]
    },
    package_data={'': ['resources/*']},
)
