#!/usr/bin/env python
import sys
import subprocess

subprocess.call("ls -l", shell=True)

target = raw_input("Enter an IP or Host to ping:\n")

host = subprocess.Popen(['host', target], stdout = subprocess.PIPE).communicate()[0]

print host