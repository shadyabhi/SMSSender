#!/usr/bin/python2

import sys
from ConfigParser import *
from getpass import getpass

c = ConfigParser()

f = open(".creds","a")

section_name = raw_input("Enter site name: ")
c.add_section(section_name)

username = raw_input("Enter username: ")
password = getpass()

c.set(section_name, "username", username)
c.set(section_name, "password", password)

c.write(f)
f.close()
