"""Install Rendor."""

from setuptools import setup

from io import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='rendor',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    description='Make static website from a bunch of markdown files',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/kvas-it/rendor',
    author='Vasily Kuznetsov',
    author_email='kvas.it@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: Markup :: Markdown',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='static site generator, markdown',
    py_modules=['rendor'],
    install_requires=[
        'jinja2',
        'markdown',
    ],
    extras_require={
        'dev': [
            'flake8',
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'rendor=rendor:main',
        ],
    },
)
