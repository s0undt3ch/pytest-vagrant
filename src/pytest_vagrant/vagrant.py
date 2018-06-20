import pytest
import subprocess
import re
import os
import py

from ssh import SSH
from status import Status


@pytest.fixture
def vagrant():
    """ Creates the py.test fixture to make it usable withing the unit tests.
    See the Vagrant class for more information.
    """
    return Vagrant()

class Vagrant(object):
    """
    """
    def __init__(self):
        try:
            subprocess.check_output('vagrant validate', shell=True)
        except subprocess.CalledProcessError as e:
            print("Unable to validate vagrant file, are you sure it exists?")
            raise e

        if self.status.not_created:
            print "run up"
            self.up()
        elif not self.status.running:
            print "run resume"
            self.resume()

    @property
    def status(self):
        out = subprocess.check_output('vagrant status', shell=True)
        m = re.search(r'\w+\s+(.+)\s+\(.+\)', out)
        status_text = m.group(1)
        return Status(status_text)

    def ssh(self):
        if not self.status.running:
            raise RuntimeError("Vagrant machine not running")

        out = subprocess.check_output('vagrant ssh-config', shell=True)
        return SSH(out)

    def port(self):
        if not self.status.running:
            raise RuntimeError("Vagrant machine not running")
        out = subprocess.check_output('vagrant port', shell=True)
        matches = re.findall(r'(\d+) \(.*\)\s*=>\s*(\d+)\s*\(.*\)', out)
        return matches

    def provision(self):
        if self.status.not_created:
            raise RuntimeError("Vagrant machine not created")
        subprocess.check_output('vagrant provision', shell=True)

    def reload(self):
        if self.status.not_created:
            raise RuntimeError("Vagrant machine not created")
        subprocess.check_output('vagrant reload', shell=True)

    def resume(self):
        if self.status.not_created:
            raise RuntimeError("Vagrant machine not created")
        subprocess.check_output('vagrant resume', shell=True)

    def ssh_config(self):
        if self.status.not_created:
            raise RuntimeError("Vagrant machine not created")
        if not self.status.running:
            raise RuntimeError("Vagrant machine not running")
        subprocess.check_output('vagrant ssh-config', shell=True)

    def destroy(self):
        subprocess.check_output('vagrant destroy', shell=True)

    def halt(self):
        subprocess.check_output('vagrant halt', shell=True)

    def suspend(self):
        subprocess.check_output('vagrant suspend', shell=True)

    def up(self):
        subprocess.check_output('vagrant up', shell=True)

    def version(self):
        out = subprocess.check_output('vagrant version', shell=True)
        m = re.search('Installed Version: (\d+\.\d+\.\d+)', out)
        return m.group(1)