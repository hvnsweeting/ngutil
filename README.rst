ngutil
======

nginx util, enable - disable sites

Usage
-----

set ngutil.py executable::

    chmod a+x ngutil.py

run it::

    root@u1210: # ./ngutil.py -h
    usage: ngutil.py [-h] [-e ENABLE] [-d DISABLE]

    optional arguments:
      -h, --help            show this help message and exit
      -e ENABLE, --enable ENABLE
                            enable site
      -d DISABLE, --disable DISABLE
                            disable site

list sites::

    root@u1210: # ./ngutil.py 
    All site status:
    default ---------- enabled

disable::

    root@u1210: # ./ngutil.py -d default
    disabling default
    Restarting nginx: nginx.
    default ---------- disabled

enable::

    root@u1210: # ./ngutil.py -e default
    enabling default
    Restarting nginx: nginx.
    default ---------- enabled

create reverse-proxy config::

    hvn@u1210: $ sudo ./ngutil.py -n dantri.com -t 10.0.0.2
    Created config file /etc/nginx/sites-available/dantri.com
