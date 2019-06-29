


![InductorGen Logo](https://github.com/maelhos/InductorGen/blob/master/res/logo.png)

# InductorGen

### Generate inductor's layout **

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
~ ❯❯❯ sudo apt-get update && sudo apt-get install nmap

~ ❯❯❯ git clone https://github.com/maelhos/InductorGen.git

~ ❯❯❯ cd InductorGen/

~/InductorGen ❯❯❯ sudo -H pip3 install -r requirements.txt

~/InductorGen ❯❯❯ sudo python3 InductorGen.py
```


## MacOS Installation

If you would like to install InductorGen on a Mac, please run the following:

```
~ ❯❯❯ brew install libdnet nmap

~ ❯❯❯ git clone https://github.com/maelhos/InductorGen.git

~ ❯❯❯ cd InductorGen/

~/InductorGen ❯❯❯ sudo -H pip3 install -r requirements.txt

~/InductorGen ❯❯❯ sudo python3 InductorGen.py
```

**NOTE**: You need to have [Homebrew](http://brew.sh/) installed before running the Mac OS installation. 

Also, **keep in mind** that you might be asked to run some extra commands after executing the pip requirement installation.


<br/>

# Usage

```
Usage: sudo python3 InductorGen.py [options]

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -p PACKETS, --packets=PACKETS
                        number of packets broadcasted per minute (default: 6)
  -s, --scan            perform a quick network scan and exit
  -t TARGETS, --target=TARGETS
                        specify target IP address(es) and perform attack

Examples:
  sudo python3 InductorGen.py --target 192.168.1.10 
  sudo python3 InductorGen.py -t 192.168.1.5,192.168.1.10 -p 30
  sudo python3 InductorGen.py (interactive mode)
```

To view all available options run:

```
~/InductorGen ❯❯❯ sudo python3 InductorGen.py -h
```


<br/>

# Demo

Here's a short demo:

[![Asciinema Demo](https://nikolaskama.me/content/images/2017/01/InductorGen_asciinema.png)](https://asciinema.org/a/98200?autoplay=1&loop=1)

(For more demos click [here](https://asciinema.org/~maelhos))


<br/>

# Developers

* Maël Hostettler - [@maelhos](https://www.instagram.com/maeldu39)
