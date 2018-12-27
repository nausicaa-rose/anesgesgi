import argparse

from anesgesgi.build.blog import build_blog
from anesgesgi.build.site import build_site

# anesgesgi build blog <input> <output>
# anesgesgi build site <input> <output>
parser = argparse.ArgumentParser()
parser.add_argument("command")
parser.add_argument("type")
parser.add_argument("input")
parser.add_argument("output")

args = parser.parse_args()

if args.command == "init":
    if args.type == "site":
        pass
    elif args.type == "blog":
        pass
elif args.command == "build":

    if args.type == "blog":
        build_blog(args.input, args.output)
    elif args.type == "site":
        build_site(args.input, args.output)
