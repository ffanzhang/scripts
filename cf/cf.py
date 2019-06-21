#!/usr/bin/env python3

import argparse
import getpass
import sys

from collections import defaultdict

import cflib.auth as auth
import cflib.status as status
import cflib.utils as utils


if sys.version_info[0] >= 3:
    import configparser as cfg
else:
    import ConfigParser as cfg

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-cfg", "--configure", help="Use a configuration file.")
    parser.add_argument("-u", "--username", help="cf handle")
    parser.add_argument("-m", "--mode", help="optional, by default problem set, problem=p, gym=g, contest=c, acm=a")
    parser.add_argument("-l", "--language_code", help="cf language code if you know it")
    parser.add_argument("-f", "--file_name", help="file name to be submitted")
    parser.add_argument("-i", "--id", help="cf problem set id, gym id or contest id")
    parser.add_argument("-x", "--index", help="cf problem index A/B/C/D/E")
    parser.add_argument("-cc", "--clear_cookies", default="0", help="clear cookies, if none 0, clears cookies")
    args = parser.parse_args()

    settings = defaultdict(None)

    # load from config file first
    if args.configure:
        config = cfg.ConfigParser()
        config.read(args.configure)
        for section in config.sections():
            items = config.items(section)
            for key, val in items:
                if val is not None:
                    settings[key] = val

    # command line arguments override config file settings
    for key in vars(args):
        val = getattr(args, key)
        if val is not None:
            settings[key] = val

    essentials = ["username", "file_name"]
    for key in essentials:
        if settings.get(key, None) is None:
            parser.print_help()
            sys.exit(1)

    # TODO: move this block somewhere else
    if settings.get("id") == None and settings.get("mode") != 'a':
        sys.stdout.write("Problem set id not specified, guessing\n")
        settings["id"] = utils.guess_problem_set_id(settings["file_name"])
        if settings.get("id") is None:
            sys.stdout.write("Failed to guess a problem set id")
            sys.exit(1)
        else:
            sys.stdout.write("Using id = {0}".format(settings["id"]))
    if settings.get("index") is None:
        sys.stdout.write("Problem index not specified, guessing")
        settings["index"] = utils.guess_problem_index(settings["file_name"])
        if settings.get("index") is None:
            sys.stdout.write("Failed to guess a problem set id\n")
            sys.exit(1)
        else:
            sys.stdout.write("Using index = {0}".format(settings["index"]))
    for item in ["id", "index", "file_name"]:
        if settings.get(item) is None:
            parser.sys.stdout.write_help()
            sys.stdout.write("One or more of problem/gym/contest id, index or file name is missing\n")
            sys.exit(1)
    
    if settings.get("language_code") is None:
        settings["language_code"] = utils.guess_language_code(settings["file_name"])

    session = None
    # if we ask to clear cookies, we clear the cookies
    if args.clear_cookies.lower() not in ['0', 'f', 'false', 'n', 'no']: 
        auth.clear_cookies()

    # if someone else was logged in, we log the previous person out 
    last_user = auth.get_last_user()
    if last_user is not None and last_user != settings.get("username", None):
        auth.clear_cookies()

    # if current cookie expired or corrupted, re-login
    cookies = auth.load_cookies()
    if auth.cookies_expired(cookies) or not auth.valid_cookies(cookies):
        # re-enter credentials if cookies about to expire
        auth.clear_cookies()
        password = getpass.getpass()
        try:
            session = auth.login(args.username, password)
        except:
            sys.stdout.write("Error logging in\n")
            sys.exit(1)
        auth.save_cookies(session)
        auth.save_last_user(settings["username"])
    else:
        session = auth.session_from_cookies(cookies)

    if args.mode == 'a':
        settings["id"] = 99999

    auth.submit(session, settings["id"], settings["index"], \
                settings["language_code"], settings["file_name"], \
                settings["mode"]) 

    status.get_submit_status(settings["username"], 1) 
