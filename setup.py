#!/usr/bin/env python

import os, re

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

try:
    import jupyterhub_ceda_auth.__version__ as version
except ImportError:
    # If we get an import error, find the version string manually
    version = "unknown"
    with open(os.path.join(here, 'jupyterhub_ceda_auth', '__init__.py')) as f:
        for line in f:
            match = re.search('__version__ *= *[\'"](?P<version>.+)[\'"]', line)
            if match:
                version = match.group('version')
                break

with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

if __name__ == "__main__":
    setup(
        name = 'jupyterhub-ceda-auth',
        version = version,
        description = 'JupyterHub authenticator for CEDA accounts',
        long_description = README,
        classifiers = [
            "Programming Language :: Python",
            "Topic :: Internet :: WWW/HTTP",
            "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
        author = 'Matt Pryor',
        author_email = 'matt.pryor@stfc.ac.uk',
        url = 'https://github.com/cedadev/jupyterhub-ceda-auth',
        keywords = 'web jupyterhub ceda',
        packages = find_packages(),
        include_package_data = True,
        zip_safe = False,
        install_requires = [
            'oauthenticator',
        ],
    )
