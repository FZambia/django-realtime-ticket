import sys
import platform
from distutils import log
from distutils.core import setup


requires = ["django>=1.3.1", "redis>=2.6.0"]


# PyPy and setuptools don't get along too well, yet.
if sys.subversion[0].lower().startswith('pypy'):
    from distutils.core import setup
    extra = dict(requires=requires)
else:
    from setuptools import setup
    extra = dict(install_requires=requires)


setup(
    name="django-realtime-ticket",
    version="0.1.0",
    author="Alexandr Emelin",
    author_email="frvzmb@gmail.com",
    url="https://github.com/FZambia/django-realtime-ticket",
    license="http://www.apache.org/licenses/LICENSE-2.0",
    description="authorize django users in realtime(asynchronous) backends using expiring tickets in Redis",
    keywords="python django realtime asynchronous async ticket redis authorization",
    packages=["realtime_ticket", ],
    package_data={},
    **extra
)
