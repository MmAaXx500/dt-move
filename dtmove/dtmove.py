#!/usr/bin/env python3
import platform
from argparse import ArgumentParser
from os import makedirs, path
from os.path import isdir, isfile
from shutil import copy2, copytree
from sqlite3 import connect
from typing import Dict, List, Tuple

linux = False
if platform.system().lower().startswith('lin'):
    import readline
    linux = True


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "library",
        help="The location/destination of the library.db.")

    parser.add_argument(
        "-f", "--from",
        help="The source library.db to copy.",
        dest="frompath")
    parser.add_argument(
        "-m", "--pathmap",
        help="Use a map to rewrite paths.")
    parser.add_argument(
        "--noconfirm",
        help="Do not ask for confirmation. (useful in scripts with --pathmap)",
        action="store_true")
    parser.add_argument(
        "--nofilter",
        help="Do not filter directory hierarchy",
        action="store_true")
    parser.add_argument(
        "-s", "--separatecfg",
        help="Use other configuration directory than where the library resides. Requires --oldcfgdir and --newcfgdir",
        action="store_true")
    parser.add_argument(
        "-o", "--oldcfgdir",
        help="Old configuration directory location. Requires --separatecfg")
    parser.add_argument(
        "-n", "--newcfgdir",
        help="New configuration directory location. Requires --separatecfg")
    parser.add_argument(
        "-l", "--lua",
        help="Copy the lua directory and the luarc file",
        action="store_true")
    parser.add_argument(
        "-c", "--config",
        help="Copy the config file (darktablerc)",
        action="store_true")
    parser.add_argument(
        "-d", "--data",
        help="Copy the data.db and the styles directory",
        action="store_true")

    args = parser.parse_args()

    check_args(args)

    libpath = args.library

    if args.separatecfg or args.frompath:
        if args.oldcfgdir and args.newcfgdir:
            oldcfgdir = args.oldcfgdir
            newcfgdir = args.newcfgdir
            if not isdir(oldcfgdir):
                print_and_quit(
                    f"Old config directory not found! \"{oldcfgdir}\"", 1)
            elif not isdir(newcfgdir):
                print(
                    f"New config directory not found! Creating. \"{newcfgdir}\"")
                makedirs(newcfgdir)
        elif args.frompath:
            frompath = args.frompath

            if not isfile(frompath):
                print_and_quit(
                    f"Old library file not found! \"{frompath}\"", 1)

            oldcfgdir = path.dirname(args.frompath)
            newcfgdir = path.dirname(args.library)

            if not isdir(newcfgdir):
                print(f"Library folder not found! Creating. \"{newcfgdir}\"")
                makedirs(newcfgdir)

            print_copy("library", frompath, libpath)
            copy2(frompath, libpath)

        if args.lua:
            luadir = path.join(oldcfgdir, "lua")
            newluadir = path.join(newcfgdir, "lua")
            luarc = path.join(oldcfgdir, "luarc")
            newluarc = path.join(newcfgdir, "luarc")

            if not isdir(luadir):
                print_and_quit(f"Lua directory not found! \"{luadir}\"", 1)

            print_copy("lua directory", luadir, newluadir)
            copytree(luadir, newluadir, dirs_exist_ok=True)

            print_copy("luarc", luarc, newluarc)
            copy2(luarc, newluarc)

        if args.config:
            cfgfile = path.join(oldcfgdir, "darktablerc")
            newcfgfile = path.join(newcfgdir, "darktablerc")

            if not isfile(cfgfile):
                print_and_quit(f"Config file not found! \"{cfgfile}\"", 1)

            print_copy("config file", cfgfile, newcfgfile)
            copy2(cfgfile, newcfgfile)

        if args.data:
            datadb = path.join(oldcfgdir, "data.db")
            newdatadb = path.join(newcfgdir, "data.db")
            styles_dir = path.join(oldcfgdir, "styles")
            newstyles_dir = path.join(newcfgdir, "styles")

            if not isfile(datadb):
                print_and_quit(f"data.db file not found! \"{datadb}\"", 1)

            print_copy("data.db", datadb, newdatadb)
            copy2(datadb, newdatadb)

            if isdir(styles_dir):
                print_copy("styles directory", styles_dir, newstyles_dir)
                copytree(styles_dir, newstyles_dir, dirs_exist_ok=True)
            else:
                print(f"Styles directory not found. Skipped. \"{styles_dir}\"")

    if not isfile(libpath):
        print_and_quit(f"Library not found! \"{libpath}\"", 1)

    print(f"Opening library: {libpath}")
    lib = connect(libpath)
    cur = lib.cursor()
    paths = cur.execute('''SELECT folder FROM film_rolls''').fetchall()
    paths = [e[0] for e in paths]
    basepaths = get_basepaths(paths, args.nofilter)

    rewritemap: Dict[str, str] = {}
    skips: List[str] = []
    ok = False
    if args.pathmap:
        pathmap: str = args.pathmap

        if not isfile(pathmap):
            print_and_quit(f"Pathmap not found! \"{pathmap}\"", 1)

        file = open(pathmap, "r").readlines()
        parse_pathmap(file, basepaths, rewritemap)

        skips = list(basepaths.keys())
        if len(rewritemap) > 0:
            ok = True

    else:
        rewritemap, skips, ok = ask_paths(basepaths)

    if ok:
        if ask_summary(rewritemap, skips, args.noconfirm):
            for old, new in rewritemap.items():
                # (?) in order: old path, new path, old separator, new separator, old path
                query = """
                    UPDATE film_rolls
                    SET folder =
                        REPLACE(REPLACE(folder, (?), (?)), (?), (?))
                    WHERE folder like (?)"""

                if '/' in old and ':' in new:
                    cur.execute(query, (old, new, '/', '\\', old + '%'))
                elif ':' in old and '/' in new:
                    cur.execute(query, (old, new, '\\', '/', old + '%'))
                else:
                    cur.execute(query, (old, new, '', '', old + '%'))

            lib.commit()

    lib.close()
    quit()


