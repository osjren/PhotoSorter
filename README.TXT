PhotoSorter
- An automated tool to sort out digital photos and videos and transcode video files

PhotoSorter is open source and uses GPL license

===============================================================================
Copyright (C) 2005-2012 Jinsong Ren

What is PhotoSorter:
====================
Do you take hundreds or thousands of digital photos and videos a day?<br>
Do you have thousands of photos in one directory or disk and a copy of them in another directory or disk:<br>
Or worse, some of them are the same but some of them are not because you have either edited the content or modified the file names<br>
Or you have many copies of the original and modified photos and videos mixed everywhere in nested sub-directories on your USB drives, NAS, home server, laptops, desktops, on-line storage space, office computers etc.<br>
And the number of them is so large that it's impossible to sort them out manually or even find them when you need them.<br>
Do you also have thousands of digital videos taken from you camera, some of them are in HD format, that quickly fill up all your disks?<br>

If the answer is yes, then here comes the PhotoSorter to help. Run it in a terminal and answer a few questions such as the source directory and destination directory and everything is sorted out.

A brief history here:<br>
Back in 2005, I was so fed up with the task of repeatedly sorting out the large amount of digital photos and videos and the usual mess that I wrote a program to do it. That was PhotoSorter. PhotoSorter didn't just do "simple" things, it also did some "smart" things. I "invented" a set of naming conventions for the files and implemented them in PhotoSorter (more details later). Over the years PhotoSorter has evolved a lot and now is quite mature except it does require some special configuration to make it fully functional (I will improve this when I find time).


What does PhotoSorter do:
=========================
Running PhotoSorter will present the following menu:
<pre>
=== Photo Sorter 2.5.4
Function list:
   0-Auto;
   1-Change the ext of companion .JPG files of .MOV files to .THM;
   2-Add date prefix to filenames;
   3-Add .JPG after .THM;
   4-Transcode video files but skip dated dirs;
   5-Transcode video files in all dirs;
   6-Sync video filename to the orig or old transcoded filename in video dirs;
   7-Bin redundant original & outdated transcoded video files in video dirs;
   8-Sync THM filename to the video filename in video dirs;
   9-Move files to dated directories;
   10-Auto but overwrite existing destination transcoded video files;
   (Seperate multiple actions by comma)
Which function [0]? 
</pre>
(The explanations will come later when I find time).


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
In a terminal, run the following command:<br>
    python PhotoSorter.py<br>

You may need to set the file's executable attribute before running under Linux.<br>


Customization:
==============
PhotoSort runs a startup script file if it exists at startup. The default name of the startup script file is PhotoSorter-startup.py. You should customize the startup file if you want to use it.

By default, PhotoSort writes the screen messages to a log file named photosorter-log.txt each time it runs. So the existing log file will be overwritten if you run PhotoSorter again.

(more to follow when I find time)


PhotoSorter Terminology and Conventions:
========================================
(to be documented)<br>
- date prefix<br>
- companion files<br>
- dated directory<br>
- extension names<br>
- video directory<br>
- special directory<br>
- comment<br>


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

(I will document the details and probably provide a compiled ffmpeg when I 
find time)


ToDo:
=====
- Documentation<br>
- Error handling when ffmpeg is not found<br>
- A few new features I'd like to add<br>


Version History:
================
2005.05.31 - Created by Jinsong Ren.<br>
2005.06.17 - v1.1.0 Added fully auto mode.<br>
2005.07.12 - v1.4.0<br>
2007.10.21 - v1.7.0<br>
2008.01.04 - v1.8.0.<br>
2011.06.25 - v2.0.0.<br>
2012.04.12 - v2.5.4. Added license terms. Updated EXIF.py to v1.09<br>

README.txt History:
===================
2012.04.12 - Created by Jinsong Ren<br>
2012.04.19 - Updated the documentation and license<br>


