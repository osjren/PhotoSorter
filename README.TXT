PhotoSorter
- An automated tool to sort out digital photos and videos and transcode (compress) video files

PhotoSorter is open source and uses GPL license

Copyright (C) 2005-2012 Jinsong Ren
*********************************************************
Project home page: http://osjren.github.com/PhotoSorter  
Report bugs: https://github.com/osjren/PhotoSorter/issues
*********************************************************


What is PhotoSorter
===================
- Do you take hundreds or thousands of digital photos and videos a day?  
- Do you have thousands of photo files in one directory or disk and a copy of them in another directory or disk?  
- And some of them are the same but some of them are not because you have either edited them or modified their file names?  
- Or worse, do you have many copies of the original and modified photos scattered everywhere in nested sub-directories on your USB keys, NAS servers, home servers, laptops, desktops, on-line storage space and office computers?  
- And the number of them is so large that it's impossible to sort them out manually or even find them?  
- Do you also have thousands of digital videos taken from you camera that quickly fill up all your disks especially when high-resolution format is common nowadays?  

If the answer is yes, then here comes the PhotoSorter to help. Run it in a terminal and answer a few questions such as the source directory and destination directory and everything is sorted out automatically for you.

A brief history here:  
Back in 2005, I was so fed up with the task of repeatedly sorting out the large amount of digital photos and videos and the usual mess that I wrote a program to free me from this. That was PhotoSorter. 

PhotoSorter doesn't just do simple things like renaming files, it also does some "smart" things. I "invented" a set of naming conventions for the files and used them in PhotoSorter. Based on these, the file names may have dates, types and annotations and PhotoSorter can synchronise them and resolve conflicts. Over the years PhotoSorter has evolved a lot and now is quite mature. However it does require some installation and configuration to make use of its video transcoding functionality (I will provide the detail when I find time).


Supported platforms
===================
Linux or similar with Python 2.4 or above installed. Not tested under Windows or Mac OS.

PhotoSorter is written in pure Python and in theory should run under any platform with Python installed.


Installation
============
No installation required. Simply save the files into a directory you like.


How to Run PhotoSorter
======================
In a terminal, run the following command:  
    python PhotoSorter.py

You may need to set the file's executable attribute before running under Linux.


How to Use PhotoSorter
======================
Running PhotoSorter will present the following menu:

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
        (Seperate multiple functions by comma. Enter "q" to quit at any time)
    Which function [0]? 

Normally you only need to choose the Auto mode by type 0 and enter.

Then you will be asked for the input directory. A list of pre-defined directory shortcuts will be displayed if you have defined them in the user configuration file. 
With the default user configuration file, you will see the following:

    Pre-defined dir shortcuts:
        0-"test/input/"
        1-"test/"
    Input dir (0-9 or path)[0]? 

Enter a number to select a directory shortcut or the path to the directory where you want PhotoSorter to find the original photo and video files.

The contents of the directory will be listed and you will be asked for confirmation:

    === Contents of the dir: 
        MVI_0730.THM
        MVI_0730.AVI
        P8010006.JPG
    Is the dir "test/input/" correct [y]? 

The same goes for the output directory:

    Pre-defined dir shortcuts:
        0-"test/input/"
        1-"test/output/"
        2-"test/"
    Output dir (0-9 or path)[0=same as input]? 

And similarly you will be asked for confirmation. In the above example entering 1 will lead to this:

    === Contents of the dir: 
    Is the dir "test/output/" correct [y]? 

Finally you will be asked if you want to start processing:

    === Input dir:  test/input/
    === Output dir: test/output/
    Start processing? [y]? 

Enter letter 'y' or just hit the Enter key to start the whole process.  
You may quit PhotoSorter in the above Question and Answer stage by entering letter "q".

PhotoSorter will display messages on-screen showing what's going on. By default the messages are also saved to a log file in the current directory.
In this example, you will see something like:

    === Dir "test/input/"

    --- "test/input/MVI_0730.THM"; 0.000KB
    ... Rename to "20111110-MVI_0730.THM"
    ... Sync the acc/mod time to the original
    ... Rename to "20111110-MVI_0730.THM.JPG"
    ... Sync the acc/mod time to the original
    ... Create new dir "test/output/20111110/video"
    ... Move to "test/output/20111110/video/"
    ... Sync the acc/mod time to the original

    --- "test/input/MVI_0730.AVI"; 8.111MB
    ... Rename to "20080121-MVI_0730.AVI"
    ... Sync the acc/mod time to the original
    ... Converting .AVI to .MKV ...
    ... Sync the acc/mod time to the original
    ... Converted to "20080121-MVI_0730.H24.MKV".
    ... Transcoded file: "20080121-MVI_0730.H24.MKV"
    ... Create new dir "test/output/20080121/video"
    ... Move to "test/output/20080121/video/"
    ... Sync the acc/mod time to the original
    ... Redundant original file: "20080121-MVI_0730.AVI"
    ... Create new dir "test/input/#videobin"
    ... Move to "test/input/#videobin/"
    ... Sync the acc/mod time to the original

    --- "test/input/P8010006.JPG"; 1.114MB
    ... Rename to "20060801-P8010006.JPG"
    ... Sync the acc/mod time to the original
    ... Create new dir "test/output/20060801"
    ... Move to "test/output/20060801/"
    ... Sync the acc/mod time to the original

    === 3 files processed in total.
    ------------------------------------------------
    === FnAddDatePrefix:
    === 3 files added with date-prefix.
    ------------------------------------------------
    === FnAddJpgSuffix:
    === 1 THM files added with JPG suffix.
    ------------------------------------------------
    === FnEncodeVideo:
    === 1 video files transcoded.
    === 0 existing target files skipped.
    ------------------------------------------------
    === FnMoveToDatedDir:
    === 3 files moved to dated dirs.
    === 0 existing target files skipped.
    === 1 redundant video files binned.
    === 0 errors.
    ================================================


    === Photo Sorter v2.5.6a (C) J Ren 2005-2012
    === [000-00:00:04] 2012-04-27 12:13:34 AM
    === End.

    === Messages logged to "PhotoSorter-log.txt"


