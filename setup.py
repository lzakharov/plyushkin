from setuptools import setup, find_packages

DESCRIPTION = '''
A command line application for dumping photos from your VK account.
'''.strip()

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='plyushkin',
    version='0.1.0',
    description=DESCRIPTION,
    long_description=readme,
    author='Lev Zakharov',
    author_email='l.j.zakharov@gmail.com',
    url='https://github.com/lzakharov/plyushkin',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    entry_points={
        'console_scripts': [
            'plyushkin = plyushkin.__main__:main'
        ]
    },
    install_requires=[
        'aiofiles',
        'aiohttp',
    ])
