#!/usr/bin/env python
import argparse
import os, sys
import subprocess

SITES_ENAB_PATH='/etc/nginx/sites-enabled/'
SITES_AVAIL_PATH='/etc/nginx/sites-available/'

parser = argparse.ArgumentParser()
parser.add_argument("-e", "--enable", help="enable site")
parser.add_argument("-d", "--disable", help="disable site")

args = parser.parse_args()

def enable_site(sitename):
    full_site_path = os.path.join(SITES_AVAIL_PATH, sitename)
    if os.path.exists(full_site_path):
        os.chdir(SITES_ENAB_PATH)
        os.symlink(full_site_path, sitename)
        restart_nginx()
        list_all_sites()
        return True
    else:
        print "site %s is not exists" % sitename
        return False

def disable_site(sitename):
    full_site_path = os.path.join(SITES_ENAB_PATH, sitename)
    if os.path.exists(full_site_path):
        os.remove(full_site_path)
        restart_nginx()
        list_all_sites()
        return True
    else:
        print "site %s is not exists" % sitename
        return False

def list_all_sites():
    ens = os.listdir(SITES_ENAB_PATH)
    avails = os.listdir(SITES_AVAIL_PATH)
    for f in avails:
        print f, '-' * 10,
        if f in ens:
            print "enabled"
        else:
            print "disabled"

    # list all site with status

def restart_nginx():
    os.system("service nginx restart")


if __name__ == "__main__":
    if os.geteuid() != 0:
        sys.exit("\nOnly root can run this script\n")
    else:
        if args.enable:
            print "enabling", args.enable
            sitename = args.enable
            enable_site(sitename)

        elif args.disable:
            print "disabling", args.disable
            sitename = args.disable
            disable_site(sitename)

        else:
            print "All site status:"
            list_all_sites()
