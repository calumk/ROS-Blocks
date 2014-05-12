#!/usr/bin/python
import webbrowser as wb
import argparse
import os
parser = argparse.ArgumentParser()
parser.add_argument("--f")
args = parser.parse_args()

path = os.path.dirname(os.path.realpath(__file__))

if args.f:
	wb.open_new("file://"+path+"/ros_blocks_designer/index.html#"+args.f)
else:
	wb.open_new("file://"+path+"/ros_blocks_designer/index.html")