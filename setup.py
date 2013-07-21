from setuptools import setup, find_packages

try:
    long_description=open('README.rst', 'rt').read(),
except Exception:
    long_description=""

setup(
    name = "carnival",
    description = "a photo album",
    long_description=long_description,

    version = "0.1.0",
    author = 'Amit Upadhyay',
    author_email = "upadhyay@gmail.com",

    url = 'https://github.com/amitu/carnival/',
    license = 'BSD',

    install_requires = ["importd", "facebook-sdk", "tweepy"],
    packages = find_packages(),

    zip_safe = True
)