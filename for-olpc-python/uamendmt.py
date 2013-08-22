# unit uamendmt

from conversion_common import *
import usupport

"""
import uclasses
import uplant
import ufiler
import delphi_compatability
"""

# const
kStartAmendmentString = "start posing change"
kEndAmendmentString = "end posing change"

class PdPlantDrawingAmendment:
    def __init__(self):
        self.partID = 0L
        self.typeOfPart = ""
        self.hide = False
        self.changeColors = False
        self.propagateColors = False
        self.addRotations = False
        self.xRotation = 0.0
        self.yRotation = 0.0
        self.zRotation = 0.0
        self.multiplyScale = False
        self.propagateScale = False
        self.applyAtAge = 0

        self.scaleMultiplier_pct = 100
        self.lengthMultiplier_pct = 100
        self.widthMultiplier_pct = 100

        self.faceColor = usupport.support_rgb(50, 200, 50)
        self.backfaceColor = usupport.support_rgb(20, 150, 20)
        self.lineColor = usupport.support_rgb(40, 100, 40)

    def readFromTextFile(self, inputFile):
        inputLine = ""
        varName = ""
        varValue = ""

        inputLine = inputFile.readln()
        while inputLine != None:
            # plant reads start line; just continue from there
            if inputLine.strip() == "":
                continue
            varName = usupport.stringUpTo(inputLine, "=")
            varValue = usupport.stringBeyond(inputLine, "=")
            if not self.setField(varName, varValue):
                break
            inputLine = inputFile.readln()
        if not string_match(kEndAmendmentString, inputLine):
            raise GeneralException.create("Problem: Expected end of posing change.")

    def readFromMemo(self, aMemo, readingMemoLine):
        inputLine = ""
        varName = ""
        varValue = ""

        while readingMemoLine <= len(aMemo.Lines) - 1:
            # plant reads start line; just continue from there
            inputLine = aMemo.Lines.Strings[readingMemoLine]
            if inputLine.strip() == "":
                continue
            varName = usupport.stringUpTo(inputLine, "=")
            varValue = usupport.stringBeyond(inputLine, "=")
            if not self.setField(varName, varValue):
                break
            readingMemoLine += 1
        if not string_match(kEndAmendmentString, inputLine):
            raise GeneralException.create("Problem: Expected end of posing change.")
        return readingMemoLine

    def setField(self, varName, varValue):
        result = False
        result = True
        if string_match("part number", varName):
            # how deal with problem?
            self.partID = StrToIntDef(varValue, 0)
        elif string_match("part type", varName):
            self.typeOfPart = varValue
        elif string_match("hide", varName):
            self.hide = usupport.strToBool(varValue)
        elif string_match("change colors", varName):
            # read these for possible backward compatibility later, but don't do anything with them
            # self.changeColors := strToBool(varValue)
            result = True
        elif string_match("propagate colors up stem", varName):
            # self.propagateColors := strToBool(varValue)
            result = True
        elif string_match("front face color", varName):
            # self.faceColor := strToIntDef(varValue, 0)
            result = True
        elif string_match("back face color", varName):
            # self.backfaceColor := strToIntDef(varValue, 0)
            result = True
        elif string_match("line color", varName):
            # self.lineColor := strToIntDef(varValue, 0)
            result = True
        elif string_match("rotate", varName):
            self.addRotations = usupport.strToBool(varValue)
        elif string_match("x rotation", varName):
            self.xRotation = float(varValue)
        elif string_match("y rotation", varName):
            self.yRotation = float(varValue)
        elif string_match("z rotation", varName):
            self.zRotation = float(varValue)
        elif string_match("change scale", varName):
            self.multiplyScale = usupport.strToBool(varValue)
        elif string_match("propagate scale change up stem", varName):
            self.propagateScale = usupport.strToBool(varValue)
        elif string_match("3d object scale multiplier", varName):
            self.scaleMultiplier_pct = StrToIntDef(varValue, 100)
        elif string_match("line length multiplier", varName):
            self.lengthMultiplier_pct = StrToIntDef(varValue, 100)
        elif string_match("line width multiplier", varName):
            self.widthMultiplier_pct = StrToIntDef(varValue, 100)
        elif string_match("apply at age", varName):
            # read these for possible backward compatibility later, but don't do anything with them
            # self.applyAtAge := strToIntDef(varValue, 0)
            result = True
        else:
            result = False
        return result

    def writeToTextFile(self, outputFile):
        writeln(outputFile, kStartAmendmentString)
        writeln(outputFile, "  part number =%d" % (self.partID))
        writeln(outputFile, "  part type =" + self.typeOfPart)
        writeln(outputFile, "  hide =" + usupport.boolToStr(self.hide))
        #
        #  writeln(outputFile, "  change colors =" + boolToStr(changeColors));
        #  writeln(outputFile, "  propagate colors up stem =" + boolToStr(propagateColors));
        #  writeln(outputFile, "  front face color =%d" % (faceColor));
        #  writeln(outputFile, "  back face color =%d" % (backfaceColor));
        #  writeln(outputFile, "  line color =%d" % (lineColor));
        #
        writeln(outputFile, "  rotate =" + usupport.boolToStr(self.addRotations))
        writeln(outputFile, "  x rotation =%d" % (int(self.xRotation)))
        writeln(outputFile, "  y rotation =%d" % (int(self.yRotation)))
        writeln(outputFile, "  z rotation =%d" % (int(self.zRotation)))
        writeln(outputFile, "  change scale =" + usupport.boolToStr(self.multiplyScale))
        writeln(outputFile, "  propagate scale change up stem =" + usupport.boolToStr(self.propagateScale))
        writeln(outputFile, "  3d object scale multiplier =%d" % (self.scaleMultiplier_pct))
        writeln(outputFile, "  line length multiplier =%d" % (self.lengthMultiplier_pct))
        writeln(outputFile, "  line width multiplier =%d" % (self.widthMultiplier_pct))
        #
        #  writeln(outputFile, "  apply at age =%d" % (applyAtAge))
        #
        writeln(outputFile, kEndAmendmentString)

    def writeToMemo(self, aMemo):
        aMemo.Lines.Add(kStartAmendmentString)
        aMemo.Lines.Add("  part number =%d" % (self.partID))
        aMemo.Lines.Add("  part type =" + self.typeOfPart)
        aMemo.Lines.Add("  hide =" + usupport.boolToStr(self.hide))
        #
        #  aMemo.lines.add('  change colors =' + boolToStr(changeColors));
        #  aMemo.lines.add('  propagate colors up stem =' + boolToStr(propagateColors));
        #  aMemo.lines.add("  front face color =%d" % (faceColor));
        #  aMemo.lines.add("  back face color =%d" % (backfaceColor));
        #  aMemo.lines.add("  line color =%d" % (lineColor));
        #
        aMemo.Lines.Add("  rotate =" + usupport.boolToStr(self.addRotations))
        aMemo.Lines.Add("  x rotation =%d" % (int(self.xRotation)))
        aMemo.Lines.Add("  y rotation =%d" % (int(self.yRotation)))
        aMemo.Lines.Add("  z rotation =%d" % (int(self.zRotation)))
        aMemo.Lines.Add("  change scale =" + usupport.boolToStr(self.multiplyScale))
        aMemo.Lines.Add("  propagate scale change up stem =" + usupport.boolToStr(self.propagateScale))
        aMemo.Lines.Add("  3d object scale multiplier =%d" % (self.scaleMultiplier_pct))
        aMemo.Lines.Add("  line length multiplier =%d" % (self.lengthMultiplier_pct))
        aMemo.Lines.Add("  line width multiplier =%d" % (self.widthMultiplier_pct))
        #
        #  aMemo.lines.add("  apply at age =%d" % (applyAtAge));
        #
        aMemo.Lines.Add(kEndAmendmentString)

    def getFullName(self):
        result = ""
        result = "%d (" % (self.partID) + self.typeOfPart + ")"
        if self.hide:
            result = result + ", hidden"
        if self.changeColors:
            result = result + ", colored"
        if self.addRotations:
            result = result + ", rotated"
        if self.multiplyScale:
            result = result + ", scaled"
        if self.applyAtAge != 0:
            result = result + " at age %d" % (self.applyAtAge)
        return result

    def streamDataWithFiler(self, filer, cvir):
        PdStreamableObject.streamDataWithFiler(self, filer, cvir)
        self.partID = filer.streamLongint(self.partID)
        self.typeOfPart = filer.streamShortString(self.typeOfPart)
        self.hide = filer.streamBoolean(self.hide)
        self.changeColors = filer.streamBoolean(self.changeColors)
        self.propagateColors = filer.streamBoolean(self.propagateColors)
        filer.streamColorRef(self.faceColor)
        filer.streamColorRef(self.backfaceColor)
        filer.streamColorRef(self.lineColor)
        self.addRotations = filer.streamBoolean(self.addRotations)
        self.xRotation = filer.streamSingle(self.xRotation)
        self.yRotation = filer.streamSingle(self.yRotation)
        self.zRotation = filer.streamSingle(self.zRotation)
        self.multiplyScale = filer.streamBoolean(self.multiplyScale)
        self.propagateScale = filer.streamBoolean(self.propagateScale)
        self.scaleMultiplier_pct = filer.streamSmallint(self.scaleMultiplier_pct)
        self.lengthMultiplier_pct = filer.streamSmallint(self.lengthMultiplier_pct)
        self.widthMultiplier_pct = filer.streamSmallint(self.widthMultiplier_pct)
        self.applyAtAge = filer.streamSmallint(self.applyAtAge)

    def classAndVersionInformation(self, cvir):
        cvir.classNumber = uclasses.kPdPlantDrawingAmendment
        cvir.versionNumber = 0
        cvir.additionNumber = 0