def check_args(args):
    if args.separatecfg:
        if not args.oldcfgdir or not args.newcfgdir:
            print_and_quit(
                "--separatecfg requires --oldcfgdir and --newcfgdir", 1)
        elif not args.lua and not args.config and not args.data:
            print_and_quit(
                "Specifying config directory without --lua, --config or --data is useless", 1)
    else:
        if args.oldcfgdir or args.newcfgdir:
            print_and_quit(
                "Specifying old/new config directory without --separatecfg is useless", 1)
        elif not args.frompath:
            if args.lua or args.config or args.data:
                print_and_quit(
                    "--lua, --config and --data requires --form or --separatecfg", 1)


def print_copy(what: str, src: str, dest: str):
    print(f"Copying {what}\n"
          f"\tfrom: {src} \n"
          f"\tto: {dest}")


def parse_pathmap(file: List[str], basepaths: Dict[str, List[str]], rewritemap: Dict[str, str]):
    for linenum, line in enumerate(file, start=1):
        line = line.strip()
        if len(line) == 0 or line[0] == '#':
            continue

        if "/>" in line:
            splits = line.split("/>")
            splits = [e.strip() for e in splits]
            if len(splits) == 2 and splits[0] in basepaths:
                rewritemap[splits[0]] = splits[1]
                remove_basepaths(basepaths, splits[0])
            else:
                print(f"{linenum}. line is invalid. Skipped.")

        else:
            print(f"{linenum}. line skipped.")


def get_basepaths(paths: list, nofilter) -> Dict[str, List[str]]:
    """Get basepaths with optional filtering"""
    bases = find_bases(paths, {})
    if not nofilter:
        bases = filter_bases(bases)
    return bases


def find_bases(paths: list, bases: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """Find and return possible directories which can be rewritten by user"""
    start_len = len(bases)

    path: str
    for path in paths:
        if ":" in path:
            cutoff = path.rfind('\\')
        else:
            cutoff = path.rfind('/')

        tree = bases.get(path[:cutoff], [])

        if cutoff > 0 and path not in tree:
            tree.append(path)
            bases[path[:cutoff]] = tree

    if start_len < len(bases):
        bases = find_bases(list(bases.keys()), bases)

    return bases


def filter_bases(bases: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """Return a list of directories witch have at least two subdirectories"""
    return {k: v for k, v in bases.items()
            if len(v) > 1 or
            (len(v) == 1 and v[0] not in bases.keys())}


def ask_paths(basepaths: Dict[str, List[str]]) -> Tuple[Dict[str, str], List[str], bool]:
    first = True
    rewritemap: Dict[str, str] = {}

    while len(basepaths) != 0:
        pathlist = dict(zip(range(1, len(basepaths) + 1),
                        sorted(list(basepaths.keys()))))
        response = ask_chooselocation(pathlist, first)

        if first:
            first = False

        if response == 'w':
            break
        elif response == 'q':
            return {}, [], False
        elif response in [str(o) for o in pathlist.keys()]:
            old_location = pathlist[int(response)]
            new_location = ask_newlocation(old_location)

            if new_location == 'w':
                break
            elif new_location == 'q':
                return {}, [], False

            rewritemap[old_location] = new_location
            remove_basepaths(basepaths, old_location)
        else:
            print("The chosen option is not valid: \"{}\"".format(response))

    return rewritemap, sorted(list(basepaths.keys())), True


def ask_chooselocation(pathlist: Dict[int, str], first: bool) -> str:
    print_separator()

    if first:
        print("We found the following directories in the library.\n"
              "NOTE: Choosing a path upper in the hierarchy also rewrites the directories below it.")
    else:
        print("Following directories remained.")

    print("Choose the one what you want to rewrite:")
    print_pathlist(pathlist)
    ret = input("{}...{}, (w)rite, (q)uit: ".format(
        min(pathlist.keys()), max(pathlist.keys())))
    return ret


def print_pathlist(pathlist: Dict[int, str]):
    for k, v in pathlist.items():
        print("\t{}. {}".format(k, v))


def ask_newlocation(old_path: str) -> str:
    print_separator()
    print("Write the new path below for \"{}\"".format(old_path))
    if linux:
        readline.set_completer_delims('')
        readline.parse_and_bind('tab: complete')
    ret = input("(w)rite, (q)uit: ")
    if linux:
        readline.parse_and_bind('tab: self-insert')
    if len(ret) > 0:
        return ret[:-1] if ret[-1] == '\\' or ret[-1] == '/' else ret
    return ret


def remove_basepaths(basepaths: Dict[str, List[str]], path: str):
    """Remove key(s) from 'basepaths' specified by 'path', any subdirectories 
    and parent directories if it's the only subdirectory"""
    remove_basepaths_down(basepaths, path)
    remove_basepaths_up(basepaths, path)

    return


def remove_basepaths_down(basepaths: Dict[str, List[str]], path: str):
    """Remove subdirectories"""
    for e in basepaths.pop(path, []):
        remove_basepaths_down(basepaths, e)


def remove_basepaths_up(basepaths: Dict[str, List[str]], path: str):
    """Remove parent directories if the `path` is the only subdir"""
    sliceidx = max(path.rfind('\\'), path.rfind('/'))
    if sliceidx > 0:
        sliceidx = sliceidx - 1 if path[sliceidx-1] == '\\' else sliceidx
        parentdir = path[:sliceidx]
        if parentdir in basepaths and len(basepaths[parentdir]) <= 1:
            basepaths.pop(parentdir)
            remove_basepaths_up(basepaths, parentdir)


def ask_summary(rewritemap: Dict[str, str], skips: List[str], noconfirm) -> bool:
    if noconfirm:
        print_summary(rewritemap, skips)
        return True

    while True:
        print_separator()
        print("Please review your chosen options.")
        print_summary(rewritemap, skips)

        response = input("(o)k, (q)uit: ")
        if response == 'o':
            return True
        elif response == 'q':
            return False
        else:
            print("The chosen option is invalid: \"{}\"".format(response))


def print_summary(rewritemap: Dict[str, str], skips: List[str]):
    if len(skips) > 0:
        print("\npaths that will NOT be rewritten:\n")
        for s in skips:
            print(f"\t{s}")
    print("\npaths that will be rewritten:")
    for old, new in rewritemap.items():
        if isdir(new):
            print("\t{}\n   \t-> {}\n".format(old, new))
        else:
            print("\t{}\n  !\t-> {}\n".format(old, new))


def print_separator():
    print("\n\n")


def print_and_quit(txt: str, exitcode: int):
    print(txt)
    quit(exitcode)


def quit(exitcode: int = 0):
    exit(exitcode)


if __name__ == '__main__':
    main()
