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
#parser.add_argument("-r", "--rproxy", help="create rproxy config")
parser.add_argument("-p", "--port")
parser.add_argument("-n", "--server_name")
parser.add_argument("-t", "--pass_to")

args = parser.parse_args()


def create_rproxy_config(server_name, pass_to, port=80):
    filepath = os.path.join(SITES_AVAIL_PATH, server_name)
    with open(filepath, 'wt') as f:
        TEMPLATE= """server {
        listen      %s;
        server_name  %s;
        access_log  /var/log/nginx/%s.log;
        error_log  /var/log/nginx/%s.error.log;
        root   /usr/share/nginx/html;
        index  index.html index.htm;

        location / {
                proxy_pass  http://%s;
                proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;
                proxy_redirect off;
                proxy_buffering off;
                proxy_set_header        Host            $host;
                proxy_set_header        X-Real-IP       $remote_addr;
                proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
        }
}
""" % (port, server_name, server_name, server_name, pass_to)
        f.write(TEMPLATE)
        return filepath
        

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

def main():
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

        elif args.pass_to and args.server_name:
            if not args.port:
                args.port = 80
            fpath = create_rproxy_config(args.server_name, args.pass_to, args.port)

            print "Created config file %s" % fpath
        else:
            print "All site status:"
            list_all_sites()


def test():
    create_rproxy_config("cacti.vccloud.vn", "10.0.0.20")


if __name__ == "__main__":
    main()
