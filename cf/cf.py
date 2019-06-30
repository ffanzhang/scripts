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

CFG_HELP            = "use a configuration file"
USERNAME_HELP       = "cf handle"
MODE_HELP           = "optional, problem = p, gym = g, contest = c, acm = a. (default = p)"
LANGUAGE_CODE_HELP  = "cf language code if you know it, (default = c++)"
FILE_NAME_HELP      = "file name to be submitted"
ID_HELP             = "cf problem set id, gym id or contest id"
INDEX_HELP          = "cf problem index A/B/C/D/E"
CC_HELP             = "clear cookies, if none zero, clears cookies"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-cfg", "--configure",      help = CFG_HELP)
    parser.add_argument("-u",   "--username",       help = USERNAME_HELP)
    parser.add_argument("-m",   "--mode",           help = MODE_HELP, default = "p")
    parser.add_argument("-l",   "--language_code",  help = LANGUAGE_CODE_HELP, default = "50")
    parser.add_argument("-f",   "--file_name",      help = FILE_NAME_HELP)
    parser.add_argument("-i",   "--id",             help = ID_HELP)
    parser.add_argument("-x",   "--index",          help = INDEX_HELP)
    parser.add_argument("-cc",  "--clear_cookies",  help = CC_HELP,  default = "0")
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
                    settings[key] = val.strip()

    # command line arguments override config file settings
    for key in vars(args):
        val = getattr(args, key)
        if val is not None:
            settings[key] = val.strip()

    if settings['mode'] == 'a':
        settings["id"] = 99999

    essentials = ["username", "file_name"]

    for key in essentials:
        if settings.get(key) is None:
            parser.print_help()
            sys.exit(1)

    # a map from key missing to method guessing the key
    criticals = {"id"               : "guess_problem_set_id", \
                 "index"            : "guess_problem_index", \
                 "language_code"    : "guess_language_code"}

    for key in criticals:
        if settings.get(key) is None:
            sys.stdout.write("Guessing " + key + "\n")
            func = getattr(utils, criticals[key])
            settings[key] = func(settings["file_name"])
            if settings[key] is None:
                sys.stdout.write("Failed to guess " + key + "\n")
                parser.print_help()
                sys.exit(1)
            else:
                sys.stdout.write("Using " + settings[key] + "\n")

    for item in ["id", "index", "file_name"]:
        if settings.get(item) is None:
            parser.print_help()
            sys.stdout.write("One or more of problem/gym/contest id, index or file name is missing\n")
            sys.exit(1)

    session = None
    # if we ask to clear cookies, we clear the cookies
    if settings["clear_cookies"].lower() not in ['0', 'f', 'false', 'n', 'no']: 
        auth.clear_cookies()

    # if someone else was logged in, we log the previous person out 
    last_user = auth.get_last_user()
    if last_user is not None and last_user != settings.get("username"):
        auth.clear_cookies()

    cookies = auth.load_cookies()
    if auth.valid_cookies(cookies):
        try:
            session = auth.session_from_cookies(cookies)
            auth.save_last_user(settings["username"])
        except:
            sys.stdout.write("Error recovering session\n")
            sys.exit(1)
    else:
        # re-enter credentials if cookies expired or not valid
        try:
            auth.clear_cookies()
            session = auth.login(settings["username"], getpass.getpass())
            auth.save_cookies(session)
            auth.save_last_user(settings["username"])
        except:
            sys.stdout.write("Error logging in\n")
            sys.exit(1)

    auth.submit(session, settings["id"], settings["index"], \
                settings["language_code"], settings["file_name"], \
                settings["mode"]) 

    status.get_submit_status(settings["username"], 1) 
