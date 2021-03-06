import re
try:
    import readline
except:
    pass
import urllib2
import json
import ssl
import os
import datetime
import itertools
#import trace
#import pdb
import random
import threading
import Queue
from collections import namedtuple
import interfaces.switchpreviewutil as switchpreviewutil
from localutils.custom_utils import *
import logging

# Create a custom logger
# Allows logging to state detailed info such as module where code is running and 
# specifiy logging levels for file vs console.  Set default level to DEBUG to allow more
# grainular logging levels
logger = logging.getLogger('aciops.' + __name__)

def local_interface_menu():
    while True:
        print("\nSelect type of interface(s): \n\n" + \
          "\t1.) PC Interfaces: \n" + \
          "\t2.) VPC Interfaces: \n")
        selection = custom_raw_input("Select number: ")
        print('\r')
        if selection.isdigit() and selection != '' and 1 <= int(selection) <= 3:
            break
        else:
            continue
    return selection 

class pcAggrIf():
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def main(import_apic,import_cookie):
    while True:
        global apic
        global cookie
        cookie = import_cookie
        apic = import_apic
        allpclist = get_All_PCs(apic,cookie)
        allvpclist = get_All_vPCs(apic,cookie)
        clear_screen()
        location_banner('Show port-channel locations')

        selection = local_interface_menu()
        if selection == '1':
            interfacelist = port_channel_selection(allpclist)
            all_locations = port_channel_location(interfacelist[0].name,apic,cookie)
            print("{}".format('\nPort-Channel Location:'))
            print('{}'.format('-'*22))
            for locations in sorted(all_locations):
                print(" \x1b[1;33;40m{} : {}\x1b[0m".format(', '.join(locations[:1]), ', '.join(locations[1])))

            custom_raw_input('\nPress Enter to Coninue...')
        elif selection == '2':
            interfacelist = port_channel_selection(allvpclist)
            all_locations = port_channel_location(interfacelist[0].name,apic,cookie)
            print(" {}".format('\nPort-Channel Location:'))
            print('{}'.format('-'*22))
            for locations in sorted(all_locations):
                print(" \x1b[1;33;40m{} : {}\x1b[0m".format(', '.join(locations[:1]), ', '.join(locations[1])))
            custom_raw_input('\nPress Enter to Coninue...')

            #import pdb; pdb.set_trace()



#url = """https://{apic}/api/class/pcAggrIf.json?query-target-filter=eq(pcAggrIf.name,"{pcname}")&rsp-subtree=full&rsp-subtree-class=pcRsMbrIfs"""