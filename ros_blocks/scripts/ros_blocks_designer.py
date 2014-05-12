#!/usr/bin/python

#    _____           _                       
#   |  __ \         (_)                      
#   | |  | | ___ ___ _  __ _ _ __   ___ _ __ 
#   | |  | |/ _ / __| |/ _` | '_ \ / _ | '__|
#   | |__| |  __\__ | | (_| | | | |  __| |   
#   |_____/ \___|___|_|\__, |_| |_|\___|_|   
#                       __/ |                
#                      |___/                 


# This script is used to launch the webbrowser

import webbrowser as wb
import argparse
import os

#argparse allows us to pass a variable to the script, in this case. The filename
parser = argparse.ArgumentParser()
parser.add_argument("--f")
args = parser.parse_args()

path = os.path.dirname(os.path.realpath(__file__))

if args.f:
	wb.open_new("file://"+path+"/ros_blocks_designer/index.html#"+args.f)
else:
	wb.open_new("file://"+path+"/ros_blocks_designer/index.html")