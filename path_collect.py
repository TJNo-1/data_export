#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from os import walk
import xlwt
import xlrd
from xlutils.copy import copy

def collect_path():
    data_path = raw_input('请输入要收集的路径信息\n')
    print(data_path)

collect_path()