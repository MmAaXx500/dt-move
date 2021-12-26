# DT-move

DT-move is a helper script for [darktable][1]. The main functions are to move and synchronize the darktable's database. 

If you moved to a new OS, PC, or just moved your images, you have three options:
1. On the new place reimport all images
2. Move the configuration directory. But when you open darktable you found yourself facing with a lot of skulls. 💀
3. Use DT-move (hint: this is the correct one)

If you choose the first, that's time consuming if you have lot of images and even you lose some attributes like grouping.

If you choose the second, you have all information without your images. Probably not a viable option.

If you choose the third, please scroll down to learn more.

[1]: https://darktable.org/ "darktable's homepage"

## Table of Contents

* [The purpose of DT-move](#the-purpose-of-dt-move)
* [What DT-move does](#what-dt-move-does)
* [What DT-move not does](#what-dt-move-not-does)
* [Prerequisites](#prerequisites)
* [Installation](#installation)
* [Usage](#usage)
* [Advanced usage](#advanced-usage)
  * [Automation](#automation)
  * [Partial updates](#partial-updates)
* [Parameter reference](#Parameter-reference)
* [Contributing](#contributing)
* [License](#license)

## The purpose of DT-move

DT-move can help in the following cases:

* Moved your images elsewhere, use them without needed to be re-imported.
* You moved to a new PC, you can update the paths in the database to fit in to your new environment.
* Jumping between OSes (e.g. Linux - Win) you can sync the database between them so not needed to import the images twice.

## What DT-move does

* Copies darktable's configuration files
* Rewrites paths in darktable's database

## What DT-move not does

* Touches your images
* Move your images
* Feed your pets 🐶

## Prerequisites

* Python 3.8 or newer
* Backup of your darktable configuration
* Tested with darktable 3.4, 3.6 and 3.8
* Tested on Linux and Windows, probably works on Mac too (but there is no guarantee)

## Installation

Just download the `dtmove.py` from the `dtmove` directory and execute it with the appropriate parameters according to [Usage](#Usage).

## Usage

The most basic usage is just specifying the library location. This allows you to configure the library in place (overwrite it).

To do this, you must already copy the database to the new location. 

`./dtmove.py ~/.config/darktable/library.db`

If you don’t want to copy by hand, you can specify where and what you want to copy from. To do this, I need to present some parameters.

**If you store the `library` along with the other config files (this is the default) you need these parameters:**

* `-f` or `--from` is the source (old location) of the library
* `-l` or `--lua` if you want to copy the `lua` directory and `luarc`
* `-c` or `--config` if you want to copy the `darktablerc` file which stores your darktable settings (but not the shortcuts)
* `-d` or `--data` if you want to copy the `data.db` along with the `styles` directory

> ⚠️ If you transferring the `lua` directory between Linux and Windows pay attention to the line endings, they can prevent you from updating your scripts. In this case issue a `git reset --hard` in the `lua` directory on the target system.

`./dtmove.py --lua --config --data --from /old/darktable/library.db /new/darktable/library.db`

**If you are storing the `library` in a separate directory you need two more parameters:**

* `-o` or `--oldcfgdir` is the old location of the configuration directory
* `-n` or `--newcfgdir` is the new location of the configuration directory

`./dtmove.py --oldcfgdir /old/cfgdir --newcfgdir /new/cfgdir --lua --config --data --from /old/darktable/library.db /new/darktable/library.db`

After starting the script you can replace the broken paths with the valid ones to do not see more skulls.

To provide an example I will use the following directory structure:
```
home/
  |- olduser/
     |- images/
        |- 2020/
        │  |- 2020-01-01/
        │  |- 2020-12-31/
        |- 2021/
           |- 2021-01-01/
           |- 2021-12-31/

```
First you have see many directories, something similar way as below.
```
Choose the one what you want to rewrite:
    1. /home/olduser/images
    2. /home/olduser/images/2020
    3. /home/olduser/images/2021
1...3, (w)rite, (q)uit: 
```
There you can choose a number which path you want to rewrite. I will go with the `1`.

As you can see the `/home/olduser` folder was not offered as an option. If you want to rewrite any of the upper directories you can use the `--nofilter` parameter.

After you selected one the following screen come up:
```
Write the new path below for "/home/olduser/images"
(w)rite, (q)uit: 
```
Here you can write the new path. I will go with `/home/me/Pictures`.

Next screen is a summary. If an exclamation mark (`!`) is displayed before the arrow (`->`) that means the path is currently does not exist, but if it is intentional you can continue.
```
Please review your chosen options.
Paths that will be rewritten:
    /home/olduser/images
    -> /home/me/Pictures
(o)k, (q)uit: 
```
There you can save the changes by writing `o` or you can discard them by writing `q`. You are done! If you open darktable now you can see your images.

The directory structure is now (In the database. We are not touched your images) is the following:
```
home/
  |- me/
     |- Pictures/
        |- 2020/
        │  |- 2020-01-01/
        │  |- 2020-12-31/
        |- 2021/
           |- 2021-01-01/
           |- 2021-12-31/

```

## Advanced usage

### Automation

Do not want to write down the paths every time? Here is the solution: Use pathmaps.

If you use a pathmap you supply the required paths from a text file.

Structure of a pathmap file:
```
# You can write comments on empty lines

/the/old/path /> /the/new/path

# Spaces do not need to be escaped
/a/path/with spaces /> /a/new path/with spaces
```

You can obtain the paths by running the script only with the `library` parameter and then use `q` to quit.

If you are done with the file you can run the script like this:

`./dtmove.py -m ./dtmove.pathmap ./path/to/library.db`

At the and it will ask for your confirmation with the well known summary screen. If you don't want to answer the confirmation either you can supply the `--noconfirm` parameter to accept automatically.

### Partial updates

If you have moved a folder, you do not need to re-import the images, just update the database.

Run the script with the library parameter only, when you updated the required path you can hit the `w`, you will land on the summary screen and save it with the `o` key.

## Parameter reference

```
library              The location/destination of the library.db. (Required)
                     e.g. ~/.config/darktable/library.db

-f --from            The source library.db to copy.
                     e.g. /mnt/olddrive/home/me/.config/darktable/library.db

-m --pathmap         Use a map to rewrite paths.
                     e.g. ./dbmove.pathmap

--noconfirm          Do not ask for confirmation. (useful in scripts with --pathmap)

--nofilter           Do not filter directory hierarchy

-s --separatecfg     Use other configuration directory than where the library resides.
                     Requires --oldcfgdir and --newcfgdir

-o --oldcfgdir       Old configuration directory location.
                     Requires --separatecfg

-n --newcfgdir       New configuration directory location.
                     Requires --separatecfg

-l --lua             Copy the lua directory and the luarc file

-c --config          Copy the config file (darktablerc)

-d --data            Copy the data.db and the styles directory
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[GNU GPLv3](LICENSE)
