#! /usr/bin/env python3

import argparse as arg
import sys
import Parser
import Resolver

def main():
    arg_parse = arg.ArgumentParser()
    arg_parse.add_argument('file', type=str, nargs='?')
    args = arg_parse.parse_args()

    try:
        with open(args.file, "r+") as f:
            file_data = f.read().splitlines()
    except Exception as e:
        print(e)
        sys.exit(1)

    parser = Parser.Parser()
    rules, facts, queries, err = parser.parse(file_data)
    if err:
        print("Error : %s" % err)
        return False

    resolver = Resolver.Resolver()
    err = resolver.resolve(rules, facts)
    if err:
        print("Error : %s" % err)
        return False
    return True

if __name__ == '__main__':
    try:
         if main() == False:
            sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(0)