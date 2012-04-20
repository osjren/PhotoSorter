# -*- coding: utf-8 -*-
"""
Copyright (C) 2005-2012 Jinsong Ren

For documentation of the project, please go to:
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
# RenLib.py: collection of generic functions
# Note:
#   Requires Python 2.2 or above.
# History:
#   2005.07.03 - Created by Jinsong Ren.
#   2007.02.05 - last update.
#===============================================================================
from __future__ import nested_scopes
import os, sys, time, commands, re, fnmatch, subprocess, shutil, select, termios
from os.path import splitext
#join, isdir, islink

#RENLIBPATH = os.path.abspath('')
#RENLIBEXTRAPATH = os.path.join(RENLIBPATH, 'extra')
#sys.path.append(RENLIBEXTRAPATH)
from standout import *
#from daemonize import *

#__all__ = ['ListFiles', 'PrintHeader', 'PrintEnder']


GPrompts = { \
    'Warning' : '!!!Warning:', \
    'Error'   : '???Error:', \
    'Info1'   : '===', \
    'Info2'   : '---', \
    'Info3'   : '...' \
}

#


def Print(Message='', Tag=None, Prompt=None):
    #Extract the &priority tag:
    idx = Message.find('&priority-')
    if idx >= 0: #Idx is -1 if not found
        pTag = Message[idx:(idx+12)] #Print priority tag
        Message = Message.replace(pTag, '') #Remove the tag from the string body
    else:
        pTag = ''
        
    if Prompt is not None:
        myPrompt = Prompt + ' '
    else:
        myPrompt = ''
        
    if Tag is not None:
        myTag = '<' + Tag + '> '
    else:
        myTag = ''
        
    print pTag + myPrompt + myTag + Message

def Warning(Message='', Tag=None):
    Print(Message, Tag, GPrompts['Warning'])
    
def Error(Message='', Tag=None):
    Print(Message, Tag, GPrompts['Error'])
    #sys.exit(1)
    
def Info1(Message='', Tag=None):
    Print(Message, Tag, GPrompts['Info1'])

def Info2(Message='', Tag=None):
    Print(Message, Tag, GPrompts['Info2'])

def Info3(Message='', Tag=None):
    Print(Message, Tag, GPrompts['Info3'])

def StripNulls(AString):
    "Strip whitespace and nulls"
    return AString.replace("\00", "").strip()

def CopyDict(ToDict, FromDict):
    """
    Copy keys and non-empty values from a dict to another, overwriting only the 
    same keys
    """
    for aKey in FromDict:
        if FromDict[aKey] is not None:
            ToDict[aKey] = FromDict[aKey]
    return ToDict

def FilesExist(FileList=None):
    """Check if a file or a list of files exist
    Return:
        1 or 0: if input is a single file name string.
        a list of 1 or 0: if input is a list of file names.
    """
    result = []
    if FileList is None:
        return 0
    if type(FileList) is str:
        return os.path.exists(FileList)
    elif type(FileList) is list:
        if len(FileList) == 0:
            return [0]
        for aFile in FileList:
            if os.path.exists(aFile):
                result.append(1)
            else:
                result.append(0)
        return result
                
    
#===============================================================================
# Print Application header
# History:
#   2005.07.16 - Created by Jinsong Ren.
#===============================================================================
def PrintAppHeader(AppName='', AppVer='', Copyright='', Year=''):
    global GAppStartTime, GAppStopTime
    
    Print(' ')
    Info1(' '.join([AppName, "v" + AppVer, Copyright, Year]))
    
    GAppStartTime = time.time() #Sec since epoch
    curTime = time.strftime('%Y-%m-%d %I:%M:%S %p', time.localtime(GAppStartTime))
    Info1("[" + GetTimeInterval(GAppStartTime) +  '] ' + curTime)
    
    Info1("Starts...")
    #Print(' ')

#===============================================================================
# Print application footer
# History:
#   2005.01.25 - Created by Jinsong Ren.
#===============================================================================
def PrintAppFooter(AppName='', AppVer='', Copyright='', Year=''):
    global GAppStartTime, GAppStopTime
    
    Print(' ')
    Info1(' '.join([AppName, "v" + AppVer, Copyright, Year]))
    
    #Info1("Total time lapse: [" + GetTimeLapse(GTimerStopTime) + ']')
    GAppStopTime = time.time()
    curTime = time.strftime('%Y-%m-%d %I:%M:%S %p', time.localtime(GAppStopTime))
    Info1("[" + GetTimeInterval(GAppStopTime) +  '] ' + curTime)
    Info1("End.")
    Print(' ')

#===============================================================================
# Get time interval
# Input:
#   StopTime: the stop time in seconds.
#     None: default, use current time.
#   StartTime: the start time in seconds.
#     None: default, use the global GTimerStartTime as start time.
# Return:
#   A string like: '09-23:32:10'  (days-hours:minutes:seconds)
# History:
#   2005.07.16 - Created by Jinsong Ren.
#===============================================================================
def GetTimeInterval(StopTime=None, StartTime=None):
    global GAppStartTime, GAppStopTime
    
    if StopTime is None:
        StopTime = time.time()
    if StartTime is None:
        StartTime = GAppStartTime
    
    intervalSec = StopTime - StartTime
    lapsedDay = int(intervalSec/3600.0/24.0)
    lapsedHour = int(intervalSec/3600.0 - lapsedDay*24.0)
    lapsedMin = int(intervalSec/60.0 - lapsedDay*24.0*60.0 - lapsedHour*60.0)
    lapsedSec = int(intervalSec - lapsedDay*24.0*3600.0 - lapsedHour*3600.0 - lapsedMin*60.0)
    return "%03d-%02d:%02d:%02d" % (lapsedDay, lapsedHour, lapsedMin, lapsedSec)

#===============================================================================
# Get the time stamp that will be used to form a log file name
# Input:
#   Time: the time that the stamp is based on, the seconds from the epoch.
#     None: default, use current time.
# Output:
#   A string in such form: YYMMDD-HHMMSS, such as '20050721_003357'
# Example:
#   
# History:
#   2005.07.20 - Created by Jinsong Ren.
#   2011.06.26 - replaced gmtime with localtime
#===============================================================================
def GetTimeStamp(Time=None):
    if Time is None:
        Time = time.time()
    gmTime = time.localtime(Time) #%time.gmtime(Time)
    timeLabel = ('%04u%02u%02u_%02u%02u%02u' % \
                (gmTime[0], gmTime[1], gmTime[2], gmTime[3], gmTime[4], \
                    gmTime[5])) #[2:]
    return timeLabel

def Lowercase(StringList=None):
    """
    Convert a string or a list of strings to lowercase.
    Example:
        c=Lowercase(['A', 'B', 'c', '1'])
        c=Lowercase('A')
    History:
        2005.08.20 - Created by Jinsong Ren.
    """
    if StringList is None:
        return None
    if len(StringList) == 0:
        return ''
    if type(StringList) is str:
        return StringList.lower()
    elif type(StringList) is list:
        result = []
        for aStr in StringList:
            result.append(aStr.lower())
        return result
    return None

def ListFiles(DictArgs={}, **KeywArgs):
    """=========================================================================
    List the files and dirs in Root
    Input:
        Root : the root path of the directory to be listed.
        WithPath: 
            0: Only filenames are included in the returned values. Default.
            1: The returned filenames have full path.
        WithFileExt: valid only when WithPath=0.
            0: Return file basenames only, without ext.
            1: Returned filenames have file ext. Default.
        FileExt: 
            None: any file is allowed. Default.
            'xxx': a string.
            ['xxx', 'yyy']: a list of strings. only files with such ext are returned.
        Recurse:
            0: do not recurse. Default.
            1: recurse into sub-directories.
    Return: RDirs, RFiles
    Note: Must call with keywords
    Example:
        (myDirs, myFiles) = ListFiles(Root=inputDir, WithPath=1)
        (myDirs, myFiles) = ListFiles(Root='c:', WithPath=0, WithFileExt=1, FileExt='.hdr')
    History:
        2005.08.20 - Added recurse argument
        2005.07.17 - Changed the calling conventions of arguments.
        2005.07.03 - Created by Jinsong Ren.
    ========================================================================="""
    defaults = { 'Root': None, 'WithPath': 0, 'WithFileExt': 1, 'FileExt': None,
                    'Recurse': 0 }
    DictArgs = DictArgs.copy()
    if not DictArgs:
        DictArgs = KeywArgs    
    for aKey in defaults:
            if not DictArgs.has_key(aKey):
                DictArgs[aKey] = defaults[aKey]
    if DictArgs['Root'] is None: #Root is needed
        return
    
    #Root=os.path.abspath('')
    #print Root
    RFiles = []
    RDirs = []
    if os.path.exists(DictArgs['Root']):
        dirContent = os.listdir(DictArgs['Root'])
    else: #Root not exists
        return RDirs, RFiles
    
    for aFile in dirContent:
        aFileFullName = os.path.join(DictArgs['Root'], aFile)
        if os.path.isdir(aFileFullName): #If a directory
            if DictArgs['WithPath']:
                RDirs.append(aFileFullName)
            else:
                RDirs.append(aFile)
            if DictArgs['Recurse']: #Recursively go into sub-dir
                subDictArgs = DictArgs.copy()
                subDictArgs['Root'] = aFileFullName
                (subDirs, subFiles) = ListFiles(subDictArgs)
                RDirs.extend(subDirs)
                RFiles.extend(subFiles)
        elif os.path.isfile(aFileFullName):
            #Check ext:
            nameAndExt = splitext(aFile)
            exts = Lowercase(DictArgs['FileExt']) #shortcut
            if exts is None: #OK. No restrict to the ext
                pass 
            elif type(exts) is str: #Single ext
                if exts == nameAndExt[1].lower(): #OK
                    pass
                else:
                    continue
            elif type(exts) is list:
                if nameAndExt[1].lower() in exts: #OK
                    pass
                else:
                    continue
            
            if DictArgs['WithPath']:
                RFiles.append(aFileFullName)
            else:
                if DictArgs['WithFileExt']:
                    RFiles.append(aFile)
                else: #No file ext
                    RFiles.append(nameAndExt[0])
        else:
            print aFile, 'is not a directory or file.'
    RDirs.sort()
    #print RDirs
    RFiles.sort()
    #print RFiles
    return RDirs, RFiles

def ListFiles2(Root, Patterns='*', Recurse=1, return_folders=0):
    """=========================================================================
    From "Python cookbook"
    The standard directory-tree function os.path.walk is powerful and flexible, but it can be
    confusing to beginners. This recipe dresses it up in a listFiles function that lets you choose
    the Root folder, whether to recurse down through subfolders, the file patterns to match, and
    whether to include folder names in the result list.
    The file patterns are case-insensitive but otherwise Unix-style, as supplied by the standard
    fnmatch module, which this recipe uses. To specify multiple patterns, join them with a
    semicolon. Note that this means that semicolons themselves can't be part of a pattern.
    For example, you can easily get a list of all Python and HTML files in directory /tmp or any
    subdirectory thereof:
    thefiles = ListFiles2('/tmp', '*.py;*.htm;*.html')
    Example:
        a = ListFiles2('G:\\temp', '*', Recurse=1, return_folders=0)    
        print 'Files: ', a
    ========================================================================="""
    # Expand patterns from semicolon-separated string to list
    pattern_list = Patterns.split(';')
    # Collect input and output arguments into one bunch
    class Bunch:
        def __init__(self, **kwds): self.__dict__.update(kwds)
        
    arg = Bunch(Recurse=Recurse, pattern_list=pattern_list, \
                return_folders=return_folders, results=[])
        
    def visit(arg, dirname, files):
        # Append to arg.results all relevant files (and perhaps folders)
        for name in files:
            fullname = os.path.normpath(os.path.join(dirname, name))
            if arg.return_folders or os.path.isfile(fullname):
                for pattern in arg.pattern_list:
                    if fnmatch.fnmatch(name, pattern):
                        arg.results.append(fullname)
                        break
        # Block recursion if recursion was disallowed
        if not arg.Recurse: files[:]=[]
    os.path.walk(Root, visit, arg)
    
    return arg.results


def RunExternal(Command=None):
    """Run external commands"""
    if Command is None:
        return
    if os.name == 'nt': #Windows
        f = os.popen(Command)
        result = f.read() #readline()
        f.close()
    elif os.name == 'posix': #Linux
        result = commands.getoutput(Command)
    else: #Other platforms
        result = commands.getoutput(Command)
        
    print result
    return result

def GetKey(): #it waits for a key pressed. Not useful
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd) #does not work inside IDE
    new = termios.tcgetattr(fd)
    new[3] = new[3] & ~termios.ICANON & ~termios.ECHO
    new[6][termios.VMIN] = 1
    new[6][termios.VTIME] = 0
    termios.tcsetattr(fd, termios.TCSANOW, new)
    aChr = None
    try:
        aChr = os.read(fd, 1)
        print('len=%i, code=%i' % (len(aChr), ord(aChr)))
        if aChr == 'q':
            print('quit')
    finally:
        termios.tcsetattr(fd, termios.TCSAFLUSH, old)
    return aChr

def PollInputFor(ALookfor=None): #can only get the input after Enter is pressed
    inObj, outObj, errObj = select.select([sys.stdin], [], [], 0.0001)
    for aElem in inObj:
        if aElem == sys.stdin:
            Result = (sys.stdin.readline()).rstrip()
            if ALookfor != None:
                if ALookfor in Result:
                    return True
                else:
                    return False
            else: #if ALookfor is not specified, return true for any char entered
                return True
    return False

def PollInput(ALookfor=None): #can only get the input after Enter is pressed
    inObj, outObj, errObj = select.select([sys.stdin], [], [], 0.0001)
    for aElem in inObj:
        if aElem == sys.stdin:
            Result = (sys.stdin.readline()).rstrip()
            if Result == 'q':
                print('Got quit')
            else:
                print('Got: ' + Result)
            return Result
    return None

def Substitute(adict, text):
    """
    Perform multiple string substitutions on a string using patterns defined
    in a dictionary.
    """
    # Create a regular expression from all of the dictionary keys
    regex = re.compile("|".join(map(re.escape, adict.keys( ))))

    # For each match, look up the corresponding value in the dictionary
    return regex.sub(lambda match: adict[match.group(0)], text)

def SubstituteVariables(StringList=None, Variables=None, Contents=None):
    """
    Replace items in the Variables found in StringList, with corresponding
    item in Contents.
    Input:
        StringList: a string or string list containing variables with leading $.
        Variables: a list of variable names.
        Contents: a list of strings that are used to replace corresponding
                    variables.
    Return:
        The string with new contents.
    """
    if StringList is None or Variables is None or Contents is None:
        return None
    
    if type(StringList) is list:
        allList = []
        for aStr in StringList:
            rStr = SubstituteVariables(aStr, Variables, Contents)
            if rStr is not None:
                allList = allList + [rStr]
        return allList
                
    newWords = []
    oldWords = SplitStringByTokens(StringList)
    #oldWords = StringList.split(' ')
    for aWord in oldWords:
        if (aWord[0:2] == '${') and (aWord[-1] == '}'): #Replace a variable
            if aWord[2:-1] in Variables:
                aWord = Contents[Variables.index(aWord[2:-1])]
        newWords.append(aWord)
    newStr = ''.join(newWords)
        
    return newStr
    
def GetDictVal(ADict=None, AKey=None):
    "Get the value by the given key from the all-string dictionay ignoring case"
    if (ADict is None) or (len(ADict)==0) or (AKey is None) or (len(AKey)==0):
        return None
    for key, val in ADict.iteritems():
        if key.lower()==AKey.lower():
            return val #If a key is found
    return None #If no key found

def GetDictKey(ADict=None, AValue=None):
    "Get the key by the given value from the all-string dictionay ignoring case"
    if ADict is None or AValue is None:
        return
    for key, val in ADict.iteritems():
        for item in val:
            if item.lower()==AValue.lower():
                return key #If a key is found
    return None #If no key found

def GetCurrentOs():
    """See also: sys.platform has a finer granularity. os.uname() gives system-dependent version information.
    """
    osName = os.name
    if (osName == "posix"):
        return os.uname()[0] #Linux
    else:
        return osName

def SyncFileModTime(AFile=None, AMsg=None, AFileModTime=None):
    """
    Problem: when copy files to samba share and one getmtime call follows short after another, it will return the 
             result even before samba is finishing the first one, and the result is wrong. 
             Solution: set the utime without checking if the old and new time are the same.
    Example 1:
    fileModTime = getmtime(origFileFull) 
    SetFileAccessModTime(targetFile, 'Sync mod time to the original', fileModTime)

    Example 2: SyncFileModTime(targetFile, ' Sync the mod time to the original', fileModTime)
    """
    if os.path.exists(AFile):
        #fileAccessTime = os.path.getatime(AFile) #Time of last access
        #fileModTime = os.path.getmtime(AFile) #The time of last content modification
        #if (fileModTime != AFileModTime):
        if AMsg:
            print(AMsg)
        os.utime(AFile, (fileAccessTime, AFileModTime))
    
def SetFileAccModTime(AFile=None, AMsg=None, AFileAccessTime=None, AFileModTime=None):
    """
    Example 1:
fileAccessTime = getatime(origFileFull)
fileModTime = getmtime(origFileFull) 
SetFileAccessModTime(targetFile, fileAccessTime, fileModTime)

    Example 2: SetFileAccessModTime(targetFile, AFileAccessTime, AFileModTime)
    """
    if os.path.exists(AFile):
        #fileModTime = os.path.getmtime(AFile) #The time of last content modification
        #fileAccessTime = os.path.getatime(AFile) #Time of last access
        #if (fileModTime != AFileModTime) or (fileAccessTime != AFileAccessTime):
        if AMsg:
            print(AMsg)
        os.utime(AFile, (AFileAccessTime, AFileModTime))

                         
def MoveFile(ASrc=None, ADest=None):
    """Move file using linux shell command
    """
    if (ASrc == None) or (ADest == None):
        return None
    
    curOs = GetCurrentOs()
    if curOs == 'Linux':
        cmdln = ['mv', ASrc, ADest]
        extProc = subprocess.Popen(cmdln, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        infos = extProc.communicate() #[0]: stdout, [1]: stderr. The stderr has the info
        return infos
    else:
        #print('MoveFile: unsupported OS')
        #return None
        shutil.move(ASrc, ADest)
        return ['', '']
    
def FormatFilePath(APath=None): 
    "Place correct seperator in the path according to OS and add seperator at the end"
    if APath is None:
        return
    APath = os.path.normpath(APath) #Normalize reference and slashes
    
    tem = StripNulls(APath)
    #tem = tem.replace('\\', os.sep) #Now replaced by os.path.normpath()
    #tem = tem.replace('/', os.sep)
    if tem[-1] != os.sep:
        tem = tem + os.sep
    return tem

def JoinFilePath(Path='', Filename=''):
        Result = os.path.join(Path, Filename)
        Result = FormatFilePath(Result)
        return Result

def ParseVariables(StringList=None):
    """
    Parse the variables in a string list. A variable is a string with a leading '$'.
    eg. 'dir $myDir'
    Input:
        StringList: a string or string list.
    Return:
        None: if no variable is found.
        Or a list of variables without the leading '$'.
    """
    if type(StringList) is list:
        allVars = []
        for aStr in StringList:
            rVars = ParseVariables(aStr)
            if rVars is not None:
                allVars = allVars + rVars
        return allVars
    
    if (StringList is None) or (len(StringList) == 0):
        return None
    
    variables = re.findall('(?<=\$\{)\w+(?=\})', StringList) #Variable: ${name}
    if len(variables) == 0:
        return None
    else:
        return variables
    

def SplitStringByTokens(AString='', BeginToken='${', EndToken='}'):
    """
    Split a string by tokens. Such as 'im = ${Im};' to ['im = ', '${Im}, ';']
    Return:
        The list of sub-strings.
    """
    splitedStr = []
    idx = 0
    while idx >= 0:
        idx = AString.find(BeginToken)
        if idx < 0:
            break
        if len(AString[0:idx]) != 0:
            splitedStr.append(AString[0:idx])
        AString = AString[idx:]
        idx = AString.find(EndToken)
        if idx < 0:
            break
        splitedStr.append(AString[0:idx+1])
        AString = AString[idx+1:]
    if len(AString) != 0:
        splitedStr.append(AString) #Append the leftover
    return splitedStr
    
def ReadListFromFile(Filename=None, Delimiter='[ ,\t]'):
    """
    Read multiple lines delimited by the Delimiter from a file into a list of lists.
    Each line is stored in a list in the lists.
    Return:
        result: a list of lists.
    Example:
        result = ReadListFromFile('adni_mprage_hd.txt')
    """
    result = []
    
    if not os.path.exists(Filename):
        Error('File "%s" not found' % (Filename))
        return []
    aFile = file(Filename, 'r')
    lines = aFile.readlines()
    for aLine in lines:
        #aListLn = aLine.strip('\n\r \t').split(Delimiter)
        aListLn = re.split(Delimiter, aLine.strip('\n\r \t'))
        result.append(aListLn)
    aFile.close()
    return result

def TransposeList(Data=None):
    """
    Convert a row list to col list.
    Note: at the moment, can only handle full array (all elements exist).
    Example:
        a = [[1,2],[3,4]]
        b = RowListToColList(a)
    """
    rowList = Data
    nCols = len(rowList[0]) #the number of columns is decided by the 1st row of the data.
    colList = []
    for j in range(0, nCols): #create empty col list
        colList.append([])
    
    for aRow in rowList:
        colIdx = 0
        for elem in aRow:
            if colIdx >= nCols:
                break
            colList[colIdx].append(elem)
            colIdx = colIdx + 1
        
    return colList
    
def ReadColListFromFile(Filename=None, Delimiter='[ ,\t]'):
    """
    Read multiple lines delimited by the Delimiter from a file into a list of lists
    by column. Each column is stored in a list in the list.
    Note: the number of columns is decided by the 1st row of the data.
    Return:
        result: a list of col lists.
    Example:
        a = ReadColListFromFile('test_col_list-short.txt')
    """
    rowList = ReadListFromFile(Filename=Filename, Delimiter=Delimiter)
    colList = TransposeList(rowList)
    return colList

def FindInList(Item=None, ItemList=None):
    """
    Find an item (or items) contained in the items of a list, and return the 
    list of items that containing it.
    Input:
        Item: a string, or a list of strings.
        ItemList: a list of strings.
    Output:
        A list of items in the ItemList containing Item.
    """
    foundList = []
    if Item is None or len(Item) == 0:
        return foundList
    if ItemList is None or len(ItemList) == 0:
        return foundList
    #position = 0
    for aItem in ItemList:
        if type(Item) is str:
            if aItem.find(Item) >= 0:
                foundList.append(aItem)
        elif type(Item) is list:
            ok = 0
            for aword in Item:
                if aItem.find(aword) >= 0:
                    ok = 1
                else:
                    ok = 0
            if ok: #If all strings are found in the item in the list
                foundList.append(aItem)
    return foundList

class NullClass:
    """
    Null objects always and reliably "do nothing."
    """
    #class __impl:
    def __init__(self, *args, **kwargs): 
        pass
    
    def __call__(self, *args, **kwargs): 
        "Ignore method calls."
        return self
    
    def __getattr__(self, mname): 
        "Ignore attribute requests."
        return self

    def __setattr__(self, name, value):
        "Ignore attribute setting."
        return self

    def __delattr__(self, name):
        "Ignore deleting attributes."
        return self

    def __repr__(self):
        "Return a string representation."
        return "<Null>"

    def __str__(self):
        "Convert to a string and return it."
        return "Null"
        
    def __nonzero__(self): 
        return 0
    
    #def __len__(self): return 0 
    
Null = NullClass()

def SetGroup(ItemList=Null, Attr=Null, Value=Null):
    """
    Set a list of objects.
    Example:
        a=testClass('t', 1)
        b=testClass('t', 2)
        SetGroup([a, b], 't', 7)
        print a.t
        print b.t
    """
    if (ItemList==Null) or (Attr==Null) or (Value==Null):
        return 0
    if type(ItemList) == list:
            for aItem in ItemList:
                setattr(aItem, Attr, Value)
    else:
        setattr(ItemList, Attr, Value)

class MetaGroup(list): #NU
    def __init__(self, ItemList=Null):
        list.__init__(self, ItemList)
    
    def __getattr__(self, Attr):
        if type(self.Items) == list:
            resultList = []
            for aItem in self.Items:
                resultList.append(getattr(aItem, Attr))
            return resultList
        else:
            return getattr(self.Items, Attr)
        
    def __setattr__(self, Attr, Value):
        if type(self.Items) == list:
            for aItem in self.Items: #self.__dict__['Items']:
                setattr(aItem, Attr, Value)
        else:
            return setattr(self.Items, Attr, Value)
    
def testMetaGroup():
    #a = MetaGroup(['a', 'b'])
    #print len(a)
    a=testClass('t', 1)
    b=testClass('t', 1)
    m = MetaGroup([a,b])
    m.t = 5
    print m.t
    x=m[0]
    
class testClass:
    def __init__(self, item, value):
        self.item = value
        
    
    
#===============================================================================
# Test and debug
#===============================================================================
if __name__ == '__main__':
    while True:
        #GetKey()
        #PollInput()
        if PollInputFor('q'):
            print('Found q')
        else:
            print('q not found')
        print('sleep')
        time.sleep(3)
        print('wake')
        
    #a = ReadColListFromFile('test_col_list-short.txt')
    
    #curDir = os.path.abspath('')
    #print 'Current dir: ', curDir
    #(dirs, files) = ListFiles(curDir)
    #print 'includes dirs: ', dirs
    #print 'and files: ', files
    
    ##print sys.path
    
    #MyStdOut = StandOut()
    
    #print 'hello'
    #MyStdOut.priority = 4
    #print "You shouldn't see this"
    #MyStdOut.verbosity = 4
    #print 'You should see this'
    #MyStdOut.priority = 0
    #print 'but not this'
    #MyStdOut.write('And you should see this\n', 5)
    #print 'but not this'
    #MyStdOut.filename = 'test.txt'
    #MyStdOut.priority = 5
    #MyStdOut.setall(5)
    #print 'This should go to the file test.txt as well as the screen.'
    #MyStdOut.file_verbosity = 7
    #print '&priority-8;'
    #print 'And this should be printed to both'
    #print '&priority-6;But this should only go to the screen.'
    #print 'And this should be printed to both, again.'
    
    #MyStdOut.close()

    #PrintHeader('test', '1')
    #PrintEnder('test', '1')
    
    #c=Lowercase(['A', 'B', 'c', '1'])
    #c=Lowercase('A')
    
    #a,b = ListFiles(Root='G:\\temp', WithPath=1, WithFileExt=1, Recurse=1)
    #print 'Dir: ', a
    #print 'Files: ', b
    
    #a = ListFiles2('G:\\temp', '*', Recurse=1, return_folders=0)    
    #print 'Files: ', a
    
    #print GetTimeStamp()
    
    #Print('!!!Warning: <GetOneItem()> &priority-6;See this')
    
    #PrintAppHeader()
    #time.sleep(10)
    #PrintAppFooter()
    
    #result = ReadListFromFile('adni_mprage_hd.txt')
    #print result
    
    #testMetaGroup()
    
    #a=testClass('t', 1)
    #b=testClass('t', 2)
    #SetGroup([a, b], 't', 7)
    #print a.t
    #print b.t
    

    
    
    