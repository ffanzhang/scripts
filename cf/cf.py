#!/usr/bin/python3
import login
import argparse
import status
import sys
import utils

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-cfg", "--configure", help="Use a configuration file instead, this overrides all the other options.")
    parser.add_argument("-u", "--username", default="", help="cf handle")
    parser.add_argument("-p", "--password", default="", help="cf password")
    parser.add_argument("-m", "--mode", default="p", help="optional, by default problem set, problem=p, gym=g, contest=c")
    parser.add_argument("-l", "--language_code", default="50", help="cf language code if you know it")
    parser.add_argument("-f", "--file_name", help="cf language code if you know it")
    parser.add_argument("-i", "--id", help="cf problem set or contest id")
    parser.add_argument("-x", "--index", help="cf problem index A/B/C/D/E")
    args = parser.parse_args()

    handle = ""
    password = ""
    language_code = "50"
    file_name = ""
    id = "" 
    index = ""
    ext = ".cc"

    if args.configure is None:
        if args.username is None or args.password is None:
            parser.print_help()

        handle = args.username
        password = args.password

        if args.id is None:
            print("Please specify a contest/virtual/problem id. (example: -i 1234)")
            sys.exit(1)
        else:
            id = args.id

        if args.index is None:
            print("Please specify an index. (example: -x A)")
            sys.exit(1)
        else:
            index = args.index

        if args.file_name is None:
            print("Please specify a file name. (example: -f r2d2.cc")
            sys.exit(1)
        else:
            file_name = args.file_name
            
        if args.language_code is None:
            ext = file_name.split('.')
            if len(ext) >= 2:
                ext = ext[-1]
                language_code = utils.guess_language_code(ext)

        session = login.get_session(handle, password)
        login.submit(session, id, index, language_code, file_name, args.mode) 
        status.get_submit_status(session, handle, 1) 
    else:
        print("TODO")
