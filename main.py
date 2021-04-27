#! /usr/bin/env python3

import argparse as arg
import sys
import parser
import resolve

def main():
    parser = arg.ArgumentParser()
    args = parser.parse_args()

    p = parser.parse()
    someArray, err = p.parse(args.file)
    if err:
        print("Error : %s" % err)
        return False
    resolver = resolve.resolve(someArray)
    err = resolver.resolve()
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