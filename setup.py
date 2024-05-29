from setuptools import setup, find_packages

setup(
    name='crun',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'ansible==6.7.0',
        'ansible-core==2.13.13',
        'ansible-runner==2.3.6',
        'cffi==1.16.0',
        'cryptography==42.0.7',
        'docutils==0.20.1',
        'importlib-metadata==6.2.1',
        'Jinja2==3.1.4',
        'lockfile==0.12.2',
        'MarkupSafe==2.1.5',
        'packaging==24.0',
        'pexpect==4.9.0',
        'ptyprocess==0.7.0',
        'pycparser==2.22',
        'python-daemon==3.0.1',
        'PyYAML==6.0.1',
        'resolvelib==0.8.1',
        'six==1.16.0',
        'zipp==3.18.1',
        'click==8.1.7',
        'Pygments==2.18.0'

    ],
)

