import os
import sys
import re
from setuptools import setup, find_packages


if sys.version_info < (2, 7) or (3, 0) <= sys.version_info:
    print('Easy requires at Python 2.7 to run.')
    sys.exit(1)

with open('__init__.py') as f:
    version = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M).group(1)

if not version:
    raise RuntimeError('Cannot find Easy version information.')

with open('README.rst') as f:
    long_description = f.read()


def get_install_requires():
    requires = [
        'psutil>=5.4.3',
        'redis>=2.10.5',
        'Flask>=0.12.2',
        'celery>=4.1.0',
        'Flask_APScheduler>=1.7.0',
        'APScheduler>=3.3.1',
        'Flask_SocketIO>=2.9.2',
        'requests>=2.18.3',
        'pymongo>=3.4.0',
    ]
    return requires


setup(
    name='Easy',
    version=version,
    description="A http service monitoring tool for RentPlat Group",
    long_description=long_description,
    author='zhenxiang li',
    author_email='lizhenxiang@lianjia.com',
    url='http://git.lianjia.com/rent_plat/easy_http',
    license='LGPLv3',
    keywords="cli curses monitoring system",
    install_requires=get_install_requires(),
    extras_require={},
    # packages=['agent', 'alert', 'api', 'dash', 'schedule', 'task', 'utils'],
    packages=find_packages(),
    # package_data={'main': ['*.py', '*.sh']},
    include_package_data=True
)
