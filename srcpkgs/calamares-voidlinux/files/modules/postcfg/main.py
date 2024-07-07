#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# === This file is part of Calamares - <http://github.com/calamares> ===
#
#   Copyright 2014 - 2019, Philip Müller <philm@manjaro.org>
#   Copyright 2016, Artoo <artoo@manjaro.org>
#
#   Calamares is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Calamares is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Calamares. If not, see <http://www.gnu.org/licenses/>.

import libcalamares
import subprocess

from shutil import copy2
from distutils.dir_util import copy_tree
from os.path import join, exists
from libcalamares.utils import target_env_call
from libcalamares.utils import target_env_process_output
from libcalamares.utils import check_target_env_output

def pretty_name():
    return ("Misc post-install configurations")

status = ("Misc post-install configurations")

def pretty_status_message():
    return status

class ConfigController:
    def __init__(self):
        self.__root = libcalamares.globalstorage.value("rootMountPoint")

    @property
    def root(self):
        return self.__root

    def terminate(self, proc):
        target_env_call(['killall', '-9', proc])

    def copy_file(self, file):
        if exists("/" + file):
            copy2("/" + file, join(self.root, file))

    def copy_folder(self, source, target):
        if exists("/" + source):
            copy_tree("/" + source, join(self.root, target))

#    def remove_pkg(self, pkg):
#            libcalamares.utils.target_env_process_output(['xbps-remove', '-Ry', calamares-fvoid-2023.02.01_1])

    def umount(self, mp):
        subprocess.call(["umount", "-l", join(self.root, mp)])

    def mount(self, mp):
        subprocess.call(["mount", "-B", "/" + mp, join(self.root, mp)])

    def rmdir(self, dir):
        subprocess.call(["rm", "-Rf", join(self.root, dir)])

    def mkdir(self, dir):
        subprocess.call(["mkdir", "-p", join(self.root, dir)])

    def run(self):
        status = ("Removing CLI installer")
        if exists(join(self.root, "usr/sbin/void-installer")):
            libcalamares.utils.target_env_process_output(["rm", "-fv", "usr/sbin/void-installer"])

        status = ("Initializing package manager databases")
        if libcalamares.globalstorage.value("hasInternet"):
            libcalamares.utils.target_env_process_output(["xbps-install", "-Syy"])

        # Remove calamares
        status = ("Removing Calamares from target")
#        self.remove_pkg("calamares-fvoid-2023.02.01_1")
        if exists(join(self.root, "usr/share/applications/calamares.desktop")):
            target_env_call(["rm", "-fv", "usr/share/applications/calamares.desktop"])


        # Copy skel to root
        status = ("Copying skel to root")
        self.copy_folder('etc/skel', 'root')

        # Update grub.cfg
        status = ("Updating GRUB")
        if exists(join(self.root, "usr/bin/fixgrub")):
            libcalamares.utils.target_env_process_output(["fixgrub"])

        # Enable 'menu_auto_hide' when supported in grubenv
        if exists(join(self.root, "usr/bin/grub-set-bootflag")):
            target_env_call(["grub-editenv", "-", "set", "menu_auto_hide=1", "boot_success=1"])


        # Replace /etc/issue msg from live
        if exists(join(self.root, "etc/issue.new")):
            libcalamares.utils.target_env_process_output(["mv", "etc/issue.new", "etc/issue"])

        # Enable doas on target
        if exists(join(self.root, "usr/bin/doas")):
            doasconf = "permit nopass :root ||\npermit persist :wheel"
            with open(join(self.root, "etc/doas.conf"), 'w') as conf:
                conf.write(doasconf)


def run():
    """ Misc post-install configurations """

    config = ConfigController()

    return config.run()
