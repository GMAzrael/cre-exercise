# Debian packages with the most files

```
$ ./package-statistics.py -h
usage: package-statistics.py [-h]
    {amd64,arm64,armel,armhf,i386,mips,mipsel,mips64el,ppc64el,s390x}

Show top 10 packages with the most files

positional arguments:
  {amd64,arm64,armel,armhf,i386,mips,mipsel,mips64el,ppc64el,s390x}
                        Architecture to be used

optional arguments:
  -h, --help            show this help message and exit
```

## Design

An effort has been made to use modules from the Python standard library. Since this is new code with no legacy, python3.6 was chosen.

`argparse` is used for command line validation and `urllib` is used for HTTP requests. The reason for choosing `urllib` over `requests` was the ability to easily pass a stream of bytes into the `gzip` module. An ex-DPL himself filed [the bug](https://bugs.python.org/issue11608).

Since `Contents-*.gz` is decompressed into a byte-array, it is necessary to `decode()` bytes so that we have strings to play around with.

### Assumptions

* The most complicated line this can parse is:
```
bin/busybox        utils/busybox,shells/busybox-static
```
* Package and section names do not have spaces in them
* Filenames can have space in them

## Return values

| Value | Meaning |
|-------|---------|
| 0     | All OK  |
| 1     | Error parsing a line |
| 2     | Could not download file |

## TODOs

* unit tests
