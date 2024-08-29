#!/usr/bin/env python
from os import error
import os
from typing import List
import lupa
import sys
import importlib
from argparse import Action, ArgumentParser


def get_version(*args, **kwargs):
    print(f"Lython 0.0.1, lupa {lupa.__version__}, python {sys.version}")
    print("[insert random quote here] - [insert name here]")


class VersionAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        get_version()
        parser.exit()


parser = ArgumentParser()
parser.register("action", "version", VersionAction)

parser.add_argument("-r", "--repl", action="store_true", help="Start REPL mode")
parser.add_argument(
    "-e", "--experimental", action="store_true", help="Enable experimental features"
)
parser.add_argument("-f", "--file", help="File to run")
parser.add_argument(
    "-v",
    "--version",
    action="version",
    nargs=0,
    help="This outputs the version of Lython and quits",
)

parser.add_argument(
    "-d", "--debug", action="store_true", help="debug mode, shows some event data"
)
args = parser.parse_args()

if args.version:
    get_version()
# Create a Lua runtime
lua = lupa.LuaRuntime(unpack_returned_tuples=True)
sys.path = [*sys.path, "./", os.path.expandvars("$HOME/lython/")]

if args.debug:
    print(sys.path)


def readFile(filename: str):
    with open(filename) as f:
        return f.read()


def pyimport(name):
    try:
        # Use importlib to dynamically import the module
        module = importlib.import_module(name)
        return module
    except ImportError as e:
        raise error(f"Cannot import '{name}': {e}")


def tupleDbouble(x, y):
    if args.debug:
        print(f"trying to make a 2 par touble, a:{x},b:{y}")
    # don't ask me why i had to make this hell-ish thing
    # just accept that it works
    return [x, y]


def tupleTriple(x, y, z):
    if args.debug:
        print(f"trying to make a 3 par touble, a:{x},b:{y},z:{z}")
    return [x, y, z]


def luaDict(d):
    return dict(d)


def initLuaFuncs(*, experimental=False):
    py = {
        # if running with experiments(-e, --experimental on cli),
        # you have a tuple object, that can have multiple sub functions
        # like double, for a 2 argument tuple
        "tuple": tuple
        if not experimental
        else {"double": tupleDbouble, "triple": tupleTriple},
        "dict": dict,
        "list": list,
        "desc": dir,  # short for describe, since this returns a list of callable things on any object
        "float": float,
        "int": int,
        "push_into": lambda d, t: d.append(
            t
        ),  # this is a hack that i had to do, since it kept giving me errors when i ran "some_list.append(some_item)"
        "import": pyimport,
    }
    lua.globals()["int"] = int
    lua.globals()["__name__"] = __name__
    lua.globals()["py"] = py


def repl():
    while True:
        try:
            code = input("lua> ")
            if code.strip().lower() == "exit":
                break
            result = lua.execute(code)
            print(result)
        except Exception as e:
            print(f"Error: {e}")


def main():
    if args.experimental:
        initLuaFuncs(experimental=True)
    else:
        initLuaFuncs(experimental=False)

    if args.repl:
        repl()
    elif args.file:
        lua.execute(readFile(args.file))
    else:
        print("You need to specify a file with -f or start REPL mode with -r.")
        exit(1)


if __name__ == "__main__":
    main()
