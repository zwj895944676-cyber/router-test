# -*- coding:utf-8 -*-
"""
将csv的数据转为可用的list列表，元素为字符串
"""

import csv

def csv_read(path):
    f = open("data/data.csv", encoding="utf-8")
    reader = csv.reader(f)
    return list(reader)[1:]