# -*- coding: utf-8 -*-
"""
Copyright (C) 2005-2012 Jinsong Ren

For documentations of the project, please go to:
http://osjren.github.com/PhotoSorter

For bugfixes, updates and support, please go to:
https://github.com/osjren/PhotoSorter/issues

This file is part of PhotoSorter.

PhotoSorter is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PhotoSorter is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PhotoSorter.  If not, see <http://www.gnu.org/licenses/>.
"""
#===============================================================================
# Main functions:
#   1) Add dated prefix to photos and videos.
#   2) Create dated dir and move dated photos and video files into dated dir.
#   3) Transcode video files (requires ffmpeg)
#
# History:
#   2005.05.31 - Created by Jinsong Ren.
#   2005.06.01 - Added  .THM to .THM.jpg function.
#   2005.06.10 - If the 2nd file ext is .dvx, omit. Added more encoding modes.
#   2005.06.12 - Added 4 Verbosity levels, 0:off; 3:most detailed.
#   2005.06.17 - v1.1.0 Added fully auto mode.
#   2005.06.18 - v1.2.0 Use class Con to store options.
#   2005.07.11 - v1.3.0 Add auto rename function. Creation time is kept for dvx files.
#   2005.07.12 - v1.4.0 Added function: Move files to dated dir.
#   2005.09.17 - fixed bug on sorting avi files.
#   2005.10.29 - v1.4.1, avi files are moved to video sub-dir. Fixed .thm bug.
#   2006.04.20 - v1.4.2, added photo type begin with 'P'.
#   2006.07.22 - v1.4.3, added the Profile attr to record the config path. Aded
#                file existance check in GetVcf().
#   2006.07.23 - v1.4.4, process files beginning with 'C'. Fixed bug, now skip when
#                encoded avi file exists.
#   2006.07.30 - v1.4.5, added more AVI encoding bitrate options. Changes vcf file forming process.
#   2006.07.30 - v1.4.6, added more AVI encoding bitrate options.
#   2006.08.02 - v1.4.7, fixed: MVI audio compression, Lame MP3 encoder not compatible.
#   2006.08.03 - v1.4.8, fixed: audio compression not compatible. Added: option of process photos first.
#   2006.12.21 - customized config for IBM laptop.
#   2006.12.24 - Seperated the OptClass from the main program to form a file
#   2007.02.05 - v1.5.0, Introduced user defined config files
#   2007.05.16 - v1.6.0, added xvid settings
#   2007.06.01 - v1.6.1. Bug fix. Rename bug; Empty EXIF tag bug.
#   2007.06.02 - v1.6.2. Minor fix. Skip video dir.
#   2007.06.05 - v1.6.3. Skip date dir.
#   2007.10.21 - v1.7.0. Use 4 digits for year for dir and file prefix. Add .THM to Lumix .mov files.
#   2008.01.04 - v1.8.0. Use two pass procedure to identify & change .JPG to .THM for Lumix .MOV files.
#   2011.06.25 - v2.0.0. changes: Don't transcode video file. Just rename them like the photos. Made it work under Linux.
#   2011.07.31 - v2.1.0. Added: re-coding video to mkv format using mpeg4 compression.
#   2011.09.01 - replace subprocess.check_output (new in phthon v2.7) with check_call (new in v2.5)
#                Change printed message to: Derived file
#   2011.09.13 - v2.1.1. Now move the unneeded original video files to a special dir.
#   2011.09.19 - v2.2.0. Added function 5, moving unneeded original video files to video bin dir.
#                Added functions: Transcode video files in or not in dated dirs.
#   2011.09.20 - v2.2.1. Added: support for multiple actions.
#   2011.09.28 - exclude MVI_0729.avi-like files that has 11.02kHz audio not supported by mpeg4 from re-encoding because ffmepg reports error.
#   2011.10.11 - v2.2.2. Added auto-detection of frame rate and size. Video with any frame rate can be encoded by ffmpeg without error message now.
#   2011.10.11 - bug fixed: .avi files not processed in ProcBinRedundantVideoFiles
#   2011.10.13 - added new token to find streams info in the output of the latest ffmpeg version
#   2011.10.14 - added: keep asking for correct answers until correct answers are given in the main menu.
#   2011.10.14 - vcodec is changed to libx264
#   2011.10.23 - v2.3.0. Full support to video encoding using h264.
#   2011.10.25 - Bug fix.
#   2011.10.26 - Modified ProcBinVideoFiles into ProcBinRedundantVideoFiles.
#                Bug fix.
#   2011.10.26 - Added: detection of possible redundanct video files.
#   2011.10.28 - Added: sync files names of video and THM files.
#   2011.11.09 - Added: full support to moving files to a output dir different from the input dir.
#                Added: log file.
#                Bug fixed: cross-device file moving error.
#   2011.11.10 - Added: smart detection of commented video dirs.
#   2011.11.16 - fully working sync functionality.
#   2011.11.25 - New function to bin redundant video files.
#   2011.11.25 - Added: startup file with pre-defined dirs.
#   2011.11.30 - Added: app header and footer. Sync file mod/access time to the orig.
#                Fixed: cross-device move failure.
#   2011.11.30 - Added: print out acc/mod time sync msg.
#   2011.12.01 - Added: user can quit the rest after a video is encoded by entering 'q'.
#   2011.12.02 - Removed the user quit coz it does't work.
#                Added: do not move the original video files in #videobin dir.
#   2011.12.06 - Added: changed GetRealVideoDir to GetRealVideoDirFname to return the real fname as well.
#   2011.12.07 - Added: can overwrite target encoded video files.
#   2012.04.12 - v2.5.4. Added MIT license terms. Updated EXIF.py to v1.09
#   2012.04.19 - Changed the license to GPL to support the free software movement
#   2012.04.21 - Changed the startup file name
#                fixed: repeated current dir in output dir list
#                Added: 'q' to quit
#                Added: disable video transcoding if video codec is not detected
#   2012.04.22 - v2.5.5
#                Added: write-permission test for the log file
#                Added: more options for user config
#                Changed: seperate func to load config file. 
#   2012.04.25 - Changed name of a few classes. Added value validity check for configurations
#                Enhanced a few classes.
#   2012.04.26 - v2.5.6a. Not fully tested. Will add automated test suite later.
#
# Note:
#   Use python v2.4. "os.walk()" is available only after v2.4.
#===============================================================================
from RenLib import *
import standout
import os, sys, time, datetime, subprocess, shutil, getopt
import EXIF

from os.path import join, getsize, split, splitext, getatime, getmtime, getctime, exists

global Con, Cfg, GDirInfo, GFileInfo, GVideoBinDir

GDirInfo = None
GFileInfo = None
GVideoBinDir = None

ssSyncToLatestComment = 0 #sync to the comment of the first matched target file.
ssAddNewCommentOnly = 1 #sync to the comment of the matched target file only when the source has no comment.


class ConstClass:
    """Define constant settings"""
    def __init__(self):
        self.AppName = 'Photo Sorter'
        self.AppVer = '2.5.6a'
        self.AppCopyright = '(C) J Ren'
        self.AppYear = '2005-2012'

        self.Prompt1 = '==='
        self.Prompt2 = '---'
        self.Prompt3 = '...'
        self.InputPrompt = '? '
        self.ErrorPrompt = '???'
        self.AttnPrompt = '!!!'

        #self.ExePath = ''
        #self.ExeName = ''
Con = ConstClass()


