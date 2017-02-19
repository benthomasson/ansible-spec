from setuptools import setup, find_packages
from pip.req import parse_requirements

import spec

install_reqs = parse_requirements('requirements.txt', session=False)
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='ansible-spec',
    version=spec.__version__,
    packages=find_packages(include='spec.*'),
    include_package_data=True,
    url='https://github.com/privateip/ansible-spec',
    license='GPLv3 (See LICENSE file for terms)',
    author='Peter Sprygada',
    author_email='psprygada@ansible.com',
    description=('Ansible Spec shortcuts ansible module creation using spec files'),
    entry_points={
        'console_scripts': ['ansible-spec = spec.cli:commandline']
    },
    install_requires=reqs
)
