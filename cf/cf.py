#!/usr/bin/env python3

import argparse
import getpass
import sys

import cflib.auth as auth
import cflib.status as status
import cflib.utils as utils

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-cfg", "--configure", help="Use a configuration file instead, this overrides all the other options.")
    parser.add_argument("-u", "--username", help="cf handle")
    parser.add_argument("-m", "--mode", default="p", help="optional, by default problem set, problem=p, gym=g, contest=c, acm=a")
    parser.add_argument("-l", "--language_code", help="cf language code if you know it")
    parser.add_argument("-f", "--file_name", help="file name to be submitted")
    parser.add_argument("-i", "--id", help="cf problem set id, gym id or contest id")
    parser.add_argument("-x", "--index", help="cf problem index A/B/C/D/E")
    parser.add_argument("-cc", "--clear_cookies", default="0", help="clear cookies, if none 0, clears cookies")
    args = parser.parse_args()

    language_code = "50"
    file_name = ""
    id = "" 
    index = ""
    ext = ".cc"

    if args.clear_cookies.lower() not in ['0', 'f', 'false', 'n', 'no']: 
        auth.clear_cookies()

    if args.configure is None:
        if args.username is None:
            parser.print_help()
            sys.exit(1)

        last_user = auth.get_last_user()
        if last_user is not None and last_user != args.username:
            auth.clear_cookies()

        id, index, file_name = args.id, args.index, args.file_name
        if args.id == None:
            print("Problem set id not specified, guessing")
            id = utils.guess_problem_set_id(args.file_name)
            if id is None:
                print("Failed to guess a problem set id")
            else:
                print("Using id = {0}".format(id))
        if args.index is None and args.mode != 'a':
            print("Problem index not specified, guessing")
            index = utils.guess_problem_index(args.file_name)
            if index is None:
                print("Failed to guess a problem set id")
            else:
                print("Using index = {0}".format(index))
        for item in [id, index, file_name]:
            if item is None:
                parser.print_help()
                print("One or more of problem/gym/contest id, index or file name is missing")
                sys.exit(1)
        
        if args.language_code is None:
            language_code = utils.guess_language_code(file_name)

        session = None
        cookies = auth.load_cookies()
        if auth.cookies_expired(cookies) or not auth.valid_cookies(cookies):
            # re-enter credentials if cookies about to expire
            auth.clear_cookies()
            password = getpass.getpass()
            try:
                session = auth.login(args.username, password)
            except:
                print("Error logging in")
                sys.exit(1)
            auth.save_cookies(session)
            auth.save_last_user(args.username)
        else:
            session = auth.session_from_cookies(cookies)

        if args.mode == 'a':
            id = 99999

        auth.submit(session, id, index, language_code, file_name, args.mode) 
        status.get_submit_status(args.username, 1) 
    else:
        print("TODO")
