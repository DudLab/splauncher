from __future__ import print_function


__author__ = "John Kirkham <kirkhamj@janelia.hhmi.org>"
__date__ = "$May 18, 2015 22:08:21 EDT$"


import os
import shutil
import subprocess
import sys
import tempfile
import time

from splauncher.core import main


class TestCore(object):
    def setup(self):
        self.cwd = os.getcwd()
        self.tempdir = ""
        self.tempdir = tempfile.mkdtemp()
        os.chdir(self.tempdir)

    def teardown(self):
        os.chdir(self.cwd)
        shutil.rmtree(self.tempdir)
        self.tempdir = ""
        self.cwd = ""

    def test_main_0(self):
        main("echo", "output")

        time.sleep(50.0)

        filenames = []
        for each_filename in os.listdir(self.tempdir):
            filenames.append(os.path.join(self.tempdir, each_filename))

        process = subprocess.Popen(
            ["qstat"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        process.wait()
        print(process.stdout.read(), file=sys.stdout)
        print(process.stderr.read(), file=sys.stderr)

        assert ".err" in filenames[0]
        assert ".out" in filenames[1]

        with open(filenames[0], "r") as f:
            s = f.read().strip()
            print("File \"%s\" contains \"%s\"." % (f.name, s))
            assert s == ""

        with open(filenames[1], "r") as f:
            s = f.read().strip()
            print("File \"%s\" contains \"%s\"." % (f.name, s))
            assert s == "output"

    def test_main_1(self):
        main("echo", "error", "1>&2")

        time.sleep(50.0)

        filenames = []
        for each_filename in os.listdir(self.tempdir):
            filenames.append(os.path.join(self.tempdir, each_filename))

        process = subprocess.Popen(
            ["qstat"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        process.wait()
        print(process.stdout.read(), file=sys.stdout)
        print(process.stderr.read(), file=sys.stderr)

        with open(filenames[0], "r") as f:
            s = f.read().strip()
            print("File \"%s\" contains \"%s\"." % (f.name, s))
            assert s == "error"

        with open(filenames[1], "r") as f:
            s = f.read().strip()
            print("File \"%s\" contains \"%s\"." % (f.name, s))
            assert s == ""
