# Unmaintained

This repository is no longer actively maintained.

MagicRescue ISO recipe
======================

This repository contains a recipe and an extraction tool to detect ISO 9660 
files within a block device, such as a disk drive image. This makes it possible 
to recover ISO image files that are contained within that image. This is useful 
in cases of disk drive recovery, where one may have placed images of CD discs 
extracted legally themselves. In a world where CD drives are becoming more 
sparse, such archived images may become more worthwhile to recover.

This recipe is not for extracting ISO images from optical media themselves. 
Other tools exist for that purpose. The block device should be an image of 
a disk drive, stored on a non-faulty and performant drive. The image should be 
extracted from a failing or damaged drive using applications such as
[ddrescue](https://www.gnu.org/software/ddrescue/ddrescue.html). If it contains 
any ISO files with a non-damaged volume descriptor set header, then they are 
copied to singular files.

Requirements
------------

- Some flavor of Linux
- [magicrescue](https://github.com/jbj/magicrescue), which is also available in 
  some package managers, build systems or user repositories, depending on the 
  Linux distribution.
- python 2.7 or 3
- [isoparser](https://github.com/barneygale/isoparser). Download this 
  repository using Git or with a snapshot (and extract it in the latter case), 
  then go into the new directory and run `sudo python setup.py install`. It is 
  also available on [PyPI](https://pypi.python.org/pypi/isoparser), however, 
  version 0.1 could not be installed through `pip install isoparser`, 
  unfortunately, but later versions might be.

Operation
---------

Run `sudo magicrescue -r iso -d OUTPUT_DIRECTORY BLOCK_DEVICE`. In case you 
receive errors, then kill `magicrescue` with `Ctrl-C` and fix the problems.

If the python script cannot be found, then change `iso.py` to the full path of 
the repository in the `iso` recipe. One can restart at the offset address at 
which `magicrescue` was killed or, if an ISO was detect, the address where it 
was found, to retry quickly.

Limitations
-----------

The recipe is able to detect the likely locations of all ISO files, but it may 
also detect chunks of files that are not actually ISO files. If a file that 
contains the ISO signature is found, then the remainder will probably not be 
a correct ISO image, which causes the tool to error as expected, or it may 
start reading stuff further than it should and cause out of memory errors.

Certain ISO files contain duplicate signatures. Both in this case and the case 
of non-ISO files with the signature, `magicrescue` may detect incorrect 
signatures and skip over real ones, so one should manually check for correct 
offsets around the ones provided by `magicrescue`, e.g., with `xxd`.

ISO files with special volume descriptor types that are not defined in ISO 9660 
(boot record, primary, supplementary, partition and terminator) are not 
supported. This includes bootable images such as live CDs.

License
-------

The recipe is available under the MIT License.
