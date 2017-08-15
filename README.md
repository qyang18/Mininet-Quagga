# Mininet-Quagga Topo:
![](./src/Architecture.jpg)

# 1. Quagga Install And Configuration

## Quagga Install Guide:

http://blog.chinaunix.net/uid-25513153-id-212328.html

## Download Quagga:

http://download.savannah.gnu.org/releases/quagga/quagga-1.2.1.tar.gz

## Unzip and Configure:

> $ ./configure --enable-vtysh --enable-user=root --enable-group=root --enable-vty-group=root

### If GNU awk is required:

> $ sudo apt-get install gawk

### If libreadline is required:

> $ sudo apt-get install libreadline6 libreadline6-dev

### If libcares is required:

> $ sudo apt-get install libc-ares-dev

## Make:

> $ make

### If aclocal-1.15 is missing:

> $ sudo apt-get install automake

### If makeinfo is missing:

> $ sudo apt-get install texinfo

## Make install:

> $ sudo make install

## Make new file, copy zebra.conf.sample to zebra.conf:

> $ cd /usr/local/etc
> $ sudo cp zebra.conf.sample zebra.conf

## Start zebra:

> $ sudo zebra -d

### If zebra: error while loading shared libraries: libzebra.so.1: cannot open shared object file: No such file or directory

> $ cd /usr/local/lib
> $ sudo cp libzebra.* /lib
> $ sudo rm libzebra.*

# 2. Quagga Service Start

## Connect to zebra using telnet(password zebra):

> $ telnet localhost 2601