def DetectVCodec(ACodecName=None):
    """=========================================================================
    Detect if video codes exists
    Note: 
    Arguments:
      ACodecName: the command name of the codec
    Return: 
      True: if the codec is found
    Example:
    ========================================================================="""
    if (ACodecName is None):
        return False
    try:
        extProc = subprocess.Popen([ACodecName], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        info = extProc.communicate() #[0]: stdout, [1]: stderr. The stderr has the info
        out = info[0]
        err = info[1]
        if out.find('Video encoder') >= 0:
            if err.find('--enable-libx264') >= 0:
                return True
            else:
                print(Con.AttnPrompt + ' H.264 support not enabled in {}'.format(ACodecName))
                return False
        else:
            print(Con.AttnPrompt + ' {} not found'.format(ACodecName))
            return False
    except:
        print(Con.AttnPrompt + ' {} not found'.format(ACodecName))
        return False
    
    
class CfgClass:
    """Define system config"""
    #valid values
    ValidVals = {
                 'VTranscodOn': [True, False],
                 'LoggingOn': [True, False],
                 'VCodec': ['libx264', 'mpeg4'],
                }
    
    def __init__(self):
        self.ConfigFname = 'PhotoSorter-config.py'
        self.LogFname = 'PhotoSorter-log.txt'
        self.VProcCmd = 'ffmpeg'
        self.VideoDir = 'video' #sub-dir to store video files
        self.VideoBinDir = '#videobin'
        
        self.DefaultInputDir = '.'
        self.InputDir = self.DefaultInputDir
        self.OutputDir = self.InputDir
        self.InputDirs = [self.InputDir]
        self.OutputDirs = [self.OutputDir]
        self.ProcessingSequence = 'None' #'None', 'PhotosFirst', 'PhotosOnly'
        
        #self.VQuality = 'sameq' #Q8
        #self.VEncExt2 = ''
        #self.VEncExt = ''
        #self.VEncCExt = ''
        self.VCodec = 'libx264'

        self.ThmCExt = '.THM.JPG'

        self.VidFileExts = ['.mov', '.mkv', '.avi', '.3gp']
        self.TmpVidFileExt2s = ['.tmp']
        self.VidCompanionFileCExts = ['.thm.jpg']
        self.ImgFileExts = ['.jpg']
        self.FnameStemSep = '-' #filename stem seperator in 20110802-P0002387.JPG
        
        self.Verbosity = 0
        self.LoggingOn = True
        self.VTranscodOn = True
        self.VidOverwriteOn = False
        
    def __setattr__(self, AName, AValue): #validity check
        if CfgClass.ValidVals.has_key(AName):
            if CfgClass.ValidVals[AName] is not None:
                if (AValue is None) or (AValue not in CfgClass.ValidVals[AName]): #failed the validity check
                    return #ignore invalid value
                
        if AName == 'InputDirs' or AName == 'OutputDirs':
            AValue = [FormatFilePath(x) for x in AValue if x is not None] #format paths
        elif AName == 'VTranscodOn':
            if AValue:
                if not DetectVCodec(self.VProcCmd):
                    AValue = False
                    print(Con.AttnPrompt + ' Video codec not found. Video transcoding disabled')
            else:
                print(Con.Prompt1 + ' Video transcoding is not enabled')
        elif AName == 'VCodec':
            if AValue == 'libx264':
                self.__dict__['VEncExt2'] = '.H24'
                self.__dict__['VEncExt'] = '.MKV'
            elif AValue == 'mpeg4':
                self.__dict__['VEncExt2'] = '.MP4'
                self.__dict__['VEncExt'] = '.MKV'
            else: #this will never happen
                raise Exception('Unsupported codec')
            self.__dict__['VEncCExt'] = self.VEncExt2 + self.VEncExt
            
        #normal way
        self.__dict__[AName] = AValue
        
Cfg = CfgClass()


class FuncNoClass:
    def __init__(self):
        self.Auto = 0
        self.JpgExtToThm = 1
        self.AddDatePrefix = 2
        self.AddJpgAfterThmExt = 3
        self.EncodeVid = 4
        self.EncodeVidAllDirs = 5
        self.SyncVidFnames = 6
        self.BinOldVidFiles = 7
        self.SyncThmFnames = 8
        self.MoveToDatedDir = 9
        self.AutoOverwrite = 10
        
    def Valid(self, AChoice=-1):
        if (AChoice >= 0) and (AChoice < len(self.__dict__)):
            return True
        else:
            return False
    
FuncNo = FuncNoClass()

#=======================================================
def main():
    """=========================================================================
    Return: error code
      0: success
      1: user aborted
    ========================================================================="""
    global Con, Cfg, GVideoBinDir

    """args = GetCmdLineArgs()
    if args != 0:
        execfile(args.ConfigFile)
    else:
        print 'Config file missing'
        return"""

    print(' ')
    print(' '.join([Con.Prompt1, Con.AppName, Con.AppVer, Con.AppCopyright, Con.AppYear]))
    Con.ExePath, Con.ExeName = os.path.split(os.path.abspath(sys.argv[0]))

    print('Function list:')
    print('   0-Auto;')
    print('   1-Change the ext of companion .JPG files of .MOV files to .THM;')
    print('   2-Add date prefix to filenames;')
    print('   3-Add .JPG after .THM;')
    print('   4-Transcode video files but skip dated dirs;')
    print('   5-Transcode video files in all dirs;')
    print('   6-Sync video filename to the orig or old transcoded filename in video dirs;')
    print('   7-Bin redundant original & outdated transcoded video files in video dirs;')
    print('   8-Sync THM filename to the video filename in video dirs;')
    print('   9-Move files to dated directories;')
    print('   10-Auto but overwrite existing destination transcoded video files;')
    print('   (Seperate multiple functions by comma. Enter \"q\" to quit at any time)')

    while True:
        ques = 'Which function [0]'
        ans = raw_input(ques + Con.InputPrompt)
        if len(ans) <= 0:
            ans = '0'
        ans = ans.split(',') #convert a string to a list

        #convert actions to a list of numbers:
        progFuncs = []
        wrongAns = False
        for aAns in ans:
            try:
                if aAns == 'q': #quit
                    return
                progFunc = eval(aAns)
            except:
                print(Con.ErrorPrompt + 'Error! function number must be a number!')
                #sys.exit(0)
                wrongAns = True
                break

            if not FuncNo.Valid(progFunc):
                print(Con.ErrorPrompt + ' Error! No such option!')
                #sys.exit(0)
                wrongAns = True
                break
            progFuncs = progFuncs + [progFunc]
        if wrongAns:
            print('')
            continue
        else:
            break

    #Load external user config file:
    configFname = join(os.getcwd(), Cfg.ConfigFname)
    LoadConfigFile(configFname)
        
    Cfg.InputDir = AskDir('Input dir (0-9 or path)[0]' + Con.InputPrompt, Cfg.InputDirs)
    if Cfg.InputDir is None:
        return 1
    
    #add the input dir to the shortcuts:
    if Cfg.InputDir in Cfg.OutputDirs:
        Cfg.OutputDirs.remove(Cfg.InputDir)
    Cfg.OutputDirs.insert(0, Cfg.InputDir)

    Cfg.OutputDir = AskDir('Output dir (0-9 or path)[0=same as input]' + Con.InputPrompt, Cfg.OutputDirs)
    if Cfg.OutputDir is None:
        return 1
    GVideoBinDir = join(Cfg.InputDir, Cfg.VideoBinDir)

    print(Con.Prompt1 + ' Input dir:  ' + Cfg.InputDir)
    print(Con.Prompt1 + ' Output dir: ' + Cfg.OutputDir)
    ques = 'Start processing? [y]'
    ans = raw_input(ques + Con.InputPrompt)
    if len(ans) <= 0:
        ans = 'y'
    if ans == 'y':
        pass
    else:           
        return 1

    #Set up log files:    
    #logFname = join(Cfg.OutputDir, 'photosorter-log.txt')
    #args = GetCmdLineArgs()
    #if args != None:
        #logFname = join(args['AppPath'], 'photosorter-log.txt')
    #else:
        #print(Con.ErrorPrompt + ' Error: AppPath is None')
        #exit(1)
    if Cfg.LoggingOn:
        logFname = join(os.getcwd(), Cfg.LogFname)
        try: #write-permission test
            logf = open(logFname, "w")
            #logf.write('PhotoSorter Log File')
        except IOError as exc:
            Cfg.LoggingOn = False
            print(Con.ErrorPrompt + ' Unable to write to log file \"{}\". {}'.format(logFname, exc[1]))
            print(Con.AttnPrompt + ' Logging disabled')
        else:
            logf.close()
            #if exists(logFname):
                #os.remove(logFname)
            MyStdout = StandOut(filename=logFname)
            MyStderr = StandOut(stream='error', share=True) #anything printed to sys.stderr goes to the stdout file as well 

    print('')
    PrintAppHeader(Con.AppName, Con.AppVer, Con.AppCopyright, Con.AppYear)
    #print('')

    for progFunc in progFuncs:
        if progFunc == FuncNo.AutoOverwrite:
            Cfg.VidOverwriteOn = True
            progFunc = FuncNo.Auto
        elif progFunc == FuncNo.Auto:
            Cfg.VidOverwriteOn = False
        
        skipDatedDir = True        
        if (progFunc == FuncNo.EncodeVidAllDirs):
            skipDatedDir = False    

        if (progFunc == FuncNo.JpgExtToThm) or (progFunc == FuncNo.Auto):
            count = ProcRenameMovJpgPair(Cfg.InputDir)
            print('')
            print('------------------------------------------------')
            print(Con.Prompt1 + ' ProcRenameMovJpgPair:')
            print Con.Prompt1, count, 'companion files of .MOV processed.'
            print('================================================')
            print('')
            if progFunc == FuncNo.JpgExtToThm:
                continue

        if (progFunc == FuncNo.SyncVidFnames):
            targetCExts = ['.mp4.mkv', '.xvd.avi', '.dvx.avi', '.avi', '.mov']
            count, redundantCnt, multiTargetsCnt, errCnt = ProcSyncVideoFnames(Cfg.InputDir, Cfg.VEncCExt, targetCExts, ssAddNewCommentOnly)
            print('')
            print('------------------------------------------------')
            print(Con.Prompt1 + ' ProcSyncVideoFnames:')
            print(Con.Prompt1 + ' %i video files synced.' % (count))
            print(Con.Prompt1 + ' %i redundanct video files found.' % (redundantCnt))
            print(Con.Prompt1 + ' %i multiple target comments found.' % (multiTargetsCnt))
            print(Con.Prompt1 + ' %i errors.' % (errCnt))
            print('================================================')
            print(' ')
            continue

        if (progFunc == FuncNo.BinOldVidFiles):
            encodedVidCExts = ['.h24.mkv', '.mp4.mkv', '.xvd.avi', '.dvx.avi']
            origVidCExts = ['.avi', '.mov']
            processedCnt, existTargetsCnt, conflictsCnt, newCommentCnt, errCnt = ProcBinRedundantVideoFiles(Cfg.InputDir, encodedVidCExts, origVidCExts)
            print('')
            print('------------------------------------------------')
            print(Con.Prompt1 + ' ProcBinRedundantVideoFiles:')
            print(Con.Prompt1 + ' %i redundant video files bined.' % (processedCnt))
            print(Con.Prompt1 + ' %i existing target files skipped.' % (existTargetsCnt))
            print(Con.Prompt1 + ' %i conflicting comments found.' % (conflictsCnt))
            print(Con.Prompt1 + ' %i new comments found.' % (newCommentCnt))
            print(Con.Prompt1 + ' %i errors.' % (errCnt))
            print('================================================')
            print(' ')
            continue

        if (progFunc == FuncNo.SyncThmFnames):
            targetCExts = ['.h24.mkv', '.mp4.mkv', '.xvd.avi', '.dvx.avi', '.avi', '.mov']
            count, redundantCnt, multiTargetsCnt, errCnt = ProcSyncVideoFnames(Cfg.InputDir, Cfg.ThmCExt, targetCExts, ssSyncToLatestComment)
            print('')
            print('------------------------------------------------')
            print(Con.Prompt1 + ' ProcSyncVideoFnames:')
            print(Con.Prompt1 + ' %i THM files synced.' % (count))
            print(Con.Prompt1 + ' %i redundanct THM files found.' % (redundantCnt))
            print(Con.Prompt1 + ' %i multiple target comments found.' % (multiTargetsCnt))
            print(Con.Prompt1 + ' %i errors.' % (errCnt))
            print('================================================')
            print(' ')
            continue

        #progFunc == Auto or the rest:
        if (Cfg.ProcessingSequence == 'PhotosFirst') or (Cfg.ProcessingSequence == 'PhotosOnly'): #Process photos first
            count, results = ProcessFiles(progFunc, Cfg.InputDir, Cfg.OutputDir, FileType='.jpg', ASkipDatedDir=skipDatedDir)
            PrintResultCnt(count, results)

        if Cfg.ProcessingSequence != 'PhotosOnly':
            count, results = ProcessFiles(progFunc, Cfg.InputDir, Cfg.OutputDir, FileType=None, ASkipDatedDir=skipDatedDir) #Process all files
            PrintResultCnt(count, results)

    PrintAppFooter(Con.AppName, Con.AppVer, Con.AppCopyright, Con.AppYear)
    if Cfg.LoggingOn:
        MyStdout.close()
        MyStderr.close()
        print(Con.Prompt1 + ' Messages logged to \"{}\"'.format(Cfg.LogFname))

    return 0


def PrintResultCnt(count=0, results=None):
    """=========================================================================
    Print the counts of the number of files being processed
    ========================================================================="""
    print ('')
    print(Con.Prompt1 + ' %i files processed in total.'  % (count))

    if sum(results['FnAddDatePrefix']) > 0:
        print('------------------------------------------------')
        print(Con.Prompt1 + ' FnAddDatePrefix:')
        print(Con.Prompt1 + ' %i files added with date-prefix.'  % (results['FnAddDatePrefix'][0]))

    if sum(results['FnAddJpgSuffix']) > 0:
        print('------------------------------------------------')
        print(Con.Prompt1 + ' FnAddJpgSuffix:')
        print(Con.Prompt1 + ' %i THM files added with JPG suffix.'  % (results['FnAddJpgSuffix'][0]))

    if sum(results['FnEncodeVideo']) > 0:
        print('------------------------------------------------')
        print(Con.Prompt1 + ' FnEncodeVideo:')
        print(Con.Prompt1 + ' %i video files transcoded.'  % (results['FnEncodeVideo'][0]))
        if Cfg.VidOverwriteOn:
            print(Con.Prompt1 + ' %i existing target files to be overwritten.'  % (results['FnEncodeVideo'][1]))
        else:
            print(Con.Prompt1 + ' %i existing target files skipped.'  % (results['FnEncodeVideo'][1]))

    if sum(results['FnMoveToDatedDir']) > 0:
        print('------------------------------------------------')
        print(Con.Prompt1 + ' FnMoveToDatedDir:')
        print(Con.Prompt1 + ' %i files moved to dated dirs.'  % (results['FnMoveToDatedDir'][0]))
        if Cfg.VidOverwriteOn:
            print(Con.Prompt1 + ' %i existing target files overwritten.'  % (results['FnMoveToDatedDir'][1]))
        else:
            print(Con.Prompt1 + ' %i existing target files skipped.'  % (results['FnMoveToDatedDir'][1]))
        print(Con.Prompt1 + ' %i redundant video files binned.'  % (results['FnMoveToDatedDir'][2]))
        print(Con.Prompt1 + ' %i errors.'  % (results['FnMoveToDatedDir'][3]))

    print('================================================')
    print (' ')

#================================================================================
def GetCmdLineArgs():
    """=========================================================================
    Get command line arguments
    Return:
       command line arguments dict.
       or 0 if there is an error.    
    ========================================================================="""
    #All init must be None, or it will overwrite the defaults
    cmdLineOpts = {'AppPath': None, 
                   'AppName': None,
                   'ConfigFile': None
                   }

    #if len(sys.argv) < 2:
    #    return None
    try:
        optsList, args = getopt.getopt(sys.argv[1:], 'hc:')
    except getopt.GetoptError:
        return None

    cmdLineOpts['AppPath'], cmdLineOpts['AppName'] = os.path.split(os.path.abspath(sys.argv[0]))

    #Parse command line arguments:   
    for opt, optValue in optsList:
        if opt in ["-h"]: #Help
            #PrintUsage()
            sys.exit()
        elif opt in ["-c"]:  #config file. Must exist.
            cmdLineOpts['ProcessConfigurationFile'] = optValue
        elif opt in ["-i"]:  
            cmdLineOpts['InputDefinitionFile'] = optValue
        elif opt in ["-o"]:  
            cmdLineOpts['OutputDefinitionFile'] = optValue
        elif opt in ["-w"]:  
            cmdLineOpts['WorkflowDefinitionFile'] = optValue
        elif opt in ["-t"]:  #-t <number>: 0: test mode off; 1: test mode on
            cmdLineOpts['TestMode'] = eval(optValue)
        elif opt in ["-d"]:  #-d [start | stop | restart | status]: daemon mode (Linux only)
            cmdLineOpts['Daemon'] = optValue
            if optValue == '1':
                cmdLineOpts['Daemon'] = 'start'
            elif optValue == '0':
                cmdLineOpts['Daemon'] = 'stop'
        else:
            Print ("??? Unknown option: " + optValue)
            exit(1)

    if cmdLineOpts.has_key('ConfigFile'):
        return cmdLineOpts
    else:
        return None


def AskDir(APrompt='Which dir? ', ADefaults=['']):
    """=========================================================================
    Return: the dir answered
        None: if 'q' command received to indicate 'quit'
    Parameters:
        ADefaults: list of default dirs
    ========================================================================="""
    while True:
        maxIdx = len(ADefaults)
        if maxIdx > 0:
            print('')
            print('Pre-defined dir shortcuts:')
            for idx in range(maxIdx):
                print('   %i-\"%s\"' % (idx, ADefaults[idx]))

        inputDir = raw_input(APrompt)
        if len(inputDir) == 0: #use the first default
            inputDir = ADefaults[0]
        elif len(inputDir) <= 2: #check if it should use defaults
            if inputDir.isdigit(): #use default
                if int(inputDir) < maxIdx:
                    inputDir = ADefaults[int(inputDir)]
                else:
                    print(Con.ErrorPrompt + ' Shortcut number out of range. Try again.')
                    continue
            elif inputDir == 'q': #quit
                return None
            else: #ignore unknown input
                pass
        else: #user input
            pass
        inputDir = FormatFilePath(inputDir)
        print ' '

        #check if the input dir is correct:
        if exists(inputDir):
            print Con.Prompt1, 'Contents of the dir: '
            for contents in os.listdir(inputDir):
                print('   ' + contents)
            ans1 = raw_input('Is the dir \"' + inputDir + '\" correct [y]' + Con.InputPrompt)
            if ((len(ans1) == 0) or (ans1.lower() == "y") or (ans1.lower() == "yes")):
                pass
            elif ans1 == 'q': #quit
                return None
            else: #ignore unknown input
                print("");
                continue
        else:
            print(Con.ErrorPrompt + ' The dir \"' + inputDir + '\" does NOT exist.')
            continue

        print(' ')
        return inputDir

    
def LoadConfigFile(AFname=None):
    """=========================================================================
    Load config file and merge settings into cfg
    
    ========================================================================="""
    global Cfg
    
    if AFname is None:
        return
    UserConfig = {}
    if exists(AFname):
        execfile(AFname)

    Cfg.InputDirs = UserConfig.get('InputDirs')
    Cfg.OutputDirs = UserConfig.get('OutputDirs')
    Cfg.VTranscodOn = UserConfig.get('EnableVideoTranscoding')
    Cfg.LoggingOn = UserConfig.get('EnableLogging')
    

def GetFnameComponents(Fname=None):
    """=========================================================================
    Return:
      datePrefix: 
        ok: the date prefix. Auto detects the prefix is 6 or 8 digits format. 
        error: Is empty string '' if no date prefix exists.
    Example return:
      20070724-P1010289-tea.THM.JPG:
        path: ''
        datePrefix: '20070724'
        base: '20070724-P1010289-tea.THM'
        ext: '.JPG'
        base2: '20070724-P1010289-tea'
        ext2: '.THM'
        stem: '20070724-P1010289'
    Note:
      6 digits date format: 971203
      8 digits date format: 19971203
    Example:
      path, datePrefix, base, ext, base2, ext2, stem = GetFnameComponents(filename)
    ========================================================================="""
    if Fname is None:
        return '', '', '', '', '', ''
    else:
        path, fname = split(Fname)
        base, ext = splitext(fname)
        base2, ext2 = splitext(base)
        parts = base2.split(Cfg.FnameStemSep)
        if len(parts) >= 2:
            stem = parts[0] + Cfg.FnameStemSep + parts[1]
        else:
            stem = base2

        #o#if GetDatePrefix(base2[0:8]): #check if it's the new 8 digits format
            #datePrefix = base2[0:8]
        #elif GetDatePrefix(base2[0:6]): #check it's the old 6 digits format first
            #datePrefix = base2[0:6]
        #else:
            #datePrefix = ''
        datePrefix = GetDatePrefix(fname)

        return path, datePrefix, base, ext, base2, ext2, stem


def ProcRenameMovJpgPair(InputDir=None):
    """=========================================================================    
    If a .MOV file is found, find its companion .JPG file and change the ext
    to .THM 
    ========================================================================="""
    global Con
    count = 0

    if (InputDir == None):
        return 0
    for root, dirs, files in os.walk(InputDir):
        if Cfg.Verbosity >= 1:
            print Con.Prompt1, 'Directory \"' + root + '\\\"',
            print 'contains', len(files), "non-directory files."
            print ' '

        for fname in files: #eg: P100.THM.JPG
            path, datePrefix, base, ext, base2, ext2, stem = GetFnameComponents(fname)
            ext = ext.lower() #the 1st extension, eg: .JPG

            processed = 0

            if ext == '.mov':            
                companFname1 = base + '.JPG'
                companFname2 = base + '.jpg'
                completeCompanFname1 =  join(root, companFname1)
                completeCompanFname2 =  join(root, companFname2)
                if exists(completeCompanFname1):
                    companFname = companFname1
                    completeCompanFname = completeCompanFname1
                elif exists(completeCompanFname2):
                    companFname = companFname2
                    completeCompanFname = completeCompanFname2
                else:
                    completeCompanFname = None
                if completeCompanFname != None:
                    completeFname = join(root, fname)
                    if not exists(completeFname):
                        continue

                    if not processed: #Print header only when no previous print    
                        fInfo = GetFileInfoStr(completeFname)
                        print fInfo

                    newFname = base + '.THM' #change P100.JPG to 'P100.THM'
                    print Con.Prompt3, 'Rename', companFname, 'to ', '\"' + newFname + '\"'
                    completeNewFname = join(root, newFname)
                    fileAccessTime = getatime(completeCompanFname)
                    fileModTime = getmtime(completeCompanFname)
                    os.rename(completeCompanFname, completeNewFname)
                    SetFileAccModTime(completeNewFname, Con.Prompt3 + ' Sync the acc/mod time to the original', fileAccessTime, fileModTime)
                    ##SyncFileModTime(completeNewFname, ' Sync the mod time to the original', fileModTime)
                    processed = 1
            if processed:
                count = count + 1
                print ' '

    return count

def GenerateDatePrefixFromExif(Filename=None):
    """Get photo date from EXIF"""
    if Filename == None:
        return ''

    f = open(Filename, 'rb')
    tags = EXIF.process_file(f, debug=0)
    #for tag in tags.keys(): #Check tags
        #if tag not in ['JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote']:
        #if tag == 'EXIF DateTimeOriginal':
            #print "Key: %s; value: %s" % (tag, tags[tag])

    if tags.has_key('EXIF DateTimeOriginal'):
        photoDate = str(tags['EXIF DateTimeOriginal'])
        filePrefix = photoDate[0:4] + photoDate[5:7] + photoDate[8:10]
    else:
        filePrefix = None

    return filePrefix

def GenerateDatePrefix(Filename=None):
    if Filename == None:
        return ''
    datePrefix = None

    nameAndExt = splitext(Filename)
    ext = nameAndExt[1].lower()
    if (ext == '.jpg' or ext == '.thm'): #Get date from EXIF
        datePrefix = GenerateDatePrefixFromExif(Filename)
    if datePrefix is None: #Get date from modification time for non-jpg or non-exif files
        mt = getmtime(Filename)
        mt = time.gmtime(mt) #time.localtime() will give wrong time
        datePrefix = ('%04u%02u%02u' % (mt[0], mt[1], mt[2]))

    return datePrefix

def GetFileInfoStr(Filename): #Get file name and size for title printing
    if not exists(Filename):
        return 'File not exists'
    if not os.path.isfile(Filename):
        return 'Not a file'

    fsize = getsize(Filename)
    if fsize > 1000000:
        fInfo = '%s \"%s\"; %5.3f%s' % (Con.Prompt2, Filename, fsize/1000000.0, 'MB')
        #print fInfo
    else:
        fInfo = '%s \"%s\"; %5.3f%s' % (Con.Prompt2, Filename, fsize/1000.0, 'KB')
    return fInfo


def IsDateStr(DateStr=''):
    """#2011.06.26 - removed support for the old date str
    if (len(DateStr) == 6): #For old 6 digit format: 071023
        try:
            yearn = int(DateStr[0:2], 10) 
        except: #For non-numbers, an exception will be raised
            return False

        try:
            monthn = int(DateStr[2:4], 10)
            if monthn < 1 or monthn > 12:
                return False
        except: #For non-numbers, an exception will be raised
            return False

        try:
            dayn = int(DateStr[4:6], 10)
            if dayn < 1 or dayn > 31:
                return False
        except: #For non-numbers, an exception will be raised
            return False

        return True
    """
    if (len(DateStr) == 8): #For new 8 digit format: 20071023
        try:
            yearn = int(DateStr[0:4], 10)
            if yearn < 1900 or yearn > datetime.date.today().year:
                return False
        except: #For non-numbers, an exception will be raised
            return False

        try:
            monthn = int(DateStr[4:6], 10)
            if monthn < 1 or monthn > 12:
                return False
        except: #For non-numbers, an exception will be raised
            return False

        try:
            dayn = int(DateStr[6:8], 10)
            if dayn < 1 or dayn > 31:
                return False
        except: #For non-numbers, an exception will be raised
            return False

        return True

    else:
        return False

#A date dir is like '20071021' //ob/or '071021'
def IsDateDir(DirName=''):
    if len(DirName) < 6:
        return False
    if len(DirName) >= 8: #check using new format: '20071023'
        return IsDateStr(DirName[0:8])
    #if IsDateStr(DirName[0:6]): #Check using old format '071021'
    #    return True
    else:
        return False

def GetDatePrefix(BaseName=''):
    """=========================================================================
    History: 2011.06.26 - removed support for the old format.
    Note: A date prefix is like (new format) '20071021-xxx' or (old format) '071021xxx'
    Return: automatically return 8 or 6 digit date prefix, or '' if none exists.
    ========================================================================="""
    if len(BaseName) < 8:
        return ''
    if (BaseName.find('-') == 8): #check if it's new format: 20071023-
        if IsDateStr(BaseName[0:8]):
            return BaseName[0:8]
    #if IsDateStr(BaseName[0:6]): #Check using old format
    #    return BaseName[0:6]

    return ''


def IsValidExt(FileExt):
    """=========================================================================
    Check if the file type (extersion) is a recognized one.
    Arguments:
      FileExt: file extension name, including the leading '.'.
    Return: True or False
    Example:

    ========================================================================="""
    FileExt = FileExt.lower()
    if (FileExt=='.jpg' or FileExt=='.avi' or FileExt=='.thm' or FileExt=='.mov' \
        or FileExt=='.3gp'):
        return True
    else:
        return False


def PrintFileInfo():
    """=========================================================================

    ========================================================================="""
    global GDirInfo, GFileInfo

    if GDirInfo != None:
        print(' ')
        print(GDirInfo)
        GDirInfo = None

    if GFileInfo != None:
        print(' ')
        print(GFileInfo)
        GFileInfo = None


def FnAddDatePrefix(ARoot, Fname):
    """=========================================================================
    Add a date prefix to the filename.
    Note: A date prefix is like '20071021-xxx' or '071021xxx'
    Arguments:
      Fname: filename.
    Return: 
      Fname, RProcessedCnt
    Example:
      name, processed = AddDatePrefix(root, name, processed)
    ========================================================================="""
    RProcessedCnt = 0
    fullname = join(ARoot, Fname)   
    path, datePrefix, base, ext, base2, ext2, stem = GetFnameComponents(Fname)

    #Get correct sub-dir name for avi and jpg respectively:
    parentDir = split(split(ARoot)[0])[1]
    parentRoot = split(split(ARoot)[0])[0]
    curDir = split(ARoot)[1]

    if IsValidExt(ext) \
       and not( (curDir == Cfg.VideoDir) and IsDateDir(parentDir) ): #don't dig into special dir
        if len(datePrefix) > 0: #date prefix exists    
            PrintFileInfo()
            print Con.Prompt3, 'Date prefix already exists. Skip.'
        else: #add date prefix
            PrintFileInfo()
            fullname = join(ARoot, Fname)
            datePrefix = GenerateDatePrefix(fullname)
            newName = path + datePrefix + '-' + base + ext
            PrintFileInfo()
            print Con.Prompt3, 'Rename to', '\"' + newName + '\"'
            newNameFull = join(ARoot, newName)
            fileAccessTime = getatime(fullname)
            fileModTime = getmtime(fullname)
            os.rename(fullname, newNameFull)
            SetFileAccModTime(newNameFull, Con.Prompt3 + ' Sync the acc/mod time to the original', fileAccessTime, fileModTime)
            ##SyncFileModTime(newNameFull, ' Sync the mod time to the original', fileModTime)
            Fname = newName
            RProcessedCnt = 1

    return Fname, RProcessedCnt    

def FnAddJpgSuffix(ARoot, Fname):
    """=========================================================================
    Add .jpg suffix to the thumbnail file extension .thm.
    Note: A thumbnail filename is like 'xxx.THM'
    Arguments:
      Fname: filename.
    Return: 
      Fname, Processed
    Example:
      name, processed = AddDatePrefix(root, name, processed)
    ========================================================================="""
    RProcessedCnt = 0
    fullname = join(ARoot, Fname)
    #Already done in the caller, so redundent:
    #if not exists(fullname):
        #if not Processed: #Print header only when not previously print
                #PrintFileInfo()
                #Processed = 1
        #print Con.ErrorPrompt, 'File not found. Skip.'
        #return Fname, Processed 

    path, datePrefix, base, ext, base2, ext2, stem = GetFnameComponents(Fname)
    if ext.lower() == '.thm':           
        PrintFileInfo()
        newName = Fname + '.JPG'
        print Con.Prompt3, 'Rename to', '\"' + newName + '\"'
        newNameFull = join(ARoot, newName)
        fileAccessTime = getatime(fullname)
        fileModTime = getmtime(fullname)
        os.rename(fullname, newNameFull)
        SetFileAccModTime(newNameFull, Con.Prompt3 + ' Sync the acc/mod time to the original', fileAccessTime, fileModTime)
        ##SyncFileModTime(newNameFull, ' Sync the mod time to the original', fileModTime)

        RProcessedCnt = 1
        #Update filename to new name to be used below:
        Fname = newName

    return Fname, RProcessedCnt 

def FnMoveToDatedDir(ARoot, Fname, AOutputDir, AVideoBinDirFull, AFileAccessTime, AFileModTime):
    """======================================================
    Note: FnEncodeVideo may return one or two filenames in Fname. In later case it includes original and re-encoded. The
          original filename is empty if the re-encoded file exists in the target location.
    AVideoBinDirFull: the unneeded original video file will be moved into this dir.
    ========================================================="""
    RMovedCnt = 0
    RExistingTgtCnt = 0
    RBinnedCnt = 0
    RErrCnt = 0

    #check the type of input name: single fname or multiple
    if isinstance(Fname, (tuple, list)): #process multiple files
        if len(Fname) != 2: #wrong number of video file names
            PrintFileInfo()
            print(Con.ErrorPrompt + ' Critical Error: Number of video file names is not 2')
            exit(1)

        reencodedFile = Fname[1]
        origFile = Fname[0]
        if len(reencodedFile) > 0:
            PrintFileInfo()
            print(Con.Prompt3 + (' Transcoded file: \"') + reencodedFile + '\"')
            Fname, RMovedCnt, RExistingTgtCnt, RErrCnt = MoveToDatedDirSingle(ARoot, reencodedFile, AOutputDir, AFileAccessTime, AFileModTime)

        #move the unneeded original file to the bin:
        if len(origFile) > 0:
            PrintFileInfo()
            print(Con.Prompt3 + (' Redundant original file: \"') + origFile + '\"')

            if ARoot.find(Cfg.VideoBinDir) >= 0: #if under #video dir, then don't move
                print(Con.Prompt3 + ' Already in dir ' + Cfg.VideoBinDir + '. No need to move. Skip.')
            else:
                fullname = join(ARoot, origFile)
                if not exists(fullname):
                    PrintFileInfo()
                    print(Con.ErrorPrompt + ' File not found. Skip.')
                    RErrCnt += 1
                if not exists(AVideoBinDirFull): #Create dir if not exists
                    print(Con.Prompt3 + ' Create new dir \"' + AVideoBinDirFull + '\"')
                    os.makedirs(AVideoBinDirFull)

                targetFile = join(AVideoBinDirFull, origFile)
                #print targetFile
                if exists(targetFile):
                    #ans = raw_input('Target file already exists, overwrite' + Con.InputPrompt)
                    print(Con.Prompt3 + ' Target file \"' + targetFile + '\" already exists. Skip.')
                    RExistingTgtCnt = 1
                else: #Target file not exists, move file
                    print(Con.Prompt3 + ' Move to \"' + AVideoBinDirFull + os.sep + '\"')
                    os.rename(fullname, targetFile)
                    RBinnedCnt += 1
                    SetFileAccModTime(targetFile, Con.Prompt3 + ' Sync the acc/mod time to the original', AFileAccessTime, AFileModTime)
                    ##SyncFileModTime(targetFile, Con.Prompt3 + ' Sync the mod time to the original', AFileModTime)

    else: #one file
        Fname, RMovedCnt, RExistingTgtCnt, RErrCnt = MoveToDatedDirSingle(ARoot, Fname, AOutputDir, AFileAccessTime, AFileModTime)

    return Fname, RMovedCnt, RExistingTgtCnt, RBinnedCnt, RErrCnt

def GetTargetDir(ACurDir, ADatePrefix, AIsVideo):
    """=========================================================================
    Get the target dir for video and image files

    Arguments:
      ACurDir: the current dir relative to the input dir.
    Return: 
      RTargetDir: dir relative to the input dir.
      RDifferent: if the target dir the same as the current dir.
    Example:
      RTargetDir, RDifferent = GetVideoFileTargetDir(subDir)
    ========================================================================="""
    global Cfg

    dirParts = split(ACurDir)
    curDir = dirParts[1]
    parentPath = dirParts[0]
    parentParts = split(parentPath)
    parentDir = parentParts[1]
    #parentRoot = parentParts[0]

    if AIsVideo: #For video files      
        if (len(parentDir) >= 8) and (parentDir[0:8] == ADatePrefix): #parent dir like: 20110403
            if curDir == Cfg.VideoDir: #in dir like: 20110403/video
                RTargetDir = ACurDir
                RDifferent = False
            else: #like 051029\xyz\fname.avi
                RTargetDir = join(parentPath, Cfg.VideoDir)
                RDifferent = True
        elif (len(curDir) >= 8) and (curDir[0:8] == ADatePrefix):
            RTargetDir = join(ACurDir, Cfg.VideoDir)
            RDifferent = True
        else:
            RTargetDir = join(ACurDir, ADatePrefix, Cfg.VideoDir)
            RDifferent = True

    else: #For image files
        if (len(curDir) >= 8) and (curDir[0:8] == ADatePrefix):
            RTargetDir = ACurDir
            RDifferent = False
        else:
            RTargetDir = join(ACurDir, ADatePrefix)
            RDifferent = True

    return RTargetDir, RDifferent

def GetRealVideoDirFname(AVidDirFull, AVidFname, AFnameStem, ADatePrefix, ACExt):
    """=========================================================================
    Search for the video dir where the video file's thm file resides
    ========================================================================="""
    global Cfg

    RVidDir = AVidDirFull
    RVidFname = AVidFname

    dirParts = split(AVidDirFull)
    curDir = dirParts[1]
    parentPath = dirParts[0]
    parentParts = split(parentPath)
    parentDir = parentParts[1]
    parentRoot = parentParts[0]

    if (curDir == Cfg.VideoDir) and (len(parentDir) >= 8) and (parentDir[0:8] == ADatePrefix): #find new dir/fname only when the path is the right type
        candidateVFnames = []
        items = os.listdir(parentRoot)
        for aItem in items:
            if os.path.isdir(join(parentRoot, aItem)):
                if (len(aItem) >= 8) and (aItem[0:8] == ADatePrefix):
                    newDir = join(parentRoot, aItem, Cfg.VideoDir)
                    if exists(newDir):
                        finalVidDir = ''
                        finalVidFnames = []
                        items2 = os.listdir(newDir)
                        for aItem2 in items2:
                            if aItem2.find(AFnameStem) >= 0:
                                if (len(aItem2) >= 8) and (os.path.isfile(join(newDir, aItem2))): #make sure file name have at least 8 chars
                                    cext = aItem2[-8:].lower()
                                    if (cext == Cfg.ThmCExt.lower()) and (not finalVidDir): 
                                        finalVidDir = newDir #the 1st dir with the thm is the dest dir
                                    elif (cext == Cfg.VEncCExt.lower()) and (len(aItem2[:-8]) > len(AFnameStem)): #fname with comment
                                        if aItem2 != AVidFname: #different comment from the default
                                            finalVidFnames.append(aItem2) #only record fnames with comment and different from the default
                        #end for aItem2

                        if finalVidDir: #choose the vid fname only when this dir is the real one
                            RVidDir = finalVidDir
                            if finalVidFnames:
                                RVidFname = finalVidFnames[0] #only the 1st is the dest. The rest are redundant
                            return RVidDir, RVidFname #dir found. Can return now
                        else: #continue to check outher dirs
                            if finalVidFnames:
                                candidateVFnames.append([newDir, finalVidFnames])
        #end for aItem
        
        #no dest dir found, figure out the best VFname to use:
        if candidateVFnames: #use the 1st candidate. The rest is redundant
            RVidDir = candidateVFnames[0][0]
            RVidFname = candidateVFnames[0][1][0]
            
    return RVidDir, RVidFname



def MoveToDatedDirSingle(ARoot, Fname, AOutputDir, AFileAccessTime, AFileModTime):
    """=========================================================================
    Move file to dated directory
    Note: Only process known file extensions such as .jpg, .avi, .mov, .3gp .
    Arguments:
      Fname: filename without root path.
    Return: 
      Fname, Processed
    Example:
      name, processed = MoveToDatedDirSingle(root, name, processed, fInfo)
    ========================================================================="""
    global Cfg

    RMovedCnt = 0
    RExistingTgtCnt = 0
    RErrCnt = 0

    subDir = ARoot[ARoot.find(Cfg.InputDir) + len(Cfg.InputDir):]
    fullname = join(ARoot, Fname)

    if not exists(fullname):
        PrintFileInfo()
        print(Con.ErrorPrompt + ' File not found. Skip.')
        RErrCnt += 1
        return Fname, RMovedCnt, RExistingTgtCnt, RErrCnt

    isPhoto = False
    isVideo = False
    isVideoCompanion = False
    path, datePrefix, base, ext, base2, ext2, stem = GetFnameComponents(Fname)
    extLo = ext.lower()
    ext2Lo = ext2.lower()
    cextLo = ext2Lo + extLo
    if (extLo in Cfg.VidFileExts) and not (ext2Lo in Cfg.TmpVidFileExt2s):
        isVideo = True
    if (cextLo in Cfg.VidCompanionFileCExts): #xx.thm.jpg is moved to video dir
        isVideoCompanion = True
        isVideo = True
    elif (extLo in Cfg.ImgFileExts): 
        isPhoto = True

    if (isPhoto or isVideo or isVideoCompanion): #Process only photo and video files
        if not datePrefix:
            datePrefix = GenerateDatePrefix(fullname)

        newTargetDir, isDifferent = GetTargetDir(subDir, datePrefix, isVideo)
        newCurDir = join(AOutputDir, newTargetDir)
        if isVideo and (not isVideoCompanion):
            newCurDir, Fname = GetRealVideoDirFname(newCurDir, Fname, stem, datePrefix, Cfg.VEncCExt)

        if (newCurDir == ARoot):
            doMove = False
        else:
            doMove = True

        if doMove:
            #print 'fullname: ', fullname
            PrintFileInfo()

            if not exists(newCurDir): #Create dir if not exists
                print(Con.Prompt3 + ' Create new dir \"' + newCurDir + '\"')
                #if not exists(newParentDir):
                    #os.makedirs(newParentDir)
                os.makedirs(newCurDir)

            targetFile = join(newCurDir, Fname)
            #print targetFile
            doMove2 = True
            if exists(targetFile):
                if not Cfg.VidOverwriteOn:
                    #ans = raw_input('Target file already exists, overwrite' + Con.InputPrompt)
                    print(Con.Prompt3 + ' Target file \"' + targetFile + '\" already exists. Skip.')
                    RExistingTgtCnt += 1
                    doMove2 = False
                else:
                    print(Con.Prompt3 + ' Target file \"' + targetFile + '\" already exists. Overwrite.')
                    RExistingTgtCnt += 1
                    
            if doMove2: #Target file not exists, move file
                print Con.Prompt3, 'Move to \"' + newCurDir + os.sep + '\"'
                #This doesn't work for cross-device move #os.rename(fullname, targetFile)
                #Use shutil.move
                if GetCurrentOs() == 'Linux': #work around shutil error on samba
                    ret = MoveFile(fullname, targetFile)
                    #if Cfg.Verbosity >= 3:
                    if ret[0]: #stdout
                        print(ret[0])
                    if ret[1]: #stderr
                        print(ret[1])
                else:
                    shutil.move(fullname, targetFile) #error for samba
                RMovedCnt += 1
                SetFileAccModTime(targetFile, Con.Prompt3 + ' Sync the acc/mod time to the original', AFileAccessTime, AFileModTime) #reset file access and mod time
                ##SyncFileModTime(targetFile, Con.Prompt3 + ' Sync the mod time to the original', AFileModTime)

    return Fname, RMovedCnt, RExistingTgtCnt, RErrCnt


#============================================================================
def GetVideoFileInfo(AFullFname=None):
    """=========================================================================
    Use ffmpeg to get the video file info.
    Note: 
    Arguments:
      AFullFname: filename with complete path.
    Return: 
      FrameRate if found, or None.
      FrameSize: (width, height)
      PixelFormat: 
    Example:
      frameRate, frameSize, pixelFormat = GetVideoFileInfo(fname)
    ========================================================================="""
    if (AFullFname == None) or (not exists(AFullFname)):
        return None, None, None

    extProc = subprocess.Popen(['ffmpeg', '-i', AFullFname], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    infos = extProc.communicate()[1] #[0]: stdout, [1]: stderr. The stderr has the info

    for aToken in ['Stream #0.0', 'Stream #0:0']:
        streamPos0 = infos.find(aToken)
        if streamPos0 >= 0:
            break
    if streamPos0 < 0:
        print(Con.ErrorPrompt + ' Failed to find Stream #0.0 in video file')
        exit(1)

    for aToken in ['Stream #0.1', 'Stream #0:1']:
        streamPos1 = infos.find(aToken)
        if streamPos1 >= 0:
            break
    if streamPos1 < 0:
        print(Con.ErrorPrompt + ' Failed to find Stream #0.1 in video file')
        exit(1)
    info0 = infos[streamPos0:streamPos1]
    info0 = info0[:info0.find('\n')]
    info1 = infos[streamPos1:]
    info1 = info1[:info1.find('\n')]
    if info0.find('Video:') >= 0: #video info
        videoInfo = info0
    elif info1.find('Video:') >= 0: #video info
        videoInfo = info1
    else:
        return None

    #get frame size:
    VEncoding = None
    FrameSize = None
    FrameRate = None
    PixelFormat = None
    tbr = None
    tbn = None
    tbc = None
    tem = videoInfo[videoInfo.find('Video:') + 7:]
    segs = tem.split(',')
    for aSeg in segs:
        aSeg = aSeg.lstrip()

        if VEncoding == None:
            idx = aSeg.lower().find('mjp')
            if idx >= 0:
                VEncoding = aSeg
                continue

        if FrameSize == None:
            idx = aSeg.find('x')
            if idx > 0: #found the frame size part
                num1 = aSeg[:idx]
                num2 = aSeg[idx + 1:]
                try:
                    w = int(num1)
                    h = int(num2)
                    if (w < 100) or (h < 50):
                        pass #invalid frame size
                    else:
                        FrameSize = (w, h)
                        continue
                except:
                    pass

        if PixelFormat == None:
            if aSeg.find('yuv') >= 0:
                PixelFormat = aSeg
                continue

        if tbr == None:
            idx = aSeg.find(' tbr')
            if idx >= 0:
                tbr = aSeg[:idx]
                continue

        if tbn == None:
            idx = aSeg.find(' tbn')
            if idx >= 0:
                tbn = aSeg[:idx]
                continue

        if tbc == None:
            idx = aSeg.find(' tbc')
            if idx >= 0:
                tbc = aSeg[:idx]
                continue

    #get frame rate:
    if (tbr == tbn) and (tbr == tbc):
        FrameRate = tbr
    else:
        FrameRate = None

    return FrameRate, FrameSize, PixelFormat

#============================================================================
def FnEncodeVideo(ARoot, AFname, AOutputDir, AVideoBinDir, AFileAccessTime=None, AFileModTime=None):
    """=========================================================================
    Re-encode video file into mkv using ffmpeg encoder.
    Note: 
    Arguments:
      AFname: filename without root path.
      AFileAccessTime, AFileModTime: used to set the encoded file the same as the original.
    Return: 
      RFname, RProcessedCnt
      RFname: includes 2 filenames: original and re-encoded, if the file is re-encodable.
             The original filename is empty if the re-encoded file exists in the target location.
    Example:
      name, processed = FnEncodeVideo(root, name, processed, fileAccessTime=0, fileModTime=0)
    ========================================================================="""
    RProcessedCnt = 0
    RExistingTgtCnt = 0

    fullname = join(ARoot, AFname)
    path, datePrefix, base, ext, base2, ext2, stem = GetFnameComponents(AFname)
    if not datePrefix:
        if AFileModTime > 0:
            mt = time.gmtime(AFileModTime) #time.localtime() will give wrong time
            datePrefix = ('%04u%02u%02u' % (mt[0], mt[1], mt[2]))
        else:
            datePrefix = GenerateDatePrefix(fullname)

    extLo = ext.lower()
    ext2Lo = ext2.lower()
    transcodeOn = False
    if (extLo in ['.avi', '.mov']) and not (ext2Lo in ['.dvx', '.xvd', '.mp4', '.h24']): #can transcode
        frameRate, frameSize, pixelFormat = GetVideoFileInfo(fullname) #returns None if the info is wrong

        if frameRate == None:
            PrintFileInfo()
            print(Con.ErrorPrompt + ' Error: Failed to get the video frame rate')
            exit(1)
        if frameSize == None:
            PrintFileInfo()
            print(Con.ErrorPrompt + ' Error: Failed to get the video frame size')
            exit(1)
        if pixelFormat == None:
            PrintFileInfo()
            print(Con.ErrorPrompt + ' Error: Failed to get the pixel format')
            exit(1)
        transcodeOn = True

    if transcodeOn: #Note: encoded file must return two filenames
        aCodec = ['-acodec', 'copy']
        vFrameRate = ['-r', frameRate]
        if Cfg.VCodec == 'mpeg4':
            vCodec = ['-vcodec', 'mpeg4']
            #Cfg.VEncExt2 = '.MP4' #set in the Cfg
            #Cfg.VEncExt = '.MKV'           
            vQuality = ['-sameq']
            pixFmt = ''
        elif Cfg.VCodec == 'libx264':
            vCodec = ['-vcodec', 'libx264']
            #Cfg.VEncExt2 = '.H24' #set in the Cfg
            #Cfg.VEncExt = '.MKV'
            frameH = frameSize[0]
            frameW = frameSize[1]
            if (frameH <= 320) and (frameW <= 240):
                vQuality = ['-crf', '23'] #22, 23
            elif (frameH <= 640) and (frameW <= 480):
                vQuality = ['-crf', '25'] #23, 24, 25
            elif (frameH <= 848) and (frameW <= 480):
                vQuality = ['-crf', '26'] #25,26
            elif (frameH <= 1280) and (frameW <= 720):
                vQuality = ['-crf', '28'] #27, 28

            if (pixelFormat == 'yuvj422p') or (pixelFormat == 'yuvj420p'):
                pixFmt = ['-pix_fmt', 'yuvj420p']
            else:
                pixFmt = ''
                PrintFileInfo()
                print(Con.ErrorPrompt + 'Error: Unknown pixel format')
                exit(0)
        else: #unrecognized
            PrintFileInfo()
            print(Con.ErrorPrompt + " Unrecognized vcodec: " + Cfg.VCodec)
            exit(1)

        #convert mov to mkv using ffMpeg:
        newFname = path + base + Cfg.VEncExt2 + Cfg.VEncExt
        outputFname = join(ARoot, newFname)
        #print outputFname
        if os.path.exists(outputFname):
            PrintFileInfo()
            print Con.Prompt3, 'Output file \"' + outputFname + '\" already exists. Skip.'
            SetFileAccModTime(outputFname, Con.Prompt3 + ' Sync the acc/mod time to the original', AFileAccessTime, AFileModTime)
            ##SyncFileModTime(outputFname, Con.Prompt3 + ' Sync the mod time to the original', AFileModTime)
            RExistingTgtCnt += 1
            return (AFname, newFname), RProcessedCnt, RExistingTgtCnt

        #Check if encoded file exists in special dir without comment:
        subDir = ARoot[ARoot.find(Cfg.InputDir) + len(Cfg.InputDir):]
        newTargetDir, isDifferent = GetTargetDir(subDir, datePrefix, AIsVideo=True)
        newTargetDir, newFname = GetRealVideoDirFname(join(AOutputDir, newTargetDir), newFname, stem, datePrefix, Cfg.VEncCExt)
        targetFile = join(newTargetDir, newFname)
        ##targetFile = GetTargetVidFname(newTargetDir, newFname, stem, Cfg.VEncExt2, Cfg.VEncExt)
        if exists(targetFile):
            if not Cfg.VidOverwriteOn:
                PrintFileInfo()
                print(Con.Prompt3 + ' Destination file \"' + targetFile + '\" already exists. Skip.')
                RExistingTgtCnt += 1
                return (AFname, ''), RProcessedCnt, RExistingTgtCnt
            else:
                PrintFileInfo()
                print(Con.Prompt3 + ' Destination file \"' + targetFile + '\" already exists. To be overwritten.')
                RExistingTgtCnt += 1

        tmpFile = join(ARoot, path + base + '.tmp' + Cfg.VEncExt) #join(ARoot, path + base + '.tmp' + Cfg.VEncExt)
        if exists(tmpFile):
            os.remove(tmpFile)

        ##cmd = join(Con.ExePath, Con.LibDir, Cfg.FFMpegDir, Cfg.VProcCmd)
        cmd = Cfg.VProcCmd
        #like: ffmpeg -i infile.mov -vcodec mpeg4 -sameq -acodec copy outfile.mkv
        ##cmdlnOpt = vCodec + vQuality + vFrameRate + pixFmt + aCodec ##-vtag XVID
        cmdlnOpt = vCodec + vQuality + vFrameRate + pixFmt + aCodec
        ##cmdln = cmd + ' -i \"' + fullname + '\" ' + cmdlnOpt + ' \"' + tmpFile +'\"'
        ##cmdln = cmd + ' -i ' + fullname + ' ' + cmdlnOpt + ' ' + tmpFile
        cmdln = [cmd, '-i', fullname] + cmdlnOpt + [tmpFile]
        PrintFileInfo()
        print(Con.Prompt3 + ' Converting ' + ext + ' to ' + Cfg.VEncExt + ' ...')

        #retStr = subprocess.check_call(cmdln, shell=True) #check_output is new in v2.7. checi_call is new in v2.5
        #if Cfg.Verbosity >= 3:
            #print(retStr)
        #extProc = subprocess.Popen(cmdln.split(), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        extProc = subprocess.Popen(cmdln, stdout=subprocess.PIPE)
        infos = extProc.communicate() #[0]: stdout, [1]: stderr. The stderr has the info
        if Cfg.Verbosity >= 3:
            print(infos[1])

        if not exists(tmpFile):
            print(Con.ErrorPrompt + ' Error: Video tmp file \"' + tmpFile + '\" does not exist.')
            exit(1)
        outputFname = join(ARoot, newFname)
        os.rename(tmpFile, outputFname)

        #Set file access, modification time to their original:
        SetFileAccModTime(outputFname, Con.Prompt3 + ' Sync the acc/mod time to the original', AFileAccessTime, AFileModTime)
        ##SyncFileModTime(outputFname, Con.Prompt3 + ' Sync the mod time to the original', AFileModTime)
        print(Con.Prompt3 + ' Converted to \"' + newFname + '\".')

        AFname = (AFname, newFname) #Update filename to new name to be used by later functions
        RProcessedCnt += 1

        #not working for ffmpeg encoding:
        #if PollInputFor('x'): #user quit
            #print(Con.AttnPrompt + ' User quited')
            #PrintAppFooter(Con.AppName, Con.AppVer, Con.AppCopyright, Con.AppYear)
            #exit(1)

    return AFname, RProcessedCnt, RExistingTgtCnt

def GetTargetVidFname(ATgtDir, AFname, AStem, AExt2, AExt):
    """=========================================================================
    Note: finished but not used.
    Find out the correct filenmae for the new transcoded video file.
    ========================================================================="""
    RFname = AFname
    if exists(ATgtDir):
        dirs, fnames = ListFiles(Root=ATgtDir)
        if fnames:
            ##tgtFnames = []
            sameExtTgts = []
            for aFname in fnames:
                path, datePrefix, base, ext, base2, ext2, stem = GetFnameComponents(AFname)
                if (stem == AStem) and (ext2 == AExt2) and (ext == AExt):
                    ##tgtFnames.append([base2, ext2, ext])
                    sameExtTgts.append([base2, ext2, ext])

            #sameExtTgts = []
            #otherExtTgts = []
            #if tgtFnames:
                #for aFname in sameExtTgts:
                    #if aFname[2] == AExt:
                        #sameExtFnames.append(aFname)
                    #else:
                        #otherExtTgts.append(aFname)

                if sameExtTgts:
                    tgtsCnt = len(sameExtTgts)
                    if tgtsCnt == 1:
                        tgt = sameExtTgts[0]
                    else: #more than 1 same-type-fname found
                        tgt = sameExtTgts[0]
                        for index in range(1, tgtsCnt):
                            if len(sameExtTgts[index][0]) > len(tgt[0]): #choose the longer base2 name
                                tgt = sameExtTgts[index]
                    RFname = path + datePrefix + tgt[0] + tgt[1] + tgt[2]

    return join(ATgtDir, RFname)

def ProcBinRedundantVideoFiles(AInputDir=None, AEncodedVidCExts=[], AOrigVidCExts=[]):
    """=========================================================================
    :: Keep the latest encoded video file and move the old encoded and original video files into the video bin dir.
    Note: 
    Arguments:
        AEncodedVidCExts: list of cext. Must in lowercase.
        AOrigVidCExts: Must in lowercase.
    Return: 

    Example:

    ========================================================================="""
    global Con, GDirInfo, GFileInfo, GVideoBinDir

    videoBinDirFull = GVideoBinDir

    RProcessedCnt = 0
    RExistTargetsCnt = 0 #existing target fname count
    RConflictsCnt = 0
    RNewCommentCnt = 0
    RErrCnt = 0

    if AInputDir == None:
        return RProcessedCnt, RExistTargetsCnt, RConflictsCnt, RNewCommentCnt, RErrCnt

    for root, dirs, files in os.walk(AInputDir):
        if Cfg.Verbosity >= 1:
            print(Con.Prompt1 + ' Directory \"' + root + os.sep + '\".')
            print('contains %u non-directory files.' % (len(files)))
            print(' ')

        if root[-1] == os.sep:
            root = root[:-1]
        rootDir, curDir = split(root)
        if curDir == Cfg.VideoDir:
            rootDir2, parentDir = split(rootDir)
            if (len(parentDir) >= 8) and IsDateDir(parentDir[:8]): #in video dir like /20110405-party/video/
                GDirInfo = Con.Prompt1 + ' Dir: \"' + root +'\"'
                vidDict = {}
                for fname in files:
                    keyNameEnc = ''
                    keyNameOrig = ''
                    FullFname = join(root, fname)
                    if not exists(FullFname):
                        continue
                    path, datePrefix, base, ext, base2, ext2, stem = GetFnameComponents(fname)
                    if (len(datePrefix) < 8): #non-std fname
                        continue
                    #extLo = ext.lower()
                    #ext2Lo = ext2.lower()
                    cext = ext2 + ext
                    cextLo = cext.lower()

                    #Step 1: collect video file info
                    if (cextLo in AEncodedVidCExts): #like: 20110823-P1003456.THM.JPG
                        keyNameEnc = stem
                    elif (cextLo) in AOrigVidCExts:
                        keyNameOrig = stem
                    else: #non-video files
                        pass

                    if keyNameEnc != '':
                        if not vidDict.has_key(keyNameEnc): #create a key
                            vidDict[keyNameEnc] = [[], []] #[EncVidFile, OrigVidFiles], where each file is [base2, cext]
                        vidDict[keyNameEnc][0].append([base2, cext])
                    if keyNameOrig != '':
                        if not vidDict.has_key(keyNameOrig): #create a key
                            vidDict[keyNameOrig] = [[], []] #[EncVidFile, OrigVidFiles], where each file is [base2, cext]
                        vidDict[keyNameOrig][1].append([base2, cext]) 
                #end of for

                #step 2:
                if vidDict: #if it's not empty
                    for vStem, values in vidDict.items():
                        encVNames = values[0]
                        origVNames = values[1]

                        if encVNames: #if not empty, search for src starting from the highes priority ext
                            srcFname = None
                            for aCExt in AEncodedVidCExts:
                                for aEncVName in encVNames:
                                    if aCExt == aEncVName[1].lower(): #found the fname with the right ext
                                        srcFname = aEncVName
                                        encVNames.remove(srcFname)
                                        break
                                if srcFname: #src found
                                    break

                            if srcFname: #if there is src file, search for redundant files
                                tgtFNames = encVNames + origVNames
                                if tgtFNames: #if not empty, check if targets are redundant or conflicting
                                    redunFnames = []
                                    conflFnames = []
                                    newerFnames = [] #fnames with newer comments
                                    if len(srcFname[0]) == len(vStem): #src has no comment
                                        srcHasComment = False
                                    else:
                                        srcHasComment = True

                                    for aTgtFName in tgtFNames:
                                        if srcHasComment:
                                            if len(aTgtFName[0]) > len(vStem): #target has comment
                                                if aTgtFName[0] != srcFname[0]: #target has different comment
                                                    conflFnames.append(aTgtFName)
                                                else: #src and target have the same comment
                                                    redunFnames.append(aTgtFName)
                                            else: #target has no comment
                                                redunFnames.append(aTgtFName)
                                        else: #src has no comment
                                            if len(aTgtFName[0]) > len(vStem): #target has comment
                                                newerFnames.append(aTgtFName)
                                            else: #target has no comment
                                                redunFnames.append(aTgtFName)
                                    #end for aTgtFName

                                    #print info if redundant etc files are found:
                                    if redunFnames or conflFnames or newerFnames:
                                        srcFileFull = join(root, srcFname[0] + srcFname[1])
                                        if exists(srcFileFull):
                                            GFileInfo = GetFileInfoStr(srcFileFull) #Get file info
                                            PrintFileInfo()
                                        else:
                                            print(Con.ErrorPrompt + ' Error: File \"' + srcFileFull +'\" does not exist.')
                                            RErrCnt += 1
                                            continue

                                        if redunFnames:
                                            for aFname in redunFnames:
                                                origFile = aFname[0] + aFname[1]
                                                origFileFull = join(root, origFile)
                                                if not exists(videoBinDirFull): #Create dir if not exists
                                                    print Con.Prompt3, 'Create new dir \"' + videoBinDirFull + '\"'
                                                    os.makedirs(videoBinDirFull)

                                                targetFile = join(videoBinDirFull, aFname[0] + aFname[1])
                                                if exists(targetFile):
                                                    #ans = raw_input('Target file already exists, overwrite' + Con.InputPrompt)
                                                    print(Con.Prompt3 + ' Target file \"' + targetFile + '\" already exists. Skip.')
                                                    RExistTargetsCnt += 1
                                                else: #Target file not exists, move file
                                                    fileAccessTime = getatime(origFileFull)
                                                    fileModTime = getmtime(origFileFull) 
                                                    print(Con.Prompt3 + ' Redundant file \"' + origFile + '\". Move to \"' + videoBinDirFull + os.sep + '\"')
                                                    os.rename(origFileFull, targetFile)
                                                    SetFileAccModTime(targetFile, Con.Prompt3 + ' Sync the acc/mod time to the original', fileAccessTime, fileModTime)
                                                    ##SyncFileModTime(targetFile, ' Sync the acc/mod time to the original', fileModTime)
                                                    RProcessedCnt += 1

                                        if conflFnames:
                                            for aFname in conflFnames:
                                                print(Con.AttnPrompt + ' Conflicting comments: ' + aFname[0] + aFname[1])
                                                RConflictsCnt += 1

                                        if newerFnames:
                                            for aFname in newerFnames:
                                                print(Con.AttnPrompt + ' New comment found: ' + aFname[0] + aFname[1])
                                                RNewCommentCnt += 1

    return RProcessedCnt, RExistTargetsCnt, RConflictsCnt, RNewCommentCnt, RErrCnt


def ProcSyncVideoFnames(AInputDir=None, ASyncFromCExt=None, ASyncToCExtList=[], AStrategy=ssSyncToLatestComment):
    """=========================================================================
    Sync the comment of SyncFrom file to the SyncTo files.
    Note: 
    Arguments:
          ASyncFromCExt: the compound (ext2+ext) ext of a file type. Can be of upper or lower case.
          ssSyncToLatestCommentt: list of compond ext in the order of priority. MUST be in lower cases.
          AStrategy: sync strategy.
              ssSyncToLatestComment: sync to the comment of the first matched target file.
              ssAddNewCommentOnly: sync to the comment of the matched target file only when the source has no comment.
    Return: 

    Example:

    ========================================================================="""
    global Con, GDirInfo, GFileInfo ##, GVideoBinDir
    RProcessedCnt = 0
    RRedundantCnt = 0
    RMultiTargets = 0
    RErrCnt = 0

    if AInputDir == None:
        return 0, 0

    for root, dirs, files in os.walk(AInputDir):
        if Cfg.Verbosity >= 1:
            print(Con.Prompt1 + ' Directory \"' + root + os.sep + '\".')
            print('contains %u non-directory files.' % (len(files)))
            print(' ')

        if root[-1] == os.sep:
            root = root[:-1]
        rootDir, curDir = split(root)
        if curDir == Cfg.VideoDir:
            rootDir2, parentDir = split(rootDir)
            if (len(parentDir) >= 8) and IsDateDir(parentDir[:8]): #in video dir like /20110405-party/video/
                GDirInfo = Con.Prompt1 + ' Dir: \"' + root +'\"'
                ThmFiles = []
                VidFiles = []

                for fname in files:
                    FullFname = join(root, fname)
                    if not exists(FullFname):
                        continue
                    path, datePrefix, base, ext, base2, ext2, stem = GetFnameComponents(fname)
                    if (len(datePrefix) < 8):
                        continue
                    extLo = ext.lower()
                    ext2Lo = ext2.lower()

                    #Step 1: collect THM and video file info
                    cextLo = ext2Lo + extLo
                    if (cextLo == ASyncFromCExt.lower()): #like: 20110823-P1003456.THM.JPG
                        ThmFiles.append([stem, base2])
                    elif (cextLo) in ASyncToCExtList:
                        VidFiles.append([stem, base2, ext2 + ext])
                #end of for

                #Step 2: find out if a THM file has a video finame to sync to
                for aThmFile in ThmFiles:
                    if len(VidFiles) == 0:
                        break
                    targetFiles = []
                    newVidFiles = []
                    for aVidFile in VidFiles: #seperate video files into two groups
                        if aThmFile[0] == aVidFile[0]:
                            targetFiles.append(aVidFile)
                        else:
                            newVidFiles.append(aVidFile)
                    VidFiles = newVidFiles

                    #Search for the best match according to a preference list:
                    bestTarget = []
                    errMsg = ''
                    targetFound = False
                    multiTargets = []
                    for aCExt in ASyncToCExtList:
                        for aTarget in targetFiles:
                            if aTarget[2].lower() == aCExt:
                                if AStrategy == ssSyncToLatestComment: #sync to the latest fname
                                    if not targetFound:
                                        targetFound = True
                                        if (aTarget[1] <> aThmFile[1]): #only change when the resulting name is different
                                            if len(aTarget[1]) > len(aTarget[0]): #if dest file has comment
                                                bestTarget = aTarget
                                            else: #disappearing comments
                                                errMsg = ' Target comment dissappeared: ' + aTarget[1] + aTarget[2]
                                        else: #src = targt 
                                            pass 
                                    else: #redundant target filenames
                                        if (aTarget[1] != aThmFile[1]): #conflict of fnames
                                            if len(aTarget[1]) > len(aTarget[0]): #if dest file has comment
                                                if len(bestTarget) > 0: #src comment will change
                                                    if aTarget[1] != bestTarget[1]: #dest's comment is different than the changed comment
                                                        multiTargets.append(aTarget)
                                                    else:
                                                        pass
                                                else: #src and dest have different comments
                                                    multiTargets.append(aTarget)
                                            else: #dest file has no comment
                                                pass
                                        else: #src and dest have the same comment
                                            pass
                                #copy comment from any old file if src has no comment. Report conflict if src's comment != target 
                                elif AStrategy == ssAddNewCommentOnly: 
                                    if not targetFound:
                                        if len(aTarget[1]) > len(aTarget[0]): #if dest file has comment
                                            targetFound = True
                                            if len(aThmFile[0]) == len(aThmFile[1]): #if src file has no comment, copy 
                                                bestTarget = aTarget
                                            elif aThmFile[1] != aTarget[1]: #src and target have different comments
                                                #bestTarget = aTarget
                                                errMsg = ' Conflict of comments: ' + aTarget[1] + aTarget[2]
                                            else: #aThmFile[1] == aTarget[1] and len(aThmFile[0]) != len(aThmFile[1])
                                                pass
                                    else: #redundant target filenames
                                        if len(aTarget[1]) > len(aTarget[0]): #if dest file has comment
                                            if len(aThmFile[0]) == len(aThmFile[1]): #if src file has no comment
                                                if len(bestTarget) > 0: #src comment will change
                                                    if aTarget[1] != bestTarget[1]: #dest's comment is different than the changed comment
                                                        multiTargets.append(aTarget)
                                                    else:
                                                        pass
                                                else:
                                                    multiTargets.append(aTarget)
                                            else: #src has comment
                                                if aTarget[1] != aThmFile[1]: #src and target have different comments
                                                    errMsg = ' Conflict of comments: ' + aTarget[1] + aTarget[2]
                                                else: #src and target comments are the same
                                                    pass

                                else:
                                    print(Con.ErrorPrompt + ' Unkown AStrategy value.')
                                    exit(0)
                                targetFiles.remove(aTarget) #remove the processed
                                break
                            else: #not the right CExt, next
                                pass
                        #end for aTarget
                    #for aCExt

                    #print:
                    if (len(bestTarget) > 0) or (len(multiTargets) > 0) or (len(errMsg) > 0):
                        thmFile = aThmFile[1] + ASyncFromCExt #Cfg.ThmCExt
                        thmFileFull = join(root, thmFile)
                        if exists(thmFileFull):
                            GFileInfo = GetFileInfoStr(thmFileFull) #Get file info
                            PrintFileInfo()

                            #if target found, then:
                            if (len(bestTarget) > 0):
                                vFullFname = join(root, bestTarget[1] + bestTarget[2])
                                if exists(vFullFname): #sync thm file name:
                                    newThmFname = bestTarget[1] + ASyncFromCExt #Cfg.ThmCExt #commented fname
                                    newThmFnameFull = join(root, newThmFname)
                                    if exists(newThmFnameFull):
                                        print(Con.AttnPrompt + ' Synced THM file exists:  \"' + newThmFname + '\"')
                                        print(Con.AttnPrompt + ' Possible redundant file: \"' + thmFile + '\"')
                                        RRedundantCnt += 1
                                    else:
                                        print(Con.Prompt3 + ' Rename ' + thmFile + ' to ' + newThmFname)
                                        fileAccessTime = getatime(thmFileFull)
                                        fileModTime = getmtime(thmFileFull)
                                        os.rename(thmFileFull, newThmFnameFull)
                                        SetFileAccModTime(newThmFnameFull, Con.Prompt3 + ' Sync the acc/mod time to the original', fileAccessTime, fileModTime)
                                        ##SyncFileModTime(newThmFnameFull, ' Sync the mod time to the original', fileModTime)
                                        RProcessedCnt += 1
                                else:
                                    print(Con.ErrorPrompt + ' Target file not found: ' + bestTarget[1] + bestTarget[2])

                            if len(multiTargets) > 0:
                                print(Con.AttnPrompt + ' Multiple target names found: ' + ', '.join([item[1]+item[2] for item in multiTargets]))
                                RMultiTargets += 1
                            if len(errMsg) > 0:
                                print(Con.ErrorPrompt + errMsg)
                                RErrCnt += 1


    return RProcessedCnt, RRedundantCnt, RMultiTargets, RErrCnt


def ProcessFiles(progFunc, AInputDir, AOutputDir, FileType=None, ASkipDatedDir=True):
    """
    Parameter:
      FileType: a string such as '.jpg'. Only file with this ext will be processed.
        If None, then all types are processed.
      ASkipDatedDir: whether to skip dated dirs.
    """
    global Con, GDirInfo, GFileInfo

    RTotalProcessedCnt = 0

    Result = { \
        'FnAddDatePrefix': [0], \
        'FnAddJpgSuffix': [0], \
        'FnEncodeVideo': [0, 0], \
        'FnMoveToDatedDir': [0, 0, 0, 0] \
    }

    skipThisRoot = False
    videoBinDirFull = GVideoBinDir #join(Cfg.InputDir, Cfg.VideoBinDir)

    for root, dirs, files in os.walk(AInputDir):
        #print 'root:', root
        #print 'dirs: ', dirs
        #print 'files: ', files
        #if Cfg.Verbosity >= 1:
        GDirInfo = Con.Prompt1 + ' Dir \"' + root + '\"' #dir info
        #print 'contains', len(files), "non-directory files."
        #print(' ')

        #Don't dig into the dated dir:
        if skipThisRoot:
            if root.find(rootToSkip) == 0:
                #print(Con.Prompt3 + ' In dated dir. Skip')
                continue
            else:
                skipThisRoot = False
        if (ASkipDatedDir) and IsDateDir(split(root)[1]):
            #print(Con.Prompt3 + ' Dated dir. Skip')
            #print(' ')
            rootToSkip = root
            skipThisRoot = True
            continue

        #do not dig into special dirs:
        if root.find(videoBinDirFull) == 0:
            #print(Con.Prompt3 + ' Special dir. Skip')
            continue


        for name in files:
            #Init:
            path, datePrefix, base, ext, base2, ext2, stem = GetFnameComponents(name)
            if (FileType is not None) and (ext.lower() != FileType): #Only process allowed file types
                continue

            #<Get file info>
            fullname = join(root, name)
            if not exists(fullname):
                continue
            #Save file time stamps to be resumed later:
            #NU#fileCreationTime = getctime(fullname) #Creation time under Win; Last change time for Unix
            fileModTime = getmtime(fullname) #The time of last modification
            fileAccessTime = getatime(fullname) #Time of last access
            GFileInfo = GetFileInfoStr(fullname)
            #</Get file info>

            processed = 0 #reset the flag
            processedCnt = 0
            #datePrefix = None

            #-------------------------------------------------------------------
            #Function 2: Add date to file names as prefix:
            if (progFunc == FuncNo.Auto) or (progFunc == FuncNo.AddDatePrefix): 
                #Add date Prefix to certain file types:
                name, processedCnt = FnAddDatePrefix(root, name)
                Result['FnAddDatePrefix'][0] += processedCnt
                processed = processed or processedCnt

            #-------------------------------------------------------------------
            #Function 3: Add .JPG after .THM
            if (progFunc == FuncNo.Auto) or (progFunc == FuncNo.AddJpgAfterThmExt):
                name, processedCnt = FnAddJpgSuffix(root, name)
                Result['FnAddJpgSuffix'][0] += processedCnt
                processed = processed or processedCnt

            #-------------------------------------------------------------------
            #Function 4: Transcode video files but skip dated dirs
            #Function 5: Transcode video files in all dirs
            if Cfg.VTranscodOn and \
               ((progFunc == FuncNo.Auto) or (progFunc == FuncNo.EncodeVid) or (progFunc == FuncNo.EncodeVidAllDirs)):
                name, processedCnt, existingTgtCnt = FnEncodeVideo(root, name, AOutputDir, videoBinDirFull, fileAccessTime, fileModTime)
                Result['FnEncodeVideo'][0] += processedCnt
                Result['FnEncodeVideo'][1] += existingTgtCnt
                processed = processed or processedCnt

            #-------------------------------------------------------------------
            #Function 100: move photo or certain type of video file to its dated dir:
            if (progFunc == FuncNo.Auto) or (progFunc == FuncNo.MoveToDatedDir):
                name, processedCnt, existingTgtCnt, binnedCnt, errCnt = FnMoveToDatedDir(root, name, AOutputDir, videoBinDirFull, fileAccessTime, fileModTime)
                Result['FnMoveToDatedDir'][0] += processedCnt
                Result['FnMoveToDatedDir'][1] += existingTgtCnt
                Result['FnMoveToDatedDir'][2] += binnedCnt
                Result['FnMoveToDatedDir'][3] += errCnt
                processed = processed or processedCnt

            #-------------------------------------------------------------------
            if processed:
                RTotalProcessedCnt = RTotalProcessedCnt + 1
                #print ' '

    return RTotalProcessedCnt, Result


#===============================================================================
#:: Body
#===============================================================================
if __name__ == "__main__":
    ec = main()
    if ec == 1:
        print(Con.Prompt1 + " User aborted.")  



