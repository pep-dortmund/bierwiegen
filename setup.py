from setuptools import setup

setup(
    name='bierwiegen',
    version='0.0.1',
    authors='Sascha Dungs, Maximilian Noethe',
    py_modules=[
        'bierwiegen',
    ],
    install_requires=[
        'PyQt5',
        'RPi.GPIO',
    ],
    entry_points={
        'gui_scripts': [
            'bierwiegen = bierwiegen:main',
        ]
    }
)
