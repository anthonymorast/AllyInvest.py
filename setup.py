from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='AllyInvestPy',
    version='1.0.1',
    description='A blackbox Ally Invest/TradeKing API interface for application developers.',
    url='https://github.com/anthonymorast/AllyInvest.py',
    author='Anthony Morast',
    author_email='anthony.a.morast@gmail.com',
    license='MIT',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        'requests',
        'requests_oauthlib',
    ]
)
