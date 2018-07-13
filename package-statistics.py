#!/usr/bin/env python3

import urllib.request
import gzip
import collections
import argparse
import sys

URL_TEMPLATE = 'http://ftp.uk.debian.org/debian/dists/stable/main/Contents-{}.gz'
TOP_N = 10


def perror(s):
    """Print arguments on stderr"""
    print(s, file=sys.stderr)


def top_packages(arch, n):
    """Returns the top n packages with the most number of files.

    @param arch: The distro architecture
    @param n: Top N packages
    @return: an ordered list of tuples of the form ('package', count)
    """

    try:
        counts = collections.defaultdict(int)
        r = urllib.request.urlopen(URL_TEMPLATE.format(arch))
        f = gzip.GzipFile(fileobj=r)

        for l in f:             # flake8: noqa
            l = l.decode().strip()
            # Split from rightmost to handle filenames with spaces in them
            # package names and sections cannot have spaces
            (fname, pkgs) = l.rsplit(maxsplit=1)
            # When the same file is present in more than one package
            # it is a comma separated list like below
            # bin/busybox        utils/busybox,shells/busybox-static
            for p in pkgs.split(','):
                counts[p.split('/')[-1]] += 1
    except (ValueError, UnicodeDecodeError, TypeError) as e:
        perror("Could not parse line: {}".format(l))
        sys.exit(1)
    except urllib.error.HTTPError as e:
        perror("Could not download {}: {}".format(URL_TEMPLATE.format(arch), e))
        sys.exit(2)

    return sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:n]


def format_list(tuples):
    """Formats a table of counts

    @param tuples: list of tuples of the form ('package', count)

    TODO: truncate package name to fit in allocated space
    """

    try:
        linenum = 1
        for pkg in tuples:
            print('{:>3}. {:<30}{:>5}'.format(linenum, *pkg))
            linenum += 1
    except TypeError as e:
        perror("Could not understand {}".format(pkg))
        sys.exit(3)


#
# Start here

known_archs = ['amd64', 'arm64', 'armel', 'armhf', 'i386',
               'mips', 'mipsel', 'mips64el', 'ppc64el', 's390x']
p = argparse.ArgumentParser(description='Show top {} packages with the most files'.format(TOP_N))
p.add_argument('arch', choices=known_archs, help='Architecture to be used')
args = p.parse_args()

pkgs = top_packages(args.arch, TOP_N)
format_list(pkgs)
