from setuptools import setup

if __name__ == '__main__':
    setup(
        name='encoder',
        version='1.0',
        description='Custom and extensible base 64 encoding and decoding utility',
        author='Andrew Cumming',
        author_email='andrew.e.cumming@gmail.com',
        url='https://github.com/AndrewEC/python-base64-encoder',
        packages=['encoder', 'encoder.lib'],
        install_requires=[
            'Click==8.0.4'
        ]
    )
