from contextlib import contextmanager as _contextmanager
import os
from fabric.api import local, prefix, task
from fabric.context_managers import lcd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@_contextmanager
def virtualenv(bin_folder):
    """Activate virtual environment

    :param basestring bin_folder: Location of virtualenv /bin folder
    :return:
    """

    with prefix('source {}/bin/activate'.format(bin_folder)):
        yield


def get_virtual_env():
    """Return location of virtual environment

    :return:
    """

    for root, dir_names, file_names in os.walk(BASE_DIR):
        if all([i in dir_names for i in ['bin', 'include', 'lib']]):
            return os.path.join(BASE_DIR, root)


def get_os():
    """Return System platform

    :return:
    """

    return local('python -c "import platform; print platform.system()"', capture=True)


@task()
def update_requirements():
    """Update project python requirements

    :return:
    """

    virtual_env = get_virtual_env()

    if virtual_env:
        with virtualenv(virtual_env):
            with lcd(BASE_DIR):
                local('pip install -r requirements.txt')
                print 'Requirements installed'

    else:
        print 'Virtual environment needs to be installed first'
        print 'Please run `fab install_virtualenv` first'


def run_setup(command):
    """Run setup.py file

    :return:
    """

    virtual_env = get_virtual_env()

    if virtual_env:
        with virtualenv(virtual_env):
            with lcd(BASE_DIR):
                local('python setup.py {}'.format(str(command)))

    else:
        print 'Virtual environment needs to be installed first'
        print 'Please run `fab install_virtualenv` first'


@task()
def install():
    """Install project

    :return:
    """

    run_setup('install')


@task()
def develop():
    """Install project (develop mode)

    :return:
    """

    run_setup('develop')


@task()
def install_virtualenv():
    """Install python virtual environment

    :return:
    """

    virtual_env = get_virtual_env()

    if not virtual_env:
        with lcd(BASE_DIR):
            local('virtualenv -p /usr/bin/python2.7 venv')

        print "Virtual environment installed..."
        print "Usage: source {}/venv/bin/activate".format(BASE_DIR)

    else:
        print "Virtual environment already installed..."
        print "Usage: source {}/bin/activate".format(virtual_env)


@task()
def publish(version=None):

    if isinstance(version, basestring):

        with lcd(BASE_DIR):

            local("sed -i '' -E -- \"s/__version__ = '.*'/__version__ = '{}'/g\" sda/__init__.py".format(version))
            local('git add sda/__init__.py')
            local('git commit -m "PyPi release {}"'.format(version))
            local('git tag {0} -m "PyPi release {0}"'.format(version))
            local('git push --tags origin master')
            release = local('python setup.py sdist bdist_wheel upload -r "https://pypi.python.org/pypi"', capture=True)

            if '200' not in release:
                print "{} release failed...".format(version)

            else:
                print "{} released...".format(version)

    else:
        print 'Please include a version'
