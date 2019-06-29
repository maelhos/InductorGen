# InductorGen
A python based on gdspy to generate Inductors


![InductorGen Logo](http://nikolaskama.me/content/images/2017/02/InductorGen_small.png)

# InductorGen

> [InductorGen](https://nikolaskama.me/InductorGenproject) - **Generate inductor's layout**

A python based tool generate inductors layout in GDS.
It allows you to select specific lenght .

- Compatible with Python **3+** 🎉.

- *Not* compatible with Windows.

Authors: [Nikolaos Kamarinakis](mailto:nikolaskam@gmail.com) & [David Schütz](mailto:xdavid@protonmail.com).

[![Build Badge](https://travis-ci.org/maelhos/InductorGen.svg?branch=master)](https://travis-ci.org/maelhos/InductorGen)
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

* Nikolaos Kamarinakis - [@nikolaskama](https://twitter.com/nikolaskama)
* David Schütz - [@xdavidhu](https://twitter.com/xdavidhu)


<br/>

# Disclaimer

InductorGen is provided as is under the MIT Licence (as stated below). 
It is built for educational purposes *only*. If you choose to use it otherwise, the developers will not be held responsible. Please, do not use it with evil intent.


<br/>

# License

Copyright (c) 2017-18 by [Nikolaos Kamarinakis](mailto:nikolaskam@gmail.com) & [David Schütz](mailto:xdavid@protonmail.com). Some rights reserved.

InductorGen is under the terms of the [MIT License](https://www.tldrlegal.com/l/mit), following all clarifications stated in the [license file](https://raw.githubusercontent.com/maelhos/InductorGen/master/LICENSE).


For more information head over to the [official project page](https://nikolaskama.me/InductorGenproject).
You can also go ahead and email me anytime at **nikolaskam{at}gmail{dot}com** or David at **xdavid{at}protonmail{dot}com**.