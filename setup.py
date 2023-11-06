from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in yhen/__init__.py
from yhen import __version__ as version

setup(
	name="yhen",
	version=version,
	description="Yuehuan ERPNext",
	author="hyaray",
	author_email="hyaray@vip.qq.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
