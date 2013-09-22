#import math
import os

### Minimal set of imports for including in Plantstudio

### Globals
UnassignedColor = None




### Strings

def string_in(sub, string):
    " True if sub in string "
    return ( string.strip().upper().find(sub.strip().upper()) != -1 )

def string_match(sub, string):
    " True if sub == string "
    return ( string.strip().upper() == sub.strip().upper() )

##def string_startsWith(a, b, find=0, uppercase=1, strip=1):
##    return string_match(a, b, find, uppercase, strip, 1)
def string_startsWith(sub, string):
    " True if string starts with sub "
    return ( string.strip().upper().find(sub.strip().upper()) == 0 )

# !! used in writing to put default value if initial structure doesn't have one
# can probably be removed as a cleanup procedure once all is working
def StrToIntDef(value, default):
    try:
        return int(value)
    except ValueError:
        return default




### Refactored Textfile class
class TextFile:
    def __init__(self):
        self.filename = None
        self.fp = None
        self.reading = 0
        self.writing = 0

    def readln(self):
        """ readline and strip carriage return etc
            assumes file is open                       """
        result = self.fp.readline()
        if not result:
            return None
        # remove possible ending chracters of newline and return
        return result.rstrip("\r\n") # can we do with .rstrip()

    def writeln(self, *args):
        self.write(self, *args)
        self.fp.write("\n")

    def write(self, *args):
        for arg in args:
            try:
                self.fp.write(arg)
            except TypeError:
                # handle numbers
                self.fp.write(`arg`)

    def assignFilename(self, filename):
        " set filename but do not open "
        self.filename = filename
        if self.fp:
            self.fp.close()
        self.fp = None
        self.reading = 0
        self.writing = 0

    # replaces Reset below reset_file
    def open_for_reading(self):
        """ close file if open
            open for reading    """
        if self.fp:
            self.fp.close()
        # weird way to open files for reading
        #self.fp = file(self.filename)
        self.fp = open(self.filename, 'rU')
        self.reading = 1

    # replaces ReWrite below
    def open_for_writing(self):
        """ close file if open
            open for writing    """
        if self.fp:
            self.fp.close()
        #self.fp = file(self.filename, "w")
        self.fp = open(self.filename, 'w')
        self.writing = 1

    def close(self):
        self.fp.close()

###
def writeln(textFile, *args):
    write(textFile, *args)
    if isinstance(textFile, TextFile):
        fp = textFile.fp
    else:
        fp = textFile
    fp.write("\n")


def write(textFile, *args):
    if isinstance(textFile, TextFile):
        fp = textFile.fp
    else:
        fp = textFile
    for arg in args:
        try:
            fp.write(arg)
        except TypeError:
            # handle numbers
            fp.write(`arg`)


# !! used in ugenera but not as a file
# !! used in u3dexport in strange way ??
def AssignFile(textFile, filename):
    textFile.filename = filename
    if textFile.fp:
        textFile.fp.close()
    textFile.fp = None
    textFile.reading = 0
    textFile.writing = 0


# open file for reading
# !! used in ugener but not as a file
def Reset(textFile):
    if textFile.fp:
        textFile.fp.close()
    textFile.fp = file(textFile.filename)
    textFile.reading = 1


# !! used in ugener but not as a file (maybe)
def CloseFile(textFile):
    if isinstance(textFile, TextFile):
        fp = textFile.fp
    else:
        fp = textFile
    if fp:
        fp.close()



ExpandFileName = os.path.abspath
ExtractFilePath = os.path.dirname
FileExists = os.path.isfile
ExtractFileName = os.path.basename


# used in usupport
def RenameFile(oldName, newName):
    try:
        os.rename(oldName, newName)
        return 1
    except OSError:
        return 0

# used in usupport
def DeleteFile(fileName):
   try:
       os.remove(fileName)
       return 1
   except OSError:
       return 0

# used in usupport
def ExtractFileExt(filename):
    " get extension from filename "
    return (os.path.splitext(filename)[1])

# used in usupport
def ChangeFileExt(filename, newExtension):
    "replace file extension"
    return (os.path.splitext(filename)[0] + newExtension)




# support classes
# might be for points in UI...?
# should use class SinglePoint
##class Point:

class SinglePoint(object):
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.reservedZ = 0.0

class Rect(object):
    def __init__(self, left=0, top=0, right=0, bottom=0):
        self.Left = left
        self.Top = top
        self.Right = right
        self.Bottom = bottom

    def getWidth(self):
        return self.right - self.left

    def getHeight(self):
        return self.bottom - self.top

    def __getattr__(self, name):
        if name == "width":
            return self.getWidth()
        elif name == "height":
            return self.getHeight()
        else:
            raise AttributeError(name)