User Configuration
==================
PhotoSorter reads a user configuration script file if it's found under the current directory so that different users may have their own individual configuration files, or a user can have different configurations for different purposes. The default name of the configuration script file is PhotoSorter-config.py. An example file has been provided. You don't have to use it. But if you do, you may want to customize it.

By default, PhotoSort writes the screen messages to a log file named photosorter-log.txt each time it runs. So the existing log file will be overwritten if you run PhotoSorter again. The logging can be disabled in the configuration file.

If you don't have ffmpeg installed or it does not support H.264 encoding, you may disable video transcoding using the 'EnableVideoTranscoding' setting in the configuration file. However, this is not strictly required because PhotoSorter detects ffmpeg automatically and warns you if video transcoding is not supported.


PhotoSorter Terminology and Conventions
=======================================
(to be documented)  
- date prefix
- companion file
- dated directory
- extension name
- video directory
- special directory
- annotation


Video Transcoding (Compression)
===============================
If you have video files in the input directory, PhotoSorter will only transcode (compress) them when the video encoding program is configured correctly. PhotoSorter uses a custom-built ffmpeg version with H.264 support enabled as the encoder and transcodes video files into MKV format using H.264 compression in CRF quality mode. The output video file size is about 1/4 - 1/8 of the original with no noticeable quality degradation. 

One of the reasons to use H.264 video compression instead of MPEG4 in ffmpeg is it's an advanced and popular industrial standard and is widely supported. The other reason is practical: I found only it supports a certain colour space in order to keep the colour quality of the transcoded image the same as that of the original from some camera makers.

MKV's full name is Matroska Multimedia Container. It is an open standard free container format for common multimedia content and also widely supported by open source software and even hardware players. 

Unfortunately the ffmpeg output messages have different formats for different versions and PhotoSorter may not work well with some ffmpeg versions.

If transcoding is successful, PhotoSorter will move the original video file into a special directory named #videobin. Otherwise the original video file will stay where it is. PhotoSorter NEVER deletes the original files.


Compiling and Installing ffmpeg
===============================
Here is a short instruction on how to compile and install ffmpeg with H.264 support under Ubuntu. For more information, please see ffmpeg web site (http://ffmpeg.org/).

Install the Dependencies:  
(1) Uninstall x264, libx264-dev, and ffmpeg if they are already installed. Open a terminal and run the following:

    sudo apt-get remove ffmpeg x264 libx264-dev

(2) Get all of the packages you will need to install FFmpeg and x264 (you may need to enable the universe and multiverse repositories):

    sudo apt-get update
    sudo apt-get install build-essential git-core checkinstall yasm texi2html libfaac-dev \
        libopencore-amrnb-dev libopencore-amrwb-dev libsdl1.2-dev libtheora-dev \
        libvorbis-dev libx11-dev libxfixes-dev libxvidcore-dev zlib1g-dev

Install x264:  
(3) Get the current source files, compile, and install:

    cd
    git clone git://git.videolan.org/x264
    cd x264
    ./configure --enable-static
    make
    sudo checkinstall --pkgname=x264 --default --pkgversion="3:$(./version.sh | \
        awk -F'[" ]' '/POINT/{print $4"+git"$5}')" --backup=no --deldoc=yes

Install FFmpeg:  
(4) Get the most current source files, compile, and install:

    cd
    git clone git://git.videolan.org/ffmpeg
    cd ffmpeg
    ./configure --enable-gpl --enable-version3 --enable-nonfree --enable-postproc \
        --enable-libfaac --enable-libopencore-amrnb --enable-libopencore-amrwb \
        --enable-libtheora --enable-libvorbis --enable-libx264 --enable-libxvid \
        --enable-x11grab  \
        --enable-avfilter --enable-vdpau --enable-bzlib \
        --enable-pthreads --enable-zlib --disable-stripping \
        --enable-runtime-cpudetect --enable-swscale --enable-parser=pcm_u8 
    make
    sudo checkinstall --pkgname=ffmpeg --pkgversion="5:$(./version.sh)" --backup=no \
        --deldoc=yes --default
    hash x264 ffmpeg ffplay ffprobe

Now ffmpeg is installed to: /usr/local/bin/ffmpeg


Supported File Formats
======================
(to be documented)


ToDo
====
- Documentation
- Full test suite
- A few new features I'd like to add


Version History
===============
2005.05.31 - Created by Jinsong Ren.  
2005.06.17 - v1.1.0 Added fully auto mode.  
2005.07.12 - v1.4.0  
2007.10.21 - v1.7.0  
2008.01.04 - v1.8.0  
2011.06.25 - v2.0.0  
2012.04.12 - v2.5.4. Added license terms. Updated EXIF.py to v1.09  
2012.04.22 - v2.5.5  
2012.04.26 - v2.5.6a  

README.txt History
==================
2012.04.12 - Created by Jinsong Ren  
2012.04.19 - Updated the documentation and license  
2012.04.22 - Updated the documentation about v2.5.5  
2012.04.26 - Added the details of the user interaction at running
             Added the compiling instruction for ffmpeg and x264



