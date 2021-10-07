# https://www.youtube.com/watch?v=F5a8RLY2N8M&list=PL1_riyn9sOjcKIAYzo7f8drxD-Yg9La-D&index=61
# Generic colorama demo using command line arguments
# By George Ogden
from colorama import Fore, Back, Style, init
import argparse
parser = argparse.ArgumentParser("colorama demo")

def format(module):
    return list(map(lambda x: x.lower(),module.__dict__.keys()))

def find(module,item):
    return module.__dict__[item.upper()]

parser.add_argument("-c","--colour",choices=format(Fore),default="RESET")
parser.add_argument("-b","--background",choices=format(Back),default="RESET")
parser.add_argument("-s","--style",choices=format(Style),default="RESET_ALL")
parser.add_argument("-t","--text",default="Lorem ipsum dolor sit amet")

args = parser.parse_args()

print(find(Style,args.style) + find(Fore,args.colour) + find(Back,args.background) + args.text + Style.RESET_ALL)