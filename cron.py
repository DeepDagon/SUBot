#!./env1/bin/python3.5
# -*- coding: utf-8 -*-
from parse import parse_archive, checkComing
from glob import glob
from db import *

released = sorted(checkComing())
if released == []:
    print('0 updated')
    exit()
for i in released:
    parse_archive(i)

for i in range(released[-1], released[-1]+50):
    if getGameData(i) == []:
        parse_archive(i)

for i in glob("src/temp/*/"):
    i = int(i.split('/')[-2])
    parse_archive(i)
