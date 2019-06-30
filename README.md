


![InductorGen Logo](https://github.com/maelhos/InductorGen/blob/master/res/logo.png)

# InductorGen

### Generate inductor's layout 

A python based tool to generate inductors layout in GDS.
It allows you to select specific parameters.

- Compatible with Python **3+** .

- *Compatible* with Windows.

Authors: [Maël Hostettler](mailto:maelhos.dev@gmail.com) .

[![Compatibility](https://img.shields.io/badge/python-3-brightgreen.svg)](https://github.com/maelhos/InductorGen)


# Installation

## Linux Installation

You can download InductorGen by cloning the [Git Repo](https://github.com/maelhos/InductorGen) and simply installing its requirements:

```
~ ❯❯❯ git clone https://github.com/maelhos/InductorGen.git

~ ❯❯❯ cd InductorGen/

~/InductorGen ❯❯❯ pip3 install -r requirements.txt

~/InductorGen ❯❯❯ python3 InductorGen.py
```
## Windows Installation

If you would like to install InductorGen on a Mac, please [download InductorGen as zip](https://github.com/maelhos/InductorGen/archive/master.zip), unzip it and run the following:
```
~/InductorGen ❯ pip3 install -r requirements.txt

~/InductorGen ❯ python3 InductorGen.py
```
or use [GitBash](https://gitforwindows.org) and run the following :

```
MINGW64 ~ ❯ git clone https://github.com/maelhos/InductorGen.git
```
then back to cmd :
```
~ ❯ cd InductorGen/

~/InductorGen ❯ pip3 install -r requirements.txt

~/InductorGen ❯ python3 InductorGen.py
```
## MacOS Installation

If you would like to install InductorGen on a Mac, please run the following:

```
~ ❯❯❯ brew install git

~ ❯❯❯ git clone https://github.com/maelhos/InductorGen.git

~ ❯❯❯ cd InductorGen/

~/InductorGen ❯❯❯ pip3 install -r requirements.txt

~/InductorGen ❯❯❯ python3 InductorGen.py
```

**NOTE**: You need to have [Homebrew](http://brew.sh/) installed before running the Mac OS installation. 

Also, **keep in mind** that you might be asked to run some extra commands after executing the pip requirement installation.


<br/>

# Usage

```
usage: python3 InductorGen.py [options]

Required arguments:
  -h, --help            show this help message and exit
  -l LENGTH, --length LENGTH
                        Length of the inscribed square
  -s {4,8}, --sides {4,8}
                        Number of sides of the geometry (only 4 or 8)
  -t TURNS, --turns TURNS
                        Number of turns of the inductor
  -lt LENTURN, --lenturn LENTURN
                        Length of a turn
  -p SPACE, --space SPACE
                        Space between the turns
  -r TAP, --tap TAP     Tapering coeficiant
  -v OVERLAP, --overlap OVERLAP
                        Overlap of the crossings
  -m MARGIN, --margin MARGIN
                        Margin between the vias and the M5 crossings
  -d DEG, --deg DEG     Degrese of the crossings
  -o OUTPUT, --output OUTPUT
                        Filename of the gds out
Optional arguments:
  --disable-preview     Disable GDS output preview
  --disable-save        Disable GDS file saving

Examples:
  python3 InductorGen.py --target 192.168.1.10 
```

To view all available options run:

```
~/InductorGen ❯❯❯ sudo python3 InductorGen.py -h
```
or :
```
~/InductorGen ❯❯❯ sudo python3 InductorGen.py --help
```

<br/>

# Developers

* Maël Hostettler - [@maelhos](https://www.instagram.com/maeldu39)
