#!/usr/bin/env python
# -*- coding: utf-8 -*-

import instapaperlib
from clint.textui import progress, colored
import argparse
import getpass
import readability
import sys
import csv
import os


CURSOR_UP_ONE_AND_ERASE_LINE = '\x1b[1A\x1b[2K'


def unicode_dict_csv_read(utf8_data, **kwargs):
    csv_reader = csv.DictReader(utf8_data, **kwargs)
    for row in csv_reader:
        yield dict([(key, unicode(value, 'utf-8')) for key, value in row.iteritems()])


def main():
    try:
        # This script is meant only to run on a TTY
        assert sys.stdout.isatty() and sys.stdin.isatty()

        # Parse args
        parser = argparse.ArgumentParser(description='Move Readability queue to Instapaper.')
        parser.add_argument('-v', '--verbose', action='store_true', default=False)
        parser.add_argument('-a', '--all', action='store_true', default=False,
            help="Transfer all queued Readability items to Instapaper, whether or not they're already present.")
        parser.add_argument('-i', '--instapaper-csv', type=argparse.FileType('r'),
            help="Use supplied CSV (e.g. from instapaper.com) to filter what will be transferred.")
        parser.add_argument('-k', '--readability-key', action='store', default=os.environ.get('READABILITY_KEY'),
            help="The Readability API key to use.")
        parser.add_argument('-s', '--readability-secret', action='store', default=os.environ.get('READABILITY_SECRET'),
            help="The Readability API secret to use.")
        args = parser.parse_args()

        if not args.readability_key:
            parser.error("A Readability API key is required. Specify with -k or the READABILITY_KEY envvar.")
        if not args.readability_secret:
            parser.error("A Readability API secret is required. Specify with -s or the READABILITY_SECRET envvar.")

        # Warn about not using an Instapaper CSV
        if not args.all and not args.instapaper_csv:
            print >>sys.stderr, colored.yellow('Warning')+':', "No Instapaper CSV supplied.", \
            "Won't filter already-added URLs. This can be hazardous to your rate limit.\n"

        # Load the set of URLs already added to Instapaper
        already_added = set()
        if args.instapaper_csv:
            for row in unicode_dict_csv_read(args.instapaper_csv):
                already_added.add(row['URL'].strip().lower())
            args.instapaper_csv.close()

        # Log into Instapaper
        sys.stdout.write("Instapaper email: ")
        sys.stdout.flush()
        insta_uname = raw_input().strip()
        insta_pwd = getpass.getpass()
        print (CURSOR_UP_ONE_AND_ERASE_LINE) * 2 # clear prompts

        sys.stdout.write('Logging into Instapaper...')
        sys.stdout.flush()
        insta = instapaperlib.Instapaper(insta_uname, insta_pwd)
        r, msg = insta.auth()
        if r == 200:
            print ' [ '+colored.green('OK')+' ]'
        else:
            print ' [ '+colored.red('FAILED')+' ]'
            print >>sys.stderr, msg
            sys.exit(1)

        # Auth with Readability
        sys.stdout.write("\nReadability username: ")
        sys.stdout.flush()
        read_uname = raw_input().strip()
        read_pwd = getpass.getpass()
        print (CURSOR_UP_ONE_AND_ERASE_LINE) * 3  # clear prompts

        sys.stdout.write('Logging into Readability...')
        sys.stdout.flush()
        try:
            read_token = readability.xauth(args.readability_key, args.readability_secret, read_uname, read_pwd)
            rdd = readability.oauth(args.readability_key, args.readability_secret, token=read_token)
        except readability.api.AuthenticationError, e:
            print ' [ '+colored.red('FAILED')+' ]'
            print >>sys.stderr, 'Invalid username or password.'
            sys.exit(2)
        else:
            print ' [ '+colored.green('OK')+' ]'

        # Get booksmarks from Readability
        print '\nDownloading all unread bookmarks from Readability. Hold, please.'
        src_bookmarks_orig = rdd.get_bookmarks(archive=False)

        # Sort in ascending order of addition to Readability
        src_bookmarks_orig.sort(key=lambda x: x.date_updated)

        # Simplify Readability structures
        src_bookmarks = []
        for mark in src_bookmarks_orig:
            a, b = mark.article.url.encode('utf8').lower(), mark.article.title.encode('utf8')
            src_bookmarks.append((a, b))

        # Find Readability readings to skip
        urls_to_skip = set(x[0] for x in src_bookmarks) & already_added
        marks_to_post = [x for x in src_bookmarks if x[0] not in urls_to_skip]  # list, maintain order

        # Now add 'em all to Instapaper
        print
        if args.verbose & len(urls_to_skip):
            print 'Adding to Instapaper.'
            for a, b in urls_to_skip:
                print ' - skipping', a
        elif args.verbose or len(urls_to_skip):
            print 'Adding to Instapaper (skipping %d of %d).' % (len(urls_to_skip), len(src_bookmarks))
        else:
            print 'Adding to Instapaper.'
        for a, b in progress.bar(marks_to_post):
            status, msg = insta.add_item(a, b)
            if status not in range(200, 300):
                print >>sys.stderr, "Instapaper:", msg, ";", status
                sys.exit(3)

        print
        print 'Done.'
        print 'Bike safely, cats and kittens :-)'
    except KeyboardInterrupt:
        print
        pass


if __name__ == '__main__':
    main()
