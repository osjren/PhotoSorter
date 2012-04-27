#===============================================================================
# PhotoSorter Configuration File
#
# PhotoSorter Copyright 2005-2012 Jinsong Ren
#
# This script will be run by PhotoSorter at startup.
# Please customize it. The following is just an example.
#
# Note: PhotoSorter ONLY looks for the configuration file under the CURRENT 
#       directory. Any configuration file in other directories will be ignored.
#       This is to allow different users to have their own configuration files.
#
# For documentations of the project, please go to:
# http://osjren.github.com/PhotoSorter
#
# For bugfixes, updates and support, please go to:
# https://github.com/osjren/PhotoSorter/issues
##===============================================================================

#Input directory shortcuts:
UserConfig['InputDirs'] = [ 
    'test/input', 
    'test', 
    ]

#Output directory shortcuts:
UserConfig['OutputDirs'] = [ 
    'test/output', 
    'test', 
    ]

#Enable transcoding of video files:
#Uncomment the following and set it to False if you don't have ffmpeg installed 
#  or don't need video transcoding.
#UserConfig['EnableVideoTranscoding'] = True #default to True

#Enable writting to a log file:
#Uncomment the following and set it to False if you don't have permission to 
#  write to the current directory or don't want it.
#UserConfig['EnableLogging'] = True #default to True




