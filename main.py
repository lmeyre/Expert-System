#! /usr/bin/env python3

import argparse as arg
import sys
import Parser
import Resolver
import Display

def main():
    arg_parse = arg.ArgumentParser()
    arg_parse.add_argument("file")
    #arg_parse.add_argument('file', type=str, nargs='?')
    arg_parse.add_argument("-S", "--show", action="store_true", default=False, help= "Show input file")
    arg_parse.add_argument("-P", "--debug_parse", action="store_true", default=False, help= "Debug parser")
    arg_parse.add_argument("-R", "--debug_resolve", action="store_true", default=False, help= "Debug resolving")
    arg_parse.add_argument("-D", "--details", action="store_true", default=False, help= "All letters are queries")
    args = arg_parse.parse_args()

    try:
        with open(args.file, "r+") as f:
            file_data = f.read().splitlines()
    except Exception as e:
        print("Error : No input file")
        sys.exit(1)

    parser = Parser.Parser(args)
    rules, queries, facts, err = parser.parse(file_data)
    if err:
        print("Error : %s" % err)
        return False
    if (args.debug_parse):
        print("\n\nListing facts, queries, then all rules")
        for key in facts.keys():
            print(key, end="")
        print("")
        print(queries)
        for rule in rules:
            print("Whole rule : ")
            print(''.join(rule.statement) + " => " + ''.join(rule.deduction))
            #print("     " + "detail, rule statement :")
            # for c in rule.statement:
            #     print("     " + c)
            #print("     " + "rule deduction :")
            # for c in rule.deduction:
            #     print("     " + c)
        print("\n////////// ENTERING RESOLVER ////////////\n")
    resolver = Resolver.Resolver(args)
    err, facts = resolver.resolve(rules, facts)
    if err:
        print("Error : %s" % err)
        return False
    Display.display_facts(args, queries, facts)
    return True




if __name__ == '__main__':
    try:
         if main() == False:
            sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(0)