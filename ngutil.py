#!/usr/bin/env python
import argparse
import os, sys
import subprocess

SITES_ENAB_PATH='/etc/nginx/sites-enabled/'
SITES_AVAIL_PATH='/etc/nginx/sites-available/'

parser = argparse.ArgumentParser()
parser.add_argument("-e", "--enable", help="enable site")
parser.add_argument("-d", "--disable", help="disable site")
parser.add_argument("-s", "--service", help="change service state", choices="start|stop|restart|reload|force-reload|status|configtest")
args = parser.parse_args()

def enable_site(sitename):
    full_site_path = os.path.join(SITES_AVAIL_PATH, sitename)
    if os.path.exists(full_site_path):
        os.chdir(SITES_ENAB_PATH)
        try:
            os.symlink(full_site_path, sitename)
        except OSError, e:
            print "site %s is enabled" % sitename
        else:
            make_nginx()

        list_all_sites()
        return True
    else:
        print "site %s is not exists" % sitename
        return False

def disable_site(sitename):
    full_site_path = os.path.join(SITES_ENAB_PATH, sitename)
    if os.path.exists(full_site_path):
        os.remove(full_site_path)
        make_nginx()
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

def make_nginx(action="restart"):
    os.system("service nginx %s" % action)


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

        elif args.service:
            make_nginx(args.service)

        else:
            print "All site status:"
            list_all_sites()
