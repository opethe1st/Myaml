from setuptools import (
    setup,
    find_packages,
)

setup(
    name='myaml',
    version='0.0.1',
    description="Minimal yaml",
    url='http://github.com/opethe1st/myaml',
    author='Opemipo Ogunkola (Ope)',
    author_email='ogunks900@gmail.com',
    license='MIT',
    packages=find_packages(where=".", exclude=["tests"]),
    zip_safe=False
)
