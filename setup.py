# Copyright (c) Deeproute.ai. All rights reserved.


import os
import subprocess
import time
from datetime import datetime as dt
from pathlib import Path
from typing import Union

from setuptools import find_packages, setup


def readme():
    with open('README.md', encoding='utf-8') as f:
        content = f.read()
    return content


package_name = 'template'
version_file = '{}/version.py'.format(package_name)



def write_version_py(tag, hotfix):
    content = """# GENERATED VERSION FILE
# TIME: {}

__version__ = '{}'
short_version = '{}'
version_info = ({})
"""
    with open('{}/VERSION'.format(package_name)) as f:
        SHORT_VERSION = f.read().strip()
    VERSION_INFO = ', '.join(SHORT_VERSION.split('.'))
    VERSION = SHORT_VERSION
    if tag:
        VERSION = VERSION + '+' + tag
    if hotfix:
        assert "rc" in hotfix, "hotfix must contain `rc`"
        VERSION = VERSION + "." + hotfix

    version_file_str = content.format(
        time.asctime(), VERSION, SHORT_VERSION,
        VERSION_INFO,
    )
    with open(version_file, 'w') as f:
        f.write(version_file_str)


def get_version():
    with open(version_file, 'r') as f:
        exec(compile(f.read(), version_file, 'exec'))
    import sys
    version = locals()["__version__"]
    return version


def parse_requirements(fname='requirements.txt', with_version=True):
    """Parse the package dependencies listed in a requirements file but strips
    specific versioning information.

    Args:
        fname (str): path to requirements file
        with_version (bool, default=False): if True include version specs

    Returns:
        list[str]: list of requirements items

    CommandLine:
        python -c "import setup; print(setup.parse_requirements())"
    """
    import re
    import sys
    from os.path import exists
    require_fpath = fname

    def parse_line(line):
        """Parse information from a line in a requirements text file."""
        if line.startswith('-r '):
            # Allow specifying requirements in other files
            target = line.split(' ')[1]
            for info in parse_require_file(target):
                yield info
        else:
            info = {'line': line}
            if line.startswith('-e '):
                info['package'] = line.split('#egg=')[1]
            else:
                # Remove versioning from the package
                pat = '(' + '|'.join(['>=', '==', '>']) + ')'
                parts = re.split(pat, line, maxsplit=1)
                parts = [p.strip() for p in parts]

                info['package'] = parts[0]
                if len(parts) > 1:
                    op, rest = parts[1:]
                    if ';' in rest:
                        # Handle platform specific dependencies
                        # http://setuptools.readthedocs.io/en/latest/setuptools.html#declaring-platform-specific-dependencies  # noqa
                        version, platform_deps = map(str.strip,
                                                     rest.split(';'))
                        info['platform_deps'] = platform_deps
                    else:
                        version = rest  # NOQA
                    info['version'] = (op, version)
            yield info

    def parse_require_file(fpath):
        with open(fpath, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if line and not line.startswith('#'):
                    for info in parse_line(line):
                        yield info

    def gen_packages_items():
        if exists(require_fpath):
            for info in parse_require_file(require_fpath):
                parts = [info['package']]
                if with_version and 'version' in info:
                    parts.extend(info['version'])
                if not sys.version.startswith('3.4'):
                    # apparently package_deps are broken in 3.4
                    platform_deps = info.get('platform_deps')
                    if platform_deps is not None:
                        parts.append(';' + platform_deps)
                item = ''.join(parts)
                yield item

    packages = list(gen_packages_items())
    return packages


if __name__ == '__main__':
    write_version_py(None, None)
    setup(
        name='my-custom-template',
        version=get_version(),
        description=('python-template.'),
        long_description=readme(),
        long_description_content_type='text/markdown',
        author='lichar',
        author_email='ylc0003@gmail.com',
        keywords='python template',
        packages=find_packages(exclude=('tests*', '__pycache__*')),
        include_package_data=True,
        # entry_points={
        #     "console_scripts": [
        #         "test = test.api:main"
        #         ],
        # },
        scripts=[],
        classifiers=[
            'Development Status :: 4 - Beta',
            'License :: OSI Approved :: Apache Software License',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
        ],
        license='',
        install_requires=parse_requirements('requirements/requirements.txt'),
        extras_require={},
        ext_modules=[],
        zip_safe=False)
