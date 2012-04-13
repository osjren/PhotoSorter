PhotoSorter
- An automated tool to sort out digital photos and videos and transcode video files

PhotoSorter is open source and has a MIT-style license

===============================================================================
Copyright (C) 2005-2012 Jinsong Ren

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in 
the Software without restriction, including without limitation the rights to 
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies 
of the Software, and to permit persons to whom the Software is furnished to do 
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
SOFTWARE.
===============================================================================

Supported platforms:
====================
Linux or similar with Python 2.4 or above installed.
Not tested under Windows or Mac OS.

PhotoSorter is written in pure Python and in theory should run under any 
platform with Python installed.


Installation:
=============
No installation required. Simply save the files into a directory you like.


Use:
====
In a terminal, run the following command:
    python PhotoSorter.py
You may need to set the file's executable attribute before running under Linux.


Known Issues:
===============
If you have video files in the input directory, then PhotoSorter will only
work when the video transcoding program is configured correctly.
The default configuration for video transcoding uses a custom-built ffmpeg 
with H.264 support.
If ffmpeg is not in the path or it has no H.264 support, PhotoSorter with the
default configuration will quit with errors.
Unfortunately the ffmpeg output messages have different formats for different
versions and PhotoSorter may fail to work with some ffmpeg versions.

I will document the details and probably provide a compiled ffmpeg when I 
have time.


ToDo:
=====
- Documentation
- Error handling when ffmpeg is not found


Version History:
================
2005.05.31 - Created by Jinsong Ren.
2005.06.17 - v1.1.0 Added fully auto mode.
2005.07.12 - v1.4.0
2007.10.21 - v1.7.0
2008.01.04 - v1.8.0.
2011.06.25 - v2.0.0.
2012.04.12 - v2.5.4. Added MIT license terms. Updated EXIF.py to v1.09




