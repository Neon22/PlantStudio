# unit Udomain

from conversion_common import *
import delphi_compatability
import uplant
print uplant
import u3dexport
import uparams
import usection
import ucollect
import usupport
import umath

"""
import uwait
import usstream
import uregistersupport
import uwizard
import umain
import utimeser
import usplash
import uhints
import uplantmn
"""

# const
kMaxWizardQuestions = 30
kMaxWizardColors = 2
kMaxWizardTdos = 3
kMainWindowOrientationHorizontal = 0
kMainWindowOrientationVertical = 1
kMaxMainWindowOrientations = 1
kIncludeSelectedPlants = 0
kIncludeVisiblePlants = 1
kIncludeAllPlants = 2
kIncludeDrawingAreaContents = 3
kMaxIncludeOption = 3
kBreederVariationLow = 0
kBreederVariationMedium = 1
kBreederVariationHigh = 2
kBreederVariationCustom = 3
kBreederVariationNoNumeric = 4
kNoMutation = 0
kLowMutation = 20
kMediumMutation = 60
kHighMutation = 100
kMaxColorOption = 7
kMinResolution = 10
kMaxResolution = 10000
kDefaultResolution = 200
kMinPixels = 10
kMaxPixels = 10000
kMinInches = 0.0
kMaxInches = 100
kExcludeInvisiblePlants = True
kIncludeInvisiblePlants = False
kExcludeNonSelectedPlants = True
kIncludeNonSelectedPlants = False
kMaxCustomColors = 16
kAnimateByXRotation = 0
kAnimateByAge = 1
kDrawFast = 0
kDrawMedium = 1
kDrawBest = 2
kDrawCustom = 3
kMinOutputCylinderFaces = 3
kMaxOutputCylinderFaces = 20
kDefaultV1IniFileName = "PlantStudio.ini"
kDefaultV2IniFileName = "PlantStudio2.ini"
kV2IniAddition = "_v2"
kMaxRecentFiles = 10
kViewPlantsInMainWindowFreeFloating = 1
kViewPlantsInMainWindowOneAtATime = 2
kMaxUnregExportsAllowed = 20
kMaxUnregExportsPerSessionAfterMaxReached = 2
kInPlantMover = True
kNotInPlantMover = False

#pf32bit
# v1.60
# record
class BitmapOptionsStructure:
    def __init__(self):
        self.exportType = 0
        self.colorType = TPixelFormat()
        self.resolution_pixelsPerInch = 0
        self.width_pixels = 0
        self.height_pixels = 0
        self.width_in = 0.0
        self.height_in = 0.0
        self.preserveAspectRatio = False
        self.jpegCompressionRatio = 0
        self.printPreserveAspectRatio = False
        self.printBorderInner = False
        self.printBorderOuter = False
        self.printWidth_in = 0.0
        self.printHeight_in = 0.0
        self.printLeftMargin_in = 0.0
        self.printTopMargin_in = 0.0
        self.printRightMargin_in = 0.0
        self.printBottomMargin_in = 0.0
        self.printBorderWidthInner = 0
        self.printBorderWidthOuter = 0
        self.borderThickness = 0
        self.borderGap = 0
        self.printBorderColorInner = UnassignedColor
        self.printBorderColorOuter = UnassignedColor

# 1 to 100
# don't save these, they are for storing to use during printing only
# record
class NozzleOptionsStructure:
    def __init__(self):
        self.exportType = 0
        self.resolution_pixelsPerInch = 0
        self.colorType = TPixelFormat()
        self.backgroundColor = UnassignedColor
        self.cellSize = delphi_compatability.TPoint()
        self.cellCount = 0

# don't save in settings
# don't save in settings
# record
class NumberedAnimationOptionsStructure:
    def __init__(self):
        self.animateBy = 0
        self.xRotationIncrement = 0
        self.ageIncrement = 0
        self.resolution_pixelsPerInch = 0
        self.colorType = TPixelFormat()
        self.frameCount = 0
        self.scaledSize = delphi_compatability.TPoint()
        self.fileSize = 0L

# don't save in settings
# don't save in settings
# don't save in settings
# record
class DomainOptionsStructure:
    def __init__(self):
        self.hideWelcomeForm = False
        self.openMostRecentFileAtStart = False
        self.ignoreWindowSettingsInFile = False
        self.cachePlantBitmaps = False
        self.memoryLimitForPlantBitmaps_MB = 0
        self.maxPartsPerPlant_thousands = 10
        self.backgroundColor = delphi_compatability.clWhite
        self.transparentColor = UnassignedColor
        self.showSelectionRectangle = False
        self.showBoundsRectangle = False
        self.resizeRectSize = 0
        self.pasteRectSize = 0
        self.firstSelectionRectangleColor = delphi_compatability.clRed
        self.multiSelectionRectangleColor = delphi_compatability.clBlue
        self.draw3DObjects = True
        self.drawStems = True
        self.fillPolygons = True
        self.drawSpeed = kDrawBest
        self.drawLinesBetweenPolygons = False
        self.sortPolygons = False
        self.draw3DObjectsAsBoundingRectsOnly = False
        self.showPlantDrawingProgress = False
        self.useMetricUnits = False
        self.undoLimit = 0
        self.undoLimitOfPlants = 0
        self.rotationIncrement = 0
        self.showLongHintsForButtons = False
        self.showHintsForParameters = False
        self.pauseBeforeHint = 0
        self.pauseDuringHint = 0
        self.noteEditorWrapLines = False
        self.updateTimeSeriesPlantsOnParameterChange = False
        self.mainWindowViewMode = 0
        self.nudgeDistance = 0
        self.resizeKeyUpMultiplierPercent = 0
        self.parametersFontSize = 0
        self.mainWindowOrientation = 0
        self.lineContrastIndex = 0
        self.sortTdosAsOneItem = False
        self.circlePointSizeInTdoEditor = 0
        self.partsInTdoEditor = 0
        self.fillTrianglesInTdoEditor = False
        self.drawLinesInTdoEditor = False
        self.showGhostingForHiddenParts = False
        self.showHighlightingForNonHiddenPosedParts = False
        self.showPosingAtAll = False
        self.ghostingColor = UnassignedColor
        self.nonHiddenPosedColor = UnassignedColor
        self.selectedPosedColor = UnassignedColor
        self.showWindowOnException = False
        self.logToFileOnException = False
        self.wizardChoices = [0] * (kMaxWizardQuestions + 1)
        self.wizardColors = [0] * (kMaxWizardColors + 1)
        self.wizardTdoNames = [0] * (kMaxWizardTdos + 1)
        self.wizardShowFruit = False
        self.customColors = [0] * (kMaxCustomColors + 1)
        self.recentFiles = [0] * (kMaxRecentFiles + 1)

# const
kUnsavedFileName = "untitled"
kSectionFiles = 0
kSectionPrefs = 1
kSectionSettings = 2
kSectionDXF = 3
kSectionWizard = 4
kSectionExport = 5
kSectionPrinting = 6
kCustomColors = 7
kSectionBreeding = 8
kSectionNozzle = 9
kSectionAnimation = 10
kSectionRegistration = 11
kSectionOverrides = 12
kSectionPOV = 13
kSection3DS = 14
kSectionOBJ = 15
kSectionVRML = 16
kSectionLWO = 17
kSectionOtherRecentFiles = 18
kLastSectionNumber = 18
iniSections = ["Files", "Preferences", "Settings", "DXF", "Wizard", "Picture export", "Printing", "Custom colors", "Breeding", "Nozzles", "Animation", "Registration", "Overrides", "POV", "3DS", "OBJ", "VRML", "LWO", "Other recent files", ]
kStandardTdoLibraryFileName = "3D object library.tdo"
kEncryptingMultiplierForAccumulatedUnregisteredTime = 20
kEncryptingMultiplierForUnregisteredExportCount = 149
kKeyForAccumulatedUnregisteredTime = "Time scale fraction"
kKeyForUnregisteredExportCount = "Frame count"
kGetKeys = True
kGetValues = False

# v2.1
# v2.0
#seconds
#seconds
# v1.4
#cfk change length if needed
class PdDomain:
    def __init__(self):
        self.plantFileName = ""
        self.lastOpenedPlantFileName = ""
        self.plantFileLoaded = False
        self.options = DomainOptionsStructure()
        self.breedingAndTimeSeriesOptions = uplant.BreedingAndTimeSeriesOptionsStructure()
        self.bitmapOptions = BitmapOptionsStructure()
        self.exportOptionsFor3D = []
        for i in range(u3dexport.k3DExportTypeLast + 1):
            self.exportOptionsFor3D.append(u3dexport.FileExport3DOptionsStructure())
        self.nozzleOptions = NozzleOptionsStructure()
        self.animationOptions = NumberedAnimationOptionsStructure()
        self.registered = False
        self.justRegistered = False
        self.startTimeThisSession = 0
        self.accumulatedUnregisteredTime = 0
        self.registrationName = ""
        self.registrationCode = ""
        self.unregisteredExportCountBeforeThisSession = 0
        self.unregisteredExportCountThisSession = 0
        self.plantManager = None
        self.sectionManager = usection.PdSectionManager()
        self.parameterManager = uparams.PdParameterManager()
        self.hintManager = None
        self.iniFileName = ""
        self.iniFileBackupName = ""
        self.useIniFile = False
        self.defaultTdoLibraryFileName = ""
        self.mainWindowRect = delphi_compatability.TRect()
        self.horizontalSplitterPos = 0
        self.verticalSplitterPos = 0
        self.breederWindowRect = delphi_compatability.TRect()
        self.timeSeriesWindowRect = delphi_compatability.TRect()
        self.debugWindowRect = delphi_compatability.TRect()
        self.undoRedoListWindowRect = delphi_compatability.TRect()
        self.tdoEditorWindowRect = delphi_compatability.TRect()
        self.temporarilyHideSelectionRectangles = False
        self.drawingToMakeCopyBitmap = False
        self.plantDrawScaleWhenDrawingCopy_PixelsPerMm = 1.0
        self.plantDrawOffsetWhenDrawingCopy_mm = SinglePoint()
        self.iniLines = ucollect.TListCollection()
        self.gotInfoFromV1IniFile = False


        """ PDF PORT __ COMMENTED OUT FOR NOTW FOR TESTING
        # v1.5
        usupport.setDecimalSeparator()
        # create empty managers
        self.plantManager = uplantmn.PdPlantManager()
        self.hintManager = uhints.PdHintManager()
        self.iniLines = delphi_compatability.TStringList.create
        # non-standard defaults
        self.plantManager.plantDrawScale_PixelsPerMm = 1.0
        """

    # registration
    # managers
    # support files
    # for remembering settings
    # for temporary use while drawing
    # for making copy bitmap with different resolution than screen
    # ------------------------------------------------------------------------------- creation/destruction
    def createDefault(self):
        result = False
        domain = PdDomain()
        result = domain.startupLoading()
        return result

    def destroyDefault(self):
        domain.free
        domain = None

    def windowsDirectory(self):
        result = ""
        cString = [0] * (range(0, 255 + 1) + 1)

        result = ""
        UNRESOLVED.getWindowsDirectory(cString, 256)
        result = UNRESOLVED.strPas(cString)
        return result

    # ------------------------------------------------------------------------------- loading
    def startupLoading(self):
        result = False
        i = 0
        iniFileFound = False
        year = 0
        month = 0
        day = 0
        v1IniFileName = ""

        result = True
        self.iniFileName = kDefaultV2IniFileName
        self.useIniFile = True
        self.plantFileName = ""
        if usplash.splashForm != None:
            usplash.splashForm.showLoadingString("Starting...")
        if UNRESOLVED.ParamCount > 0:
            for i in range(1, UNRESOLVED.ParamCount + 1):
                if UNRESOLVED.ParamStr(i).upper() == "/I=":
                    # ============= parse command line options
                    self.useIniFile = False
                elif UNRESOLVED.ParamStr(i).upper() == "/I":
                    self.useIniFile = False
                elif UNRESOLVED.pos("/I=", UNRESOLVED.ParamStr(i)).upper() == 1:
                    self.iniFileName = UNRESOLVED.copy(UNRESOLVED.ParamStr(i), 4, len(UNRESOLVED.ParamStr(i)))
                elif UNRESOLVED.pos("/I", UNRESOLVED.ParamStr(i)).upper() == 1:
                    self.iniFileName = UNRESOLVED.copy(UNRESOLVED.ParamStr(i), 3, len(UNRESOLVED.ParamStr(i)))
                elif (self.plantFileName == "") and (UNRESOLVED.pos("/", UNRESOLVED.ParamStr(i)).upper() != 1):
                    self.plantFileName = UNRESOLVED.ParamStr(i)
                else:
                    ShowMessage("Improper parameter string " + UNRESOLVED.ParamStr(i))
        # make parameters
        self.parameterManager.makeParameters()
        # make hints
        self.hintManager.makeHints()
        # v2.0
        # reconcile v2 and v1 ini files
        # only do this if they did NOT specify an alternate file
        # if they specified an alternate file, there is no way to know what version it is;
        # just read it as v1 and write it as v2 (do not expect this to be common use)
        # if they asked NOT to read any ini file, skip doing this
        self.gotInfoFromV1IniFile = False
        if (self.useIniFile) and (self.iniFileName == kDefaultV2IniFileName):
            if not FileExists(self.windowsDirectory() + "\\" + self.iniFileName):
                # if no v2 ini file but there is a v1 ini file, read the v1 ini file NOW but do not change the name for writing out
                v1IniFileName = self.windowsDirectory() + "\\" + kDefaultV1IniFileName
                if FileExists(v1IniFileName):
                    self.getProfileInformationFromFile(v1IniFileName)
                    self.gotInfoFromV1IniFile = True
        if ExtractFilePath(self.iniFileName) != "":
            # find out if ini file exists now, because if it doesn't we should save the profile info when leaving
            #    even if it did not change. if iniFileName does not have a directory, use Windows directory
            iniFileFound = FileExists(self.iniFileName)
            if not iniFileFound:
                ShowMessage("Could not find alternate settings file " + chr(13) + chr(13) + "  " + self.iniFileName + chr(13) + chr(13) + "Using standard settings file in Windows directory instead.")
                self.iniFileName = kDefaultV2IniFileName
                iniFileFound = FileExists(self.windowsDirectory() + "\\" + self.iniFileName)
                self.iniFileName = self.windowsDirectory() + "\\" + self.iniFileName
        else:
            iniFileFound = FileExists(self.windowsDirectory() + "\\" + self.iniFileName)
            self.iniFileName = self.windowsDirectory() + "\\" + self.iniFileName
        usupport.iniFileChanged = not iniFileFound
        if iniFileFound and self.useIniFile:
            # ============= if ini file doesn't exist or don't want, set default options; otherwise read options from ini file
            # if already read options from v1 ini file, don't default - v2.0
            self.getProfileInformationFromFile(self.iniFileName)
        elif not self.gotInfoFromV1IniFile:
            # defaults options
            self.getProfileInformationFromFile("")
        self.startTimeThisSession = UNRESOLVED.Now
        if self.plantFileName != "":
            try:
                if usplash.splashForm != None:
                    # ============= load plant file from command line if found
                    usplash.splashForm.showLoadingString("Reading startup file...")
                self.plantFileName = self.buildFileNameInPath(self.plantFileName)
                self.load(self.plantFileName)
            except Exception, E:
                ShowMessage(E.message)
                ShowMessage("Could not open plant file from command line " + self.plantFileName)
        elif (self.useIniFile) and (self.options.openMostRecentFileAtStart):
            # ============= if most recent plant file in INI try it unless -I option
            # assume ini file has been read by now
            self.plantFileName = self.stringForSectionAndKey("Files", "Recent", self.plantFileName)
            self.plantFileName = self.buildFileNameInPath(self.plantFileName)
            if (self.plantFileName != "") and self.isFileInPath(self.plantFileName):
                try:
                    if usplash.splashForm != None:
                        usplash.splashForm.showLoadingString("Reading most recent file...")
                    self.load(self.plantFileName)
                except Exception, E:
                    ShowMessage(E.message)
                    ShowMessage("Could not load most recently saved plant file " + self.plantFileName)
        # show obsolete warning if unregistered
        UNRESOLVED.DecodeDate(UNRESOLVED.Now, year, month, day)
        if (not self.registered) and (year >= 2003):
            MessageDialog("This version of PlantStudio was released some time ago." + chr(13) + chr(13) + "Please check for an newer version at:" + chr(13) + "  http://www.kurtz-fernhout.com" + chr(13) + chr(13) + "The web site may also have updated pricing information." + chr(13) + chr(13) + "You can still register this copy of the software if you want to, though;" + chr(13) + "this message will disappear when this copy is registered.", mtInformation, [mbOK, ], 0)
        return result

    # --------------------------------------------------------------------------------- ini file methods referred to
    def sectionStartIndexInIniLines(self, section):
        result = -1
        i = 0
        while i < len(self.iniLines):
            aLine = self.iniLines[i].strip()
            if "[" + section + "]" == aLine:
                result = i
                return result
            else:
                i += 1
        return result

    def stringForSectionAndKey(self, section, key, defaultString):
        result = defaultString
        if (self.iniLines == None) or (len(self.iniLines) <= 0):
            return result
        i = self.sectionStartIndexInIniLines(section)
        if i < 0:
            return result
        # move to next after section
        i += 1
        while (i < len(self.iniLines)):
            # only read up until next section - don't want to get same name from different section
            aLine = self.iniLines.Strings[i].strip()
            if (len(aLine) > 0) and (aLine[0] == "["):
                return result
            if key == usupport.stringUpTo(aLine, "=").strip():
                result = usupport.stringBeyond(self.iniLines[i], "=")
                return result
            else:
                i += 1
        return result

    def setStringForSectionAndKey(self, section, key, newString):
        if (self.iniLines == None):
            return
        i = self.sectionStartIndexInIniLines(section)
        if i < 0:
            # if no section found, add section at end and add this one item to it
            self.iniLines.Add("[" + section + "]")
            self.iniLines.Add(key + "=" + newString)
            # section found
        else:
            found = False
            # move to next after section
            i += 1
            while i < len(self.iniLines):
                # only read up until next section - don't want to get same name from different section
                aLine = self.iniLines[i].strip()
                if (len(aLine) > 0) and (aLine[1] == "["):
                    break
                if key == usupport.stringUpTo(self.iniLines[i], "=").strip():
                    self.iniLines[i] = key + "=" + newString
                    found = True
                    break
                else:
                    i += 1
            if not found:
                if i < len(self.iniLines):
                    # if there was no match for the key, ADD a line to the section
                    self.iniLines.Insert(i, key + "=" + newString)
                else:
                    self.iniLines.Add(key + "=" + newString)

    def readSectionKeysOrValues(self, section, aList, getKeys):
        i = 0
        aLine = ""

        if (self.iniLines == None) or (len(self.iniLines) <= 0):
            return
        i = self.sectionStartIndexInIniLines(section)
        if i < 0:
            return
        # move to next after section
        i += 1
        while i < len(self.iniLines):
            aLine = self.iniLines[i].strip()
            if (len(aLine) > 0) and (aLine[1] == "["):
                break
            if getKeys:
                # values
                aList.Add(usupport.stringUpTo(self.iniLines.Strings[i], "=").strip())
            else:
                aList.Add(usupport.stringBeyond(self.iniLines.Strings[i], "="))
            i += 1

    def removeSectionFromIniLines(self, section):
        if (self.iniLines == None) or (len(self.iniLines) <= 0):
            return
        i = self.sectionStartIndexInIniLines(section)
        if i < 0:
            return
        self.iniLines.Delete(i)
        while i < len(self.iniLines):
            aLine = self.iniLines.Strings[i].strip()
            if (len(aLine) > 0) and (aLine[0] == "["):
                break
            self.iniLines.Delete(i)

    # --------------------------------------------------------------------------------- ini file load/save
    def getProfileInformationFromFile(self, fileName):
        if fileName != "":
            self.iniLines.LoadFromFile(fileName)
        # ------------------------------------------- files
        section = iniSections[kSectionFiles]
        # PDF PORT FIX
        #filPath = ExtractFilePath(delphi_compatability.Application.exeName)
        filePath = ""
        self.defaultTdoLibraryFileName = self.stringForSectionAndKey(section, "3D object library", filePath + "3D object library.tdo")
        # ------------------------------------------- recent files
        section = iniSections[kSectionOtherRecentFiles]
        for i in range(0, kMaxRecentFiles):
            self.options.recentFiles[i] = self.stringForSectionAndKey(section, "File %d" % (i + 1), "")
        # ------------------------------------------- preferences
        section = iniSections[kSectionPrefs]
        self.options.openMostRecentFileAtStart = usupport.strToBool(self.stringForSectionAndKey(section, "Open most recent file at start", "True"))
        self.options.ignoreWindowSettingsInFile = usupport.strToBool(self.stringForSectionAndKey(section, "Ignore window settings saved in files", "False"))
        self.options.cachePlantBitmaps = usupport.strToBool(self.stringForSectionAndKey(section, "Draw plants into separate bitmaps", "True"))
        self.options.memoryLimitForPlantBitmaps_MB = int(self.stringForSectionAndKey(section, "Memory limit for plant bitmaps (in MB)", "5"))
        self.options.maxPartsPerPlant_thousands = int(self.stringForSectionAndKey(section, "Max parts per plant (in thousands)", "10"))
        self.options.hideWelcomeForm = usupport.strToBool(self.stringForSectionAndKey(section, "Hide welcome window", "False"))
        self.options.backgroundColor = int(self.stringForSectionAndKey(section, "Background color", "%d" % (delphi_compatability.clWhite)))
        self.options.transparentColor = int(self.stringForSectionAndKey(section, "Transparent color", "%d" % (delphi_compatability.clWhite)))
        self.options.showSelectionRectangle = usupport.strToBool(self.stringForSectionAndKey(section, "Show selection rectangle", "True"))
        self.options.showBoundsRectangle = usupport.strToBool(self.stringForSectionAndKey(section, "Show bounding rectangle", "False"))
        self.options.resizeRectSize = int(self.stringForSectionAndKey(section, "Resizing rectangle size", "6"))
        self.options.pasteRectSize = int(self.stringForSectionAndKey(section, "Paste rectangle size", "100"))
        self.options.firstSelectionRectangleColor = int(self.stringForSectionAndKey(section, "First selection rectangle color", "%d" % (delphi_compatability.clRed)))
        self.options.multiSelectionRectangleColor = int(self.stringForSectionAndKey(section, "Multi selection rectangle color", "%d" % (delphi_compatability.clBlue)))
        self.options.draw3DObjects = usupport.strToBool(self.stringForSectionAndKey(section, "Draw 3D objects", "True"))
        self.options.drawStems = usupport.strToBool(self.stringForSectionAndKey(section, "Draw stems", "True"))
        self.options.fillPolygons = usupport.strToBool(self.stringForSectionAndKey(section, "Fill polygons", "True"))
        self.options.drawSpeed = int(self.stringForSectionAndKey(section, "Draw speed (boxes/frames/solids)", "%d" % (kDrawBest)))
        self.options.drawLinesBetweenPolygons = usupport.strToBool(self.stringForSectionAndKey(section, "Draw lines between polygons", "True"))
        self.options.sortPolygons = usupport.strToBool(self.stringForSectionAndKey(section, "Sort polygons", "True"))
        self.options.draw3DObjectsAsBoundingRectsOnly = usupport.strToBool(self.stringForSectionAndKey(section, "Draw 3D objects as squares", "False"))
        self.options.showPlantDrawingProgress = usupport.strToBool(self.stringForSectionAndKey(section, "Show drawing progress", "True"))
        self.options.useMetricUnits = usupport.strToBool(self.stringForSectionAndKey(section, "Use metric units", "True"))
        self.options.undoLimit = int(self.stringForSectionAndKey(section, "Actions to keep in undo list", "50"))
        self.options.undoLimitOfPlants = int(self.stringForSectionAndKey(section, "Plants to keep in undo list", "10"))
        self.options.rotationIncrement = int(self.stringForSectionAndKey(section, "Rotation button increment", "10"))
        self.options.showLongHintsForButtons = usupport.strToBool(self.stringForSectionAndKey(section, "Show long hints for buttons", "True"))
        self.options.showHintsForParameters = usupport.strToBool(self.stringForSectionAndKey(section, "Show hints for parameters", "True"))
        self.options.pauseBeforeHint = int(self.stringForSectionAndKey(section, "Pause before hint", "1"))
        self.options.pauseDuringHint = int(self.stringForSectionAndKey(section, "Pause during hint", "60"))
        self.options.noteEditorWrapLines = usupport.strToBool(self.stringForSectionAndKey(section, "Wrap lines in note editor", "True"))
        self.options.updateTimeSeriesPlantsOnParameterChange = usupport.strToBool(self.stringForSectionAndKey(section, "Update time series plants on parameter change", "True"))
        self.options.mainWindowViewMode = int(self.stringForSectionAndKey(section, "Main window view option (all/one)", "0"))
        self.options.nudgeDistance = int(self.stringForSectionAndKey(section, "Distance plant moves with Control-arrow key", "5"))
        self.options.resizeKeyUpMultiplierPercent = int(self.stringForSectionAndKey(section, "Percent size increase with Control-Shift-up-arrow key", "110"))
        self.options.parametersFontSize = int(self.stringForSectionAndKey(section, "Parameter panels font size", "8"))
        self.options.mainWindowOrientation = int(self.stringForSectionAndKey(section, "Main window orientation (horiz/vert)", "0"))
        self.options.lineContrastIndex = int(self.stringForSectionAndKey(section, "Contrast index for lines on polygons", "3"))
        self.options.sortTdosAsOneItem = usupport.strToBool(self.stringForSectionAndKey(section, "Sort 3D objects as one item", "True"))
        self.options.circlePointSizeInTdoEditor = int(self.stringForSectionAndKey(section, "3D object editor point size", "8"))
        self.options.partsInTdoEditor = int(self.stringForSectionAndKey(section, "3D object editor parts", "1"))
        self.options.fillTrianglesInTdoEditor = usupport.strToBool(self.stringForSectionAndKey(section, "3D object editor fill triangles", "True"))
        self.options.drawLinesInTdoEditor = usupport.strToBool(self.stringForSectionAndKey(section, "3D object editor draw lines", "True"))
        self.options.showWindowOnException = usupport.strToBool(self.stringForSectionAndKey(section, "Show numerical exceptions window on exception", "False"))
        self.options.logToFileOnException = usupport.strToBool(self.stringForSectionAndKey(section, "Log to file on exception", "False"))
        self.options.showGhostingForHiddenParts = usupport.strToBool(self.stringForSectionAndKey(section, "Ghost hidden parts", "False"))
        self.options.showHighlightingForNonHiddenPosedParts = usupport.strToBool(self.stringForSectionAndKey(section, "Highlight posed parts", "True"))
        self.options.showPosingAtAll = usupport.strToBool(self.stringForSectionAndKey(section, "Show posing", "True"))
        self.options.ghostingColor = int(self.stringForSectionAndKey(section, "Ghosting color", "%d" % (delphi_compatability.clSilver)))
        self.options.nonHiddenPosedColor = int(self.stringForSectionAndKey(section, "Posed color", "%d" % (delphi_compatability.clBlue)))
        self.options.selectedPosedColor = int(self.stringForSectionAndKey(section, "Posed selected color", "%d" % (delphi_compatability.clRed)))
        # ------------------------------------------- settings
        section = iniSections[kSectionSettings]
        self.mainWindowRect = usupport.stringToRect(self.stringForSectionAndKey(section, "Window position", "50 50 500 350"))
        self.horizontalSplitterPos = int(self.stringForSectionAndKey(section, "Horizontal split", "200"))
        self.verticalSplitterPos = int(self.stringForSectionAndKey(section, "Vertical split", "200"))
        self.debugWindowRect = usupport.stringToRect(self.stringForSectionAndKey(section, "Numerical exceptions window position", "75 75 400 200"))
        self.undoRedoListWindowRect = usupport.stringToRect(self.stringForSectionAndKey(section, "Undo/redo list window position", "100 100 400 300"))
        self.tdoEditorWindowRect = usupport.stringToRect(self.stringForSectionAndKey(section, "3D object editor window position", "100 100 400 400"))
        self.breederWindowRect = usupport.stringToRect(self.stringForSectionAndKey(section, "Breeder position", "100 100 400 350"))
        self.timeSeriesWindowRect = usupport.stringToRect(self.stringForSectionAndKey(section, "Time series position", "150 150 250 150"))
        for i in range(1, u3dexport.k3DExportTypeLast + 1):
            # ------------------------------------------- 3d export options
            section = iniSections[self.sectionNumberFor3DExportType(i)]
            typeName = u3dexport.nameFor3DExportType(i)
            # ------------------------------------------- options in common for all
            self.exportOptionsFor3D[i].exportType = int(self.stringForSectionAndKey(section, typeName + " which plants to draw (selected/visible/all)", "0"))
            self.exportOptionsFor3D[i].layeringOption = int(self.stringForSectionAndKey(section, typeName + " layering option (all/by type/by part)", "1"))
            self.exportOptionsFor3D[i].stemCylinderFaces = int(self.stringForSectionAndKey(section, typeName + " stem cylinder sides", "5"))
            self.exportOptionsFor3D[i].translatePlantsToWindowPositions = usupport.strToBool(self.stringForSectionAndKey(section, typeName + " translate plants to match window positions", "True"))
            if i == u3dexport.k3DS:
                self.exportOptionsFor3D[i].lengthOfShortName = int(self.stringForSectionAndKey(section, typeName + " length of plant name", "2"))
            else:
                self.exportOptionsFor3D[i].lengthOfShortName = int(self.stringForSectionAndKey(section, typeName + " length of plant name", "8"))
            self.exportOptionsFor3D[i].writePlantNumberInFrontOfName = usupport.strToBool(self.stringForSectionAndKey(section, typeName + " write plant number in front of name", "False"))
            self.exportOptionsFor3D[i].writeColors = usupport.strToBool(self.stringForSectionAndKey(section, typeName + " write colors", "True"))
            self.exportOptionsFor3D[i].xRotationBeforeDraw = int(self.stringForSectionAndKey(section, typeName + " X rotation before drawing", "0"))
            self.exportOptionsFor3D[i].overallScalingFactor_pct = int(self.stringForSectionAndKey(section, typeName + " scaling factor (percent)", "100"))
            self.exportOptionsFor3D[i].pressPlants = usupport.strToBool(self.stringForSectionAndKey(section, typeName + " press plants", "False"))
            self.exportOptionsFor3D[i].directionToPressPlants = int(self.stringForSectionAndKey(section, typeName + " press dimension (x/y/z)", "%d" % (u3dexport.kY)))
            self.exportOptionsFor3D[i].makeTrianglesDoubleSided = usupport.strToBool(self.stringForSectionAndKey(section, typeName + " double sided", "True"))
            if i == u3dexport.kDXF:
                # ------------------------------------------- special options
                self.exportOptionsFor3D[i].dxf_whereToGetColors = int(self.stringForSectionAndKey(section, "DXF colors option (by type/by part/all)", "0"))
                # lime
                self.exportOptionsFor3D[i].dxf_wholePlantColorIndex = int(self.stringForSectionAndKey(section, "DXF whole plant color index", "2"))
                for j in range(0, u3dexport.kExportPartLast + 1):
                    # lime
                    self.exportOptionsFor3D[i].dxf_plantPartColorIndexes[j] = int(self.stringForSectionAndKey(section, "DXF color indexes %d" % (j + 1), "2"))
            elif i == u3dexport.kPOV:
                self.exportOptionsFor3D[i].pov_minLineLengthToWrite = usupport.strToFloatWithCommaCheck(self.stringForSectionAndKey(section, "POV minimum line length to write (mm)", "0.01"))
                self.exportOptionsFor3D[i].pov_minTdoScaleToWrite = usupport.strToFloatWithCommaCheck(self.stringForSectionAndKey(section, "POV minimum 3D object scale to write", "0.01"))
                self.exportOptionsFor3D[i].pov_commentOutUnionAtEnd = usupport.strToBool(self.stringForSectionAndKey(section, "POV comment out union of plants at end", "False"))
            elif i == u3dexport.kVRML:
                self.exportOptionsFor3D[i].vrml_version = int(self.stringForSectionAndKey(section, "VRML version", "1"))
            if (i == u3dexport.kPOV) or (i == u3dexport.kVRML):
                self.exportOptionsFor3D[i].nest_LeafAndPetiole = usupport.strToBool(self.stringForSectionAndKey(section, typeName + " nest leaves with petioles", "True"))
                self.exportOptionsFor3D[i].nest_CompoundLeaf = usupport.strToBool(self.stringForSectionAndKey(section, typeName + " compound leaves", "True"))
                self.exportOptionsFor3D[i].nest_Inflorescence = usupport.strToBool(self.stringForSectionAndKey(section, typeName + " nest inflorescences", "True"))
                self.exportOptionsFor3D[i].nest_PedicelAndFlowerFruit = usupport.strToBool(self.stringForSectionAndKey(section, typeName + " nest flowers/fruits with pedicels", "True"))
                self.exportOptionsFor3D[i].nest_FloralLayers = usupport.strToBool(self.stringForSectionAndKey(section, typeName + " nest pistils and stamens", "True"))
        # ------------------------------------------- wizard
        #PDF PORT TEMPORARILY COMMENTED OUT WIZARD
        """
        section = iniSections[kSectionWizard]
        # meristems
        self.options.wizardChoices[uwizard.kMeristem_AlternateOrOpposite] = self.stringForSectionAndKey(section, "Wizard question %d" % (uwizard.kMeristem_AlternateOrOpposite), "leavesAlternate")
        self.options.wizardChoices[uwizard.kMeristem_BranchIndex] = self.stringForSectionAndKey(section, "Wizard question %d" % (uwizard.kMeristem_BranchIndex), "branchNone")
        self.options.wizardChoices[uwizard.kMeristem_SecondaryBranching] = self.stringForSectionAndKey(section, "Wizard question %d" % (uwizard.kMeristem_SecondaryBranching), "secondaryBranchingNo")
        self.options.wizardChoices[uwizard.kMeristem_BranchAngle] = self.stringForSectionAndKey(section, "Wizard question %d" % (uwizard.kMeristem_BranchAngle), "branchAngleSmall")
        # internodes
        self.options.wizardChoices[uwizard.kInternode_Curviness] = self.stringForSectionAndKey(section, "Wizard question %d" % (uwizard.kInternode_Curviness), "curvinessLittle")
        self.options.wizardChoices[uwizard.kInternode_Length] = self.stringForSectionAndKey(section, "Wizard question %d" % (uwizard.kInternode_Length), "internodesMedium")
        self.options.wizardChoices[uwizard.kInternode_Thickness] = self.stringForSectionAndKey(section, "Wizard question %d" % (uwizard.kInternode_Thickness), "internodeWidthThin")
        # leaves
        self.options.wizardChoices[uwizard.kLeaves_Scale] = self.stringForSectionAndKey(section, "Wizard question %d" % (uwizard.kLeaves_Scale), "leafScaleMedium")
        self.options.wizardChoices[uwizard.kLeaves_PetioleLength] = self.stringForSectionAndKey(section, "Wizard question %d" % (uwizard.kLeaves_PetioleLength), "petioleMedium")
        self.options.wizardChoices[uwizard.kLeaves_Angle] = self.stringForSectionAndKey(section, "Wizard question %d" % (uwizard.kLeaves_Angle), "leafAngleMedium")
        # compound leaves
        self.options.wizardChoices[uwizard.kLeaflets_Number] = self.stringForSectionAndKey(section, "Wizard question %d" % (uwizard.kLeaflets_Number), "leafletsOne")
        self.options.wizardChoices[uwizard.kLeaflets_Shape] = self.stringForSectionAndKey(section, "Wizard question %d" % (uwizard.kLeaflets_Shape), "leafletsPinnate")
        self.options.wizardChoices[uwizard.kLeaflets_Spread] = self.stringForSectionAndKey(section, "Wizard question %d" % (uwizard.kLeaflets_Spread), "leafletSpacingMedium")
        # inflor placement
        self.options.wizardChoices[uwizard.kInflorPlace_NumApical] = self.stringForSectionAndKey(section, "Wizard question %d" % (uwizard.kInflorPlace_NumApical), "apicalInflorsNone")
        self.options.wizardChoices[uwizard.kInflorPlace_ApicalStalkLength] = self.stringForSectionAndKey(section, "Wizard question %d" % (uwizard.kInflorPlace_ApicalStalkLength), "apicalStalkMedium")
        self.options.wizardChoices[uwizard.kInflorPlace_NumAxillary] = self.stringForSectionAndKey(section, "Wizard question %d" % (uwizard.kInflorPlace_NumAxillary), "axillaryInflorsNone")
        self.options.wizardChoices[uwizard.kInflorPlace_AxillaryStalkLength] = self.stringForSectionAndKey(section, "Wizard question %d" % (uwizard.kInflorPlace_AxillaryStalkLength), "axillaryStalkMedium")
        # inflor drawing
        self.options.wizardChoices[uwizard.kInflorDraw_NumFlowers] = self.stringForSectionAndKey(section, "Wizard question %d" % (uwizard.kInflorDraw_NumFlowers), "inflorFlowersThree")
        self.options.wizardChoices[uwizard.kInflorDraw_Shape] = self.stringForSectionAndKey(section, "Wizard question %d" % (uwizard.kInflorDraw_Shape), "inflorShapeRaceme")
        self.options.wizardChoices[uwizard.kInflorDraw_Thickness] = self.stringForSectionAndKey(section, "Wizard question %d" % (uwizard.kInflorDraw_Thickness), "inflorWidthThin")
        # flowers
        self.options.wizardChoices[uwizard.kFlowers_NumPetals] = self.stringForSectionAndKey(section, "Wizard question %d" % (uwizard.kFlowers_NumPetals), "petalsFive")
        self.options.wizardChoices[uwizard.kFlowers_Scale] = self.stringForSectionAndKey(section, "Wizard question %d" % (uwizard.kFlowers_Scale), "petalScaleSmall")
        self.options.wizardColors[1] = int(self.stringForSectionAndKey(section, "Wizard colors 1", "%d" % (delphi_compatability.clFuchsia)))
        # fruit
        self.options.wizardChoices[uwizard.kFruit_NumSections] = self.stringForSectionAndKey(section, "Wizard question %d" % (uwizard.kFruit_NumSections), "fruitSectionsFive")
        self.options.wizardChoices[uwizard.kFruit_Scale] = self.stringForSectionAndKey(section, "Wizard question %d" % (uwizard.kFruit_Scale), "fruitScaleSmall")
        self.options.wizardColors[2] = int(self.stringForSectionAndKey(section, "Wizard colors 2", "%d" % (delphi_compatability.clRed)))
        for i in range(1, kMaxWizardTdos + 1):
            # the wizard will default the tdo names when it comes up, we don't have to do it here
            self.options.wizardTdoNames[i] = self.stringForSectionAndKey(section, "Wizard 3D objects %d" % (i), "")
        self.options.wizardShowFruit = usupport.strToBool(self.stringForSectionAndKey(section, "Wizard show fruit", "False"))
        """
        # ------------------------------------------- custom colors
        section = iniSections[kCustomColors]
        for i in range(0, kMaxCustomColors):
            self.options.customColors[i] = int(self.stringForSectionAndKey(section, "Custom color %d" % (i + 1), "0"))
        # with options
        # -------------------------------------------  export (2D)
        section = iniSections[kSectionExport]
        self.bitmapOptions.exportType = int(self.stringForSectionAndKey(section, "Which plants to draw (selected/visible/all/drawing)", "%d" % (kIncludeSelectedPlants)))
        ### PDF PORT TEMPORARILY COMMENT OUT: self.bitmapOptions.colorType = UNRESOLVED.TPixelFormat(int(self.stringForSectionAndKey(section, "Colors (screen/2/16/256/15-bit/16-bit/24-bit/32-bit)", "6")))
        self.bitmapOptions.resolution_pixelsPerInch = int(self.stringForSectionAndKey(section, "Resolution (pixels per inch)", "%d" % (kDefaultResolution)))
        self.bitmapOptions.width_pixels = int(self.stringForSectionAndKey(section, "Picture width (pixels)", "400"))
        self.bitmapOptions.height_pixels = int(self.stringForSectionAndKey(section, "Picture height (pixels)", "400"))
        self.bitmapOptions.width_in = usupport.strToFloatWithCommaCheck(self.stringForSectionAndKey(section, "Picture width (inches)", "2.0"))
        self.bitmapOptions.height_in = usupport.strToFloatWithCommaCheck(self.stringForSectionAndKey(section, "Picture height (inches)", "2.0"))
        self.bitmapOptions.preserveAspectRatio = usupport.strToBool(self.stringForSectionAndKey(section, "Preserve aspect ratio", "True"))
        self.bitmapOptions.jpegCompressionRatio = int(self.stringForSectionAndKey(section, "JPEG compression quality ratio (1-100)", "50"))
        # -------------------------------------------  printing
        section = iniSections[kSectionPrinting]
        self.bitmapOptions.printPreserveAspectRatio = usupport.strToBool(self.stringForSectionAndKey(section, "Preserve aspect ratio", "True"))
        self.bitmapOptions.printWidth_in = usupport.strToFloatWithCommaCheck(self.stringForSectionAndKey(section, "Print width (inches)", "4.0"))
        self.bitmapOptions.printHeight_in = usupport.strToFloatWithCommaCheck(self.stringForSectionAndKey(section, "Print height (inches)", "4.0"))
        self.bitmapOptions.printLeftMargin_in = usupport.strToFloatWithCommaCheck(self.stringForSectionAndKey(section, "Print left margin (inches)", "1.0"))
        self.bitmapOptions.printTopMargin_in = usupport.strToFloatWithCommaCheck(self.stringForSectionAndKey(section, "Print top margin (inches)", "1.0"))
        self.bitmapOptions.printRightMargin_in = usupport.strToFloatWithCommaCheck(self.stringForSectionAndKey(section, "Print right margin (inches)", "1.0"))
        self.bitmapOptions.printBottomMargin_in = usupport.strToFloatWithCommaCheck(self.stringForSectionAndKey(section, "Print bottom margin (inches)", "1.0"))
        self.bitmapOptions.printBorderInner = usupport.strToBool(self.stringForSectionAndKey(section, "Print inner border", "False"))
        self.bitmapOptions.printBorderOuter = usupport.strToBool(self.stringForSectionAndKey(section, "Print outer border", "False"))
        self.bitmapOptions.printBorderWidthInner = int(self.stringForSectionAndKey(section, "Inner border width (pixels)", "1"))
        self.bitmapOptions.printBorderWidthOuter = int(self.stringForSectionAndKey(section, "Outer border width (pixels)", "1"))
        self.bitmapOptions.printBorderColorInner = int(self.stringForSectionAndKey(section, "Inner border color", "0"))
        self.bitmapOptions.printBorderColorOuter = int(self.stringForSectionAndKey(section, "Outer border color", "0"))
        # -------------------------------------------  breeding
        section = iniSections[kSectionBreeding]
        self.breedingAndTimeSeriesOptions.plantsPerGeneration = int(self.stringForSectionAndKey(section, "Plants per generation", "5"))
        self.breedingAndTimeSeriesOptions.percentMaxAge = int(self.stringForSectionAndKey(section, "Percent max age", "100"))
        self.breedingAndTimeSeriesOptions.variationType = int(self.stringForSectionAndKey(section, "Variation (low/med/high/custom/none)", "1"))
        self.breedingAndTimeSeriesOptions.thumbnailWidth = int(self.stringForSectionAndKey(section, "Thumbnail width", "40"))
        self.breedingAndTimeSeriesOptions.thumbnailHeight = int(self.stringForSectionAndKey(section, "Thumbnail height", "80"))
        self.breedingAndTimeSeriesOptions.maxGenerations = int(self.stringForSectionAndKey(section, "Max generations", "30"))
        self.breedingAndTimeSeriesOptions.numTimeSeriesStages = int(self.stringForSectionAndKey(section, "Time series stages", "5"))
        for i in range(0, uplant.kMaxBreedingSections):
            self.breedingAndTimeSeriesOptions.mutationStrengths[i] = int(self.stringForSectionAndKey(section, "Mutation %d" % (i + 1), "%d" % (kMediumMutation)))
        for i in range(0, uplant.kMaxBreedingSections):
            self.breedingAndTimeSeriesOptions.firstPlantWeights[i] = int(self.stringForSectionAndKey(section, "First plant weight %d" % (i + 1), "50"))
        self.breedingAndTimeSeriesOptions.getNonNumericalParametersFrom = int(self.stringForSectionAndKey(section, "Non-numeric", "5"))
        self.breedingAndTimeSeriesOptions.mutateAndBlendColorValues = usupport.strToBool(self.stringForSectionAndKey(section, "Vary colors", "False"))
        self.breedingAndTimeSeriesOptions.chooseTdosRandomlyFromCurrentLibrary = usupport.strToBool(self.stringForSectionAndKey(section, "Vary 3D objects", "False"))
        # -------------------------------------------  nozzles
        section = iniSections[kSectionNozzle]
        self.nozzleOptions.exportType = int(self.stringForSectionAndKey(section, "Which plants to make nozzle from (selected/visible/all)", "0"))
        self.nozzleOptions.resolution_pixelsPerInch = int(self.stringForSectionAndKey(section, "Nozzle resolution", "%d" % (kDefaultResolution)))
        ### PDF PORT TEMPORARILY COMMENTED OUT: self.nozzleOptions.colorType = UNRESOLVED.TPixelFormat(int(self.stringForSectionAndKey(section, "Nozzle colors (screen/2/16/256/15-bit/16-bit/24-bit/32-bit)", "6")))
        self.nozzleOptions.backgroundColor = int(self.stringForSectionAndKey(section, "Nozzle background color", "%d" % (delphi_compatability.clWhite)))
        # -------------------------------------------  animations
        section = iniSections[kSectionAnimation]
        self.animationOptions.animateBy = int(self.stringForSectionAndKey(section, "Animate by (x rotation/age)", "0"))
        self.animationOptions.xRotationIncrement = int(self.stringForSectionAndKey(section, "X rotation increment", "10"))
        self.animationOptions.ageIncrement = int(self.stringForSectionAndKey(section, "Age increment", "5"))
        self.animationOptions.resolution_pixelsPerInch = int(self.stringForSectionAndKey(section, "Resolution", "%d" % (kDefaultResolution)))
        # 24 bit
        ### PODF PORT __ REMPORARILY COMMENT OUT: self.animationOptions.colorType = UNRESOLVED.TPixelFormat(int(self.stringForSectionAndKey(section, "Animation colors (screen/2/16/256/15-bit/16-bit/24-bit/32-bit)", "6")))
        # -------------------------------------------  registration
        # PDF PORT -- NO LOGNER USING
        """
        section = iniSections[kSectionRegistration]
        self.registrationName = self.stringForSectionAndKey(section, "R4", "")
        self.registrationName = usupport.hexUnencode(self.registrationName)
        self.registrationCode = self.stringForSectionAndKey(section, "R2", "")
        self.registrationCode = usupport.hexUnencode(self.registrationCode)
        self.registered = uregistersupport.RegistrationMatch(self.registrationName, self.registrationCode)
        if not self.registered:
            section = iniSections[kSectionPrefs]
            timeString = self.stringForSectionAndKey(section, kKeyForAccumulatedUnregisteredTime, "0")
            readNumber = max(usupport.strToFloatWithCommaCheck(timeString), 0)
            self.accumulatedUnregisteredTime = readNumber / kEncryptingMultiplierForAccumulatedUnregisteredTime
            section = iniSections[kSectionBreeding]
            readInt = int(self.stringForSectionAndKey(section, kKeyForUnregisteredExportCount, "0"))
            self.unregisteredExportCountBeforeThisSession = readInt / kEncryptingMultiplierForUnregisteredExportCount
            self.unregisteredExportCountThisSession = 0
        """
        # -------------------------------------------  parameter overrides
        section = iniSections[kSectionOverrides]
        overrideKeys = ucollect.TListCollection()
        overrideValues = ucollect.TListCollection
        self.readSectionKeysOrValues(section, overrideKeys, kGetKeys)
        self.readSectionKeysOrValues(section, overrideValues, kGetValues)
        for i in range(0, len(overrideKeys)):
            key = overrideKeys.Strings[i]
            # v2.1 changed to require section and param name for overrides
            sectionName = usupport.stringUpTo(key, ":").strip()
            paramName = usupport.stringBeyond(key, ":").strip()
            value = overrideValues.Strings[i]
            value = usupport.stringBeyond(value, "=")
            param = None
            param = self.sectionManager.parameterForSectionAndName(sectionName, paramName)
            if (param == None) or (param.cannotOverride):
                continue
            stream = usstream.KfStringStream()
            stream.onStringSeparator(value, " ")
            try:
                param.lowerBoundOverride = usupport.strToFloatWithCommaCheck(stream.nextToken())
                param.upperBoundOverride = usupport.strToFloatWithCommaCheck(stream.nextToken())
                param.defaultValueStringOverride = usupport.stringBetween("(", ")", stream.remainder)
                param.isOverridden = True
            except:
                param.isOverridden = False
        self.boundProfileInformation()

    def storeProfileInformation(self):
        i = 0
        j = 0
        section = ""
        typeName = ""
        saveNumber = 0.0
        saveInt = 0
        param = PdParameter()

        try:
            # v1.5
            usupport.setDecimalSeparator()
            if self.gotInfoFromV1IniFile:
                # remove two sections gotten rid of in v2
                self.removeSectionFromIniLines("Breeder")
                self.removeSectionFromIniLines("Time series")
            # files
            section = iniSections[kSectionFiles]
            if UNRESOLVED.pos(kUnsavedFileName.upper(), self.lastOpenedPlantFileName).upper() == 0:
                self.setStringForSectionAndKey(section, "Recent", self.lastOpenedPlantFileName)
            else:
                self.setStringForSectionAndKey(section, "Recent", "")
            self.setStringForSectionAndKey(section, "3D object library", self.defaultTdoLibraryFileName)
            # recent files
            section = iniSections[kSectionOtherRecentFiles]
            for i in range(0, kMaxRecentFiles):
                if self.options.recentFiles[i] != "":
                    self.setStringForSectionAndKey(section, "File%d" % (i + 1), self.options.recentFiles[i])
            # preferences
            section = iniSections[kSectionPrefs]
            self.setStringForSectionAndKey(section, "Hide welcome window", usupport.boolToStr(self.options.hideWelcomeForm))
            self.setStringForSectionAndKey(section, "Open most recent file at start", usupport.boolToStr(self.options.openMostRecentFileAtStart))
            self.setStringForSectionAndKey(section, "Ignore window settings saved in files", usupport.boolToStr(self.options.ignoreWindowSettingsInFile))
            self.setStringForSectionAndKey(section, "Draw plants into separate bitmaps", usupport.boolToStr(self.options.cachePlantBitmaps))
            self.setStringForSectionAndKey(section, "Memory limit for plant bitmaps (in MB)", "%d" % (self.options.memoryLimitForPlantBitmaps_MB))
            self.setStringForSectionAndKey(section, "Max parts per plant (in thousands)", "%d" % (self.options.maxPartsPerPlant_thousands))
            self.setStringForSectionAndKey(section, "Background color", "%d" % (self.options.backgroundColor))
            self.setStringForSectionAndKey(section, "Transparent color", "%d" % (self.options.transparentColor))
            self.setStringForSectionAndKey(section, "Show selection rectangle", usupport.boolToStr(self.options.showSelectionRectangle))
            self.setStringForSectionAndKey(section, "Show bounding rectangle", usupport.boolToStr(self.options.showBoundsRectangle))
            self.setStringForSectionAndKey(section, "Resizing rectangle size", "%d" % (self.options.resizeRectSize))
            self.setStringForSectionAndKey(section, "Paste rectangle size", "%d" % (self.options.pasteRectSize))
            self.setStringForSectionAndKey(section, "First selection rectangle color", "%d" % (self.options.firstSelectionRectangleColor))
            self.setStringForSectionAndKey(section, "Multi selection rectangle color", "%d" % (self.options.multiSelectionRectangleColor))
            self.setStringForSectionAndKey(section, "Draw 3D objects", usupport.boolToStr(self.options.draw3DObjects))
            self.setStringForSectionAndKey(section, "Draw stems", usupport.boolToStr(self.options.drawStems))
            self.setStringForSectionAndKey(section, "Fill polygons", usupport.boolToStr(self.options.fillPolygons))
            self.setStringForSectionAndKey(section, "Draw speed (boxes/frames/solids)", "%d" % (self.options.drawSpeed))
            self.setStringForSectionAndKey(section, "Draw lines between polygons", usupport.boolToStr(self.options.drawLinesBetweenPolygons))
            self.setStringForSectionAndKey(section, "Sort polygons", usupport.boolToStr(self.options.sortPolygons))
            self.setStringForSectionAndKey(section, "Draw 3D objects as squares", usupport.boolToStr(self.options.draw3DObjectsAsBoundingRectsOnly))
            self.setStringForSectionAndKey(section, "Show drawing progress", usupport.boolToStr(self.options.showPlantDrawingProgress))
            self.setStringForSectionAndKey(section, "Use metric units", usupport.boolToStr(self.options.useMetricUnits))
            self.setStringForSectionAndKey(section, "Actions to keep in undo list", "%d" % (self.options.undoLimit))
            self.setStringForSectionAndKey(section, "Plants to keep in undo list", "%d" % (self.options.undoLimitOfPlants))
            self.setStringForSectionAndKey(section, "Rotation button increment", "%d" % (self.options.rotationIncrement))
            self.setStringForSectionAndKey(section, "Show long hints for buttons", usupport.boolToStr(self.options.showLongHintsForButtons))
            self.setStringForSectionAndKey(section, "Show hints for parameters", usupport.boolToStr(self.options.showHintsForParameters))
            self.setStringForSectionAndKey(section, "Pause before hint", "%d" % (self.options.pauseBeforeHint))
            self.setStringForSectionAndKey(section, "Pause during hint", "%d" % (self.options.pauseDuringHint))
            self.setStringForSectionAndKey(section, "Wrap lines in note editor", usupport.boolToStr(self.options.noteEditorWrapLines))
            if self.justRegistered:
                # registration, embedded here to hide time scale fraction
                section = iniSections[kSectionRegistration]
                self.setStringForSectionAndKey(section, "R1", "RQBBBOYUMMBIHYMBB")
                self.setStringForSectionAndKey(section, "R2", usupport.hexEncode(self.registrationCode))
                self.setStringForSectionAndKey(section, "R3", "YWEHZBBIUWOPBCDVXBQB")
                self.setStringForSectionAndKey(section, "R4", usupport.hexEncode(self.registrationName))
            elif not self.registered:
                section = iniSections[kSectionPrefs]
                self.accumulatedUnregisteredTime = self.accumulatedUnregisteredTime + max((UNRESOLVED.now - self.startTimeThisSession), 0)
                saveNumber = self.accumulatedUnregisteredTime * kEncryptingMultiplierForAccumulatedUnregisteredTime
                self.setStringForSectionAndKey(section, kKeyForAccumulatedUnregisteredTime, "%f" % (saveNumber))
                # hide this elsewhere
                section = iniSections[kSectionBreeding]
                saveInt = (self.unregisteredExportCountBeforeThisSession + self.unregisteredExportCountThisSession) * kEncryptingMultiplierForUnregisteredExportCount
                self.setStringForSectionAndKey(section, kKeyForUnregisteredExportCount, "%d" % (saveInt))
            section = iniSections[kSectionPrefs]
            self.setStringForSectionAndKey(section, "Update time series plants on parameter change", usupport.boolToStr(self.options.updateTimeSeriesPlantsOnParameterChange))
            self.setStringForSectionAndKey(section, "Main window view option (all/one)", "%d" % (self.options.mainWindowViewMode))
            self.setStringForSectionAndKey(section, "Distance plant moves with Control-arrow key", "%d" % (self.options.nudgeDistance))
            self.setStringForSectionAndKey(section, "Percent size increase with Control-Shift-up-arrow key", "%d" % (self.options.resizeKeyUpMultiplierPercent))
            self.setStringForSectionAndKey(section, "Parameter panels font size", "%d" % (self.options.parametersFontSize))
            self.setStringForSectionAndKey(section, "Main window orientation (horiz/vert)", "%d" % (self.options.mainWindowOrientation))
            self.setStringForSectionAndKey(section, "Contrast index for lines on polygons", "%d" % (self.options.lineContrastIndex))
            self.setStringForSectionAndKey(section, "Sort 3D objects as one item", usupport.boolToStr(self.options.sortTdosAsOneItem))
            self.setStringForSectionAndKey(section, "3D object editor point size", "%d" % (self.options.circlePointSizeInTdoEditor))
            self.setStringForSectionAndKey(section, "3D object editor parts", "%d" % (self.options.partsInTdoEditor))
            self.setStringForSectionAndKey(section, "3D object editor fill triangles", usupport.boolToStr(self.options.fillTrianglesInTdoEditor))
            self.setStringForSectionAndKey(section, "3D object editor draw lines", usupport.boolToStr(self.options.drawLinesInTdoEditor))
            self.setStringForSectionAndKey(section, "Show numerical exceptions window on exception", usupport.boolToStr(self.options.showWindowOnException))
            self.setStringForSectionAndKey(section, "Log to file on exception", usupport.boolToStr(self.options.logToFileOnException))
            self.setStringForSectionAndKey(section, "Ghost hidden parts", usupport.boolToStr(self.options.showGhostingForHiddenParts))
            self.setStringForSectionAndKey(section, "Highlight posed parts", usupport.boolToStr(self.options.showHighlightingForNonHiddenPosedParts))
            self.setStringForSectionAndKey(section, "Show posing", usupport.boolToStr(self.options.showPosingAtAll))
            self.setStringForSectionAndKey(section, "Ghosting color", "%d" % (self.options.ghostingColor))
            self.setStringForSectionAndKey(section, "Posed color", "%d" % (self.options.nonHiddenPosedColor))
            self.setStringForSectionAndKey(section, "Posed selected color", "%d" % (self.options.selectedPosedColor))
            # settings
            section = iniSections[kSectionSettings]
            self.setStringForSectionAndKey(section, "Window position", usupport.rectToString(self.mainWindowRect))
            self.setStringForSectionAndKey(section, "Horizontal split", "%d" % (self.horizontalSplitterPos))
            self.setStringForSectionAndKey(section, "Vertical split", "%d" % (self.verticalSplitterPos))
            self.setStringForSectionAndKey(section, "Numerical exceptions window position", usupport.rectToString(self.debugWindowRect))
            self.setStringForSectionAndKey(section, "Undo/redo list window position", usupport.rectToString(self.undoRedoListWindowRect))
            self.setStringForSectionAndKey(section, "3D object editor window position", usupport.rectToString(self.tdoEditorWindowRect))
            self.setStringForSectionAndKey(section, "Breeder position", usupport.rectToString(self.breederWindowRect))
            self.setStringForSectionAndKey(section, "Time series position", usupport.rectToString(self.timeSeriesWindowRect))
            for i in range(1, u3dexport.k3DExportTypeLast + 1):
                # 3d export options
                section = iniSections[self.sectionNumberFor3DExportType(i)]
                typeName = u3dexport.nameFor3DExportType(i)
                # options in common for all
                self.setStringForSectionAndKey(section, typeName + " which plants to draw (selected/visible/all)", "%d" % (self.exportOptionsFor3D[i].exportType))
                self.setStringForSectionAndKey(section, typeName + " layering option (all/by type/by part)", "%d" % (self.exportOptionsFor3D[i].layeringOption))
                self.setStringForSectionAndKey(section, typeName + " stem cylinder sides", "%d" % (self.exportOptionsFor3D[i].stemCylinderFaces))
                self.setStringForSectionAndKey(section, typeName + " translate plants to match window positions", usupport.boolToStr(self.exportOptionsFor3D[i].translatePlantsToWindowPositions))
                self.setStringForSectionAndKey(section, typeName + " length of plant name", "%d" % (self.exportOptionsFor3D[i].lengthOfShortName))
                self.setStringForSectionAndKey(section, typeName + " write plant number in front of name", usupport.boolToStr(self.exportOptionsFor3D[i].writePlantNumberInFrontOfName))
                self.setStringForSectionAndKey(section, typeName + " write colors", usupport.boolToStr(self.exportOptionsFor3D[i].writeColors))
                self.setStringForSectionAndKey(section, typeName + " X rotation before drawing", "%d" % (self.exportOptionsFor3D[i].xRotationBeforeDraw))
                self.setStringForSectionAndKey(section, typeName + " scaling factor (percent)", "%d" % (self.exportOptionsFor3D[i].overallScalingFactor_pct))
                self.setStringForSectionAndKey(section, typeName + " press plants", usupport.boolToStr(self.exportOptionsFor3D[i].pressPlants))
                self.setStringForSectionAndKey(section, typeName + " press dimension (x/y/z)", "%d" % (self.exportOptionsFor3D[i].directionToPressPlants))
                self.setStringForSectionAndKey(section, typeName + " double sided", usupport.boolToStr(self.exportOptionsFor3D[i].makeTrianglesDoubleSided))
                if i == u3dexport.kDXF:
                    # special options
                    self.setStringForSectionAndKey(section, "DXF colors option (by type/by part/all)", "%d" % (self.exportOptionsFor3D[i].dxf_whereToGetColors))
                    self.setStringForSectionAndKey(section, "DXF whole plant color index", "%d" % (self.exportOptionsFor3D[i].dxf_wholePlantColorIndex))
                    for j in range(0, u3dexport.kExportPartLast + 1):
                        self.setStringForSectionAndKey(section, "DXF color indexes %d" % (j + 1), "%d" % (self.exportOptionsFor3D[i].dxf_plantPartColorIndexes[j]))
                elif i == u3dexport.kPOV:
                    self.setStringForSectionAndKey(section, "POV minimum line length to write (mm)", usupport.digitValueString(self.exportOptionsFor3D[i].pov_minLineLengthToWrite))
                    self.setStringForSectionAndKey(section, "POV minimum 3D object scale to write", usupport.digitValueString(self.exportOptionsFor3D[i].pov_minTdoScaleToWrite))
                    self.setStringForSectionAndKey(section, "POV comment out union of plants at end", usupport.boolToStr(self.exportOptionsFor3D[i].pov_commentOutUnionAtEnd))
                elif i == u3dexport.kVRML:
                    self.setStringForSectionAndKey(section, "VRML version", "%d" % (self.exportOptionsFor3D[i].vrml_version))
                if (i == u3dexport.kPOV) or (i == u3dexport.kVRML):
                    self.setStringForSectionAndKey(section, typeName + " nest leaves with petioles", usupport.boolToStr(self.exportOptionsFor3D[i].nest_LeafAndPetiole))
                    self.setStringForSectionAndKey(section, typeName + " compound leaves", usupport.boolToStr(self.exportOptionsFor3D[i].nest_CompoundLeaf))
                    self.setStringForSectionAndKey(section, typeName + " nest inflorescences", usupport.boolToStr(self.exportOptionsFor3D[i].nest_Inflorescence))
                    self.setStringForSectionAndKey(section, typeName + " nest flowers/fruits with pedicels", usupport.boolToStr(self.exportOptionsFor3D[i].nest_PedicelAndFlowerFruit))
                    self.setStringForSectionAndKey(section, typeName + " nest pistils and stamens", usupport.boolToStr(self.exportOptionsFor3D[i].nest_FloralLayers))
            # wizard
            section = iniSections[kSectionWizard]
            for i in range(1, kMaxWizardQuestions + 1):
                self.setStringForSectionAndKey(section, "Wizard question %d" % (i), self.options.wizardChoices[i])
            for i in range(1, kMaxWizardColors + 1):
                self.setStringForSectionAndKey(section, "Wizard colors %d" % (i), "%d" % (self.options.wizardColors[i]))
            for i in range(1, kMaxWizardTdos + 1):
                self.setStringForSectionAndKey(section, "Wizard 3D objects %d" % (i), self.options.wizardTdoNames[i])
            self.setStringForSectionAndKey(section, "Wizard show fruit", usupport.boolToStr(self.options.wizardShowFruit))
            # custom colors
            section = iniSections[kCustomColors]
            for i in range(0, kMaxCustomColors):
                self.setStringForSectionAndKey(section, "Custom color %d" % (i + 1), "%d" % (self.options.customColors[i]))
            # export
            section = iniSections[kSectionExport]
            self.setStringForSectionAndKey(section, "Which plants to draw (selected/visible/all/drawing)", "%d" % (self.bitmapOptions.exportType))
            self.setStringForSectionAndKey(section, "Colors (screen/2/16/256/15-bit/16-bit/24-bit/32-bit)", "%d" % (ord(self.bitmapOptions.colorType)))
            self.setStringForSectionAndKey(section, "Resolution (pixels per inch)", "%d" % (self.bitmapOptions.resolution_pixelsPerInch))
            self.setStringForSectionAndKey(section, "Picture width (pixels)", "%d" % (self.bitmapOptions.width_pixels))
            self.setStringForSectionAndKey(section, "Picture height (pixels)", "%d" % (self.bitmapOptions.height_pixels))
            self.setStringForSectionAndKey(section, "Picture width (inches)", usupport.digitValueString(self.bitmapOptions.width_in))
            self.setStringForSectionAndKey(section, "Picture height (inches)", usupport.digitValueString(self.bitmapOptions.height_in))
            self.setStringForSectionAndKey(section, "Preserve aspect ratio", usupport.boolToStr(self.bitmapOptions.preserveAspectRatio))
            self.setStringForSectionAndKey(section, "JPEG compression quality ratio (1-100)", "%d" % (self.bitmapOptions.jpegCompressionRatio))
            # printing
            section = iniSections[kSectionPrinting]
            self.setStringForSectionAndKey(section, "Preserve aspect ratio", usupport.boolToStr(self.bitmapOptions.printPreserveAspectRatio))
            self.setStringForSectionAndKey(section, "Print width (inches)", usupport.digitValueString(self.bitmapOptions.printWidth_in))
            self.setStringForSectionAndKey(section, "Print height (inches)", usupport.digitValueString(self.bitmapOptions.printHeight_in))
            self.setStringForSectionAndKey(section, "Print left margin (inches)", usupport.digitValueString(self.bitmapOptions.printLeftMargin_in))
            self.setStringForSectionAndKey(section, "Print top margin (inches)", usupport.digitValueString(self.bitmapOptions.printTopMargin_in))
            self.setStringForSectionAndKey(section, "Print right margin (inches)", usupport.digitValueString(self.bitmapOptions.printRightMargin_in))
            self.setStringForSectionAndKey(section, "Print bottom margin (inches)", usupport.digitValueString(self.bitmapOptions.printBottomMargin_in))
            self.setStringForSectionAndKey(section, "Print inner border", usupport.boolToStr(self.bitmapOptions.printBorderInner))
            self.setStringForSectionAndKey(section, "Print outer border", usupport.boolToStr(self.bitmapOptions.printBorderOuter))
            self.setStringForSectionAndKey(section, "Inner border width (pixels)", "%d" % (self.bitmapOptions.printBorderWidthInner))
            self.setStringForSectionAndKey(section, "Outer border width (pixels)", "%d" % (self.bitmapOptions.printBorderWidthOuter))
            self.setStringForSectionAndKey(section, "Inner border color", "%d" % (self.bitmapOptions.printBorderColorInner))
            self.setStringForSectionAndKey(section, "Outer border color", "%d" % (self.bitmapOptions.printBorderColorOuter))
            section = iniSections[kSectionBreeding]
            self.setStringForSectionAndKey(section, "Plants per generation", "%d" % (self.breedingAndTimeSeriesOptions.plantsPerGeneration))
            self.setStringForSectionAndKey(section, "Variation (low/med/high/custom/none)", "%d" % (self.breedingAndTimeSeriesOptions.variationType))
            self.setStringForSectionAndKey(section, "Percent max age", "%d" % (self.breedingAndTimeSeriesOptions.percentMaxAge))
            self.setStringForSectionAndKey(section, "Thumbnail width", "%d" % (self.breedingAndTimeSeriesOptions.thumbnailWidth))
            self.setStringForSectionAndKey(section, "Thumbnail height", "%d" % (self.breedingAndTimeSeriesOptions.thumbnailHeight))
            self.setStringForSectionAndKey(section, "Max generations", "%d" % (self.breedingAndTimeSeriesOptions.maxGenerations))
            self.setStringForSectionAndKey(section, "Time series stages", "%d" % (self.breedingAndTimeSeriesOptions.numTimeSeriesStages))
            for i in range(0, uplant.kMaxBreedingSections):
                self.setStringForSectionAndKey(section, "Mutation %d" % (i + 1), "%d" % (self.breedingAndTimeSeriesOptions.mutationStrengths[i]))
            for i in range(0, uplant.kMaxBreedingSections):
                self.setStringForSectionAndKey(section, "First plant weight %d" % (i + 1), "%d" % (self.breedingAndTimeSeriesOptions.firstPlantWeights[i]))
            self.setStringForSectionAndKey(section, "Non-numeric", "%d" % (self.breedingAndTimeSeriesOptions.getNonNumericalParametersFrom))
            self.setStringForSectionAndKey(section, "Vary colors", usupport.boolToStr(self.breedingAndTimeSeriesOptions.mutateAndBlendColorValues))
            self.setStringForSectionAndKey(section, "Vary 3D objects", usupport.boolToStr(self.breedingAndTimeSeriesOptions.chooseTdosRandomlyFromCurrentLibrary))
            section = iniSections[kSectionNozzle]
            self.setStringForSectionAndKey(section, "Which plants to make nozzle from (selected/visible/all)", "%d" % (self.nozzleOptions.exportType))
            self.setStringForSectionAndKey(section, "Nozzle resolution", "%d" % (self.nozzleOptions.resolution_pixelsPerInch))
            self.setStringForSectionAndKey(section, "Nozzle colors (screen/2/16/256/15-bit/16-bit/24-bit/32-bit)", "%d" % (ord(self.nozzleOptions.colorType)))
            self.setStringForSectionAndKey(section, "Nozzle background color", "%d" % (self.nozzleOptions.backgroundColor))
            section = iniSections[kSectionAnimation]
            self.setStringForSectionAndKey(section, "Animate by (x rotation/age)", "%d" % (self.animationOptions.animateBy))
            self.setStringForSectionAndKey(section, "X rotation increment", "%d" % (self.animationOptions.xRotationIncrement))
            self.setStringForSectionAndKey(section, "Age increment", "%d" % (self.animationOptions.ageIncrement))
            self.setStringForSectionAndKey(section, "Resolution", "%d" % (self.animationOptions.resolution_pixelsPerInch))
            self.setStringForSectionAndKey(section, "Animation colors (screen/2/16/256/15-bit/16-bit/24-bit/32-bit)", "%d" % (ord(self.animationOptions.colorType)))
            # write parameter overrides
            section = iniSections[kSectionOverrides]
            for param in self.parameterManager.parameters:
                if (not param.cannotOverride) and (param.isOverridden):
                    # v2.1 added section name to override key
                    self.setStringForSectionAndKey(section, param.originalSectionName + ": " + param.name, usupport.digitValueString(param.lowerBoundOverride) + " " + usupport.digitValueString(param.upperBoundOverride) + " " + "(" + param.defaultValueStringOverride + ")")
            self.iniLines.SaveToFile(self.iniFileName)
        finally:
            usupport.iniFileChanged = False

    def boundProfileInformation(self):
        self.options.resizeRectSize = max(2, min(20, self.options.resizeRectSize))
        self.options.pasteRectSize = max(50, min(500, self.options.pasteRectSize))
        self.options.memoryLimitForPlantBitmaps_MB = max(1, min(200, self.options.memoryLimitForPlantBitmaps_MB))
        self.options.maxPartsPerPlant_thousands = max(1, min(100, self.options.maxPartsPerPlant_thousands))
        self.horizontalSplitterPos = max(50, self.horizontalSplitterPos)
        self.verticalSplitterPos = max(30, self.verticalSplitterPos)
        self.options.nudgeDistance = max(1, min(100, self.options.nudgeDistance))
        self.options.resizeKeyUpMultiplierPercent = max(100, min(200, self.options.resizeKeyUpMultiplierPercent))
        self.options.parametersFontSize = max(6, min(20, self.options.parametersFontSize))
        self.options.mainWindowOrientation = max(0, min(kMaxMainWindowOrientations, self.options.mainWindowOrientation))
        self.options.undoLimit = max(0, min(1000, self.options.undoLimit))
        self.options.undoLimitOfPlants = max(0, min(500, self.options.undoLimitOfPlants))
        self.options.circlePointSizeInTdoEditor = max(1, min(30, self.options.circlePointSizeInTdoEditor))
        self.options.partsInTdoEditor = max(1, min(30, self.options.partsInTdoEditor))
        self.options.lineContrastIndex = max(0, min(10, self.options.lineContrastIndex))
        self.options.drawSpeed = max(0, min(kDrawCustom, self.options.drawSpeed))
        self.bitmapOptions.exportType = max(0, min(kMaxIncludeOption, self.bitmapOptions.exportType))
        ### PDF PORT TEMP COMMENT OUT: self.bitmapOptions.colorType = UNRESOLVED.TPixelFormat(max(0, min(kMaxColorOption, ord(self.bitmapOptions.colorType))))
        self.bitmapOptions.resolution_pixelsPerInch = max(kMinResolution, min(kMaxResolution, self.bitmapOptions.resolution_pixelsPerInch))
        self.bitmapOptions.width_pixels = max(kMinPixels, min(kMaxPixels, self.bitmapOptions.width_pixels))
        self.bitmapOptions.height_pixels = max(kMinPixels, min(kMaxPixels, self.bitmapOptions.height_pixels))
        self.bitmapOptions.width_in = max(kMinInches, min(kMaxInches, self.bitmapOptions.width_in))
        self.bitmapOptions.height_in = max(kMinInches, min(kMaxInches, self.bitmapOptions.height_in))
        self.bitmapOptions.printWidth_in = max(kMinInches, min(kMaxInches, self.bitmapOptions.printWidth_in))
        self.bitmapOptions.printHeight_in = max(kMinInches, min(kMaxInches, self.bitmapOptions.printHeight_in))
        self.bitmapOptions.printLeftMargin_in = max(kMinInches, min(kMaxInches, self.bitmapOptions.printLeftMargin_in))
        self.bitmapOptions.printTopMargin_in = max(kMinInches, min(kMaxInches, self.bitmapOptions.printTopMargin_in))
        self.bitmapOptions.printRightMargin_in = max(kMinInches, min(kMaxInches, self.bitmapOptions.printRightMargin_in))
        self.bitmapOptions.printBottomMargin_in = max(kMinInches, min(kMaxInches, self.bitmapOptions.printBottomMargin_in))
        self.bitmapOptions.printBorderWidthInner = max(0, min(1000, self.bitmapOptions.printBorderWidthInner))
        self.bitmapOptions.printBorderWidthOuter = max(0, min(1000, self.bitmapOptions.printBorderWidthOuter))
        self.breedingAndTimeSeriesOptions.plantsPerGeneration = max(1, min(100, self.breedingAndTimeSeriesOptions.plantsPerGeneration))
        self.breedingAndTimeSeriesOptions.variationType = max(0, min(4, self.breedingAndTimeSeriesOptions.variationType))
        self.breedingAndTimeSeriesOptions.percentMaxAge = max(1, min(100, self.breedingAndTimeSeriesOptions.percentMaxAge))
        self.breedingAndTimeSeriesOptions.thumbnailWidth = min(200, max(30, self.breedingAndTimeSeriesOptions.thumbnailWidth))
        self.breedingAndTimeSeriesOptions.thumbnailHeight = min(200, max(30, self.breedingAndTimeSeriesOptions.thumbnailHeight))
        self.breedingAndTimeSeriesOptions.maxGenerations = max(20, min(500, self.breedingAndTimeSeriesOptions.maxGenerations))
        self.breedingAndTimeSeriesOptions.numTimeSeriesStages = max(1, min(100, self.breedingAndTimeSeriesOptions.numTimeSeriesStages))
        for i in range(0, uplant.kMaxBreedingSections):
            self.breedingAndTimeSeriesOptions.mutationStrengths[i] = max(0, min(100, self.breedingAndTimeSeriesOptions.mutationStrengths[i]))
        for i in range(0, uplant.kMaxBreedingSections):
            self.breedingAndTimeSeriesOptions.firstPlantWeights[i] = max(0, min(100, self.breedingAndTimeSeriesOptions.firstPlantWeights[i]))
        self.breedingAndTimeSeriesOptions.getNonNumericalParametersFrom = max(0, min(5, self.breedingAndTimeSeriesOptions.getNonNumericalParametersFrom))
        self.nozzleOptions.exportType = max(0, min(kIncludeAllPlants, self.nozzleOptions.exportType))
        self.nozzleOptions.resolution_pixelsPerInch = max(kMinResolution, min(kMaxResolution, self.nozzleOptions.resolution_pixelsPerInch))
        self.animationOptions.animateBy = max(0, min(kAnimateByAge, self.animationOptions.animateBy))
        self.animationOptions.xRotationIncrement = max(-360, min(360, self.animationOptions.xRotationIncrement))
        # will check against max plant age later
        self.animationOptions.ageIncrement = max(0, min(1000, self.animationOptions.ageIncrement))
        self.animationOptions.resolution_pixelsPerInch = max(kMinResolution, min(kMaxResolution, self.animationOptions.resolution_pixelsPerInch))
        for i in range(1, u3dexport.k3DExportTypeLast + 1):
            self.exportOptionsFor3D[i].exportType = max(0, min(kIncludeAllPlants, self.exportOptionsFor3D[i].exportType))
            self.exportOptionsFor3D[i].layeringOption = max(u3dexport.kLayerOutputAllTogether, min(u3dexport.kLayerOutputByPlantPart, self.exportOptionsFor3D[i].layeringOption))
            self.exportOptionsFor3D[i].stemCylinderFaces = max(kMinOutputCylinderFaces, min(kMaxOutputCylinderFaces, self.exportOptionsFor3D[i].stemCylinderFaces))
            self.exportOptionsFor3D[i].lengthOfShortName = max(1, min(60, self.exportOptionsFor3D[i].lengthOfShortName))
            self.exportOptionsFor3D[i].xRotationBeforeDraw = max(-180, min(180, self.exportOptionsFor3D[i].xRotationBeforeDraw))
            self.exportOptionsFor3D[i].overallScalingFactor_pct = max(1, min(10000, self.exportOptionsFor3D[i].overallScalingFactor_pct))
            self.exportOptionsFor3D[i].directionToPressPlants = max(u3dexport.kX, min(u3dexport.kZ, self.exportOptionsFor3D[i].directionToPressPlants))
            self.exportOptionsFor3D[i].dxf_whereToGetColors = max(u3dexport.kColorDXFFromPlantPartType, min(u3dexport.kColorDXFFromOneColor, self.exportOptionsFor3D[i].dxf_whereToGetColors))
            self.exportOptionsFor3D[i].dxf_wholePlantColorIndex = max(0, min(u3dexport.kLastDxfColorIndex, self.exportOptionsFor3D[i].dxf_wholePlantColorIndex))
            for j in range(0, u3dexport.kExportPartLast + 1):
                self.exportOptionsFor3D[i].dxf_plantPartColorIndexes[j] = max(0, min(u3dexport.kLastDxfColorIndex, self.exportOptionsFor3D[i].dxf_plantPartColorIndexes[j]))
            self.exportOptionsFor3D[i].pov_minLineLengthToWrite = max(0.0, min(100.0, self.exportOptionsFor3D[i].pov_minLineLengthToWrite))
            self.exportOptionsFor3D[i].pov_minTdoScaleToWrite = max(0.0, min(100.0, self.exportOptionsFor3D[i].pov_minTdoScaleToWrite))
            self.exportOptionsFor3D[i].vrml_version = max(u3dexport.kVRMLVersionOne, min(u3dexport.kVRMLVersionTwo, self.exportOptionsFor3D[i].vrml_version))

    # --------------------------------------------------------------------------- plant file i/o
    def load(self, fileName):
        extension = ""

        self.plantFileLoaded = False
        try:
            self.plantFileName = fileName
            self.plantFileName = ExpandFileName(self.plantFileName)
            # v2.1 check for file extension - when opening file on startup or send to
            extension = usupport.stringBeyond(ExtractFileName(self.plantFileName), ".").lower()
            if extension != "pla":
                ShowMessage("The file (" + self.plantFileName + ") does not have the correct extension (pla).")
            else:
                self.plantManager.loadPlantsFromFile(fileName, kNotInPlantMover)
                self.plantFileLoaded = True
                if umain.MainForm != None:
                    umain.MainForm.setPlantFileChanged(False)
                self.lastOpenedPlantFileName = self.plantFileName
                self.lastOpenedPlantFileName = self.lastOpenedPlantFileName.strip()
                # v1.60
                self.updateRecentFileNames(self.lastOpenedPlantFileName)
        except:
            self.plantFileLoaded = False
            #callers need exception
            raise

    def save(self, fileName):
        self.plantManager.savePlantsToFile(fileName, kNotInPlantMover)

    # v1.60
    def updateRecentFileNames(self, aFileName):
        i = 0
        saved = False

        for i in range(0, kMaxRecentFiles):
            if self.options.recentFiles[i] == aFileName:
                # first look to see if the file is already there, and if so don't record it twice
                return
        # now look for an empty spot in the array
        saved = False
        for i in range(0, kMaxRecentFiles):
            if self.options.recentFiles[i] == "":
                self.options.recentFiles[i] = aFileName
                saved = True
                break
        if not saved:
            for i in range(0, kMaxRecentFiles):
                if i < kMaxRecentFiles - 1:
                    # if there was no empty spot, shift the files up one and add it to the end
                    self.options.recentFiles[i] = self.options.recentFiles[i + 1]
                else:
                    self.options.recentFiles[i] = aFileName
        if umain.MainForm != None:
            # PDF PORTING -- maybe syntax error in original -- had empty parens -- unless intended as procedure or fucntion call from pointer? Probably nt
            umain.MainForm.updateFileMenuForOtherRecentFiles()

    def resetForEmptyPlantFile(self):
        self.plantManager.plants.clear()
        self.plantFileLoaded = True
        self.plantFileName = kUnsavedFileName + "." + usupport.extensionForFileType(usupport.kFileTypePlant)
        self.lastOpenedPlantFileName = ""
        if umain.MainForm != None:
            umain.MainForm.setPlantFileChanged(False)

    def resetForNoPlantFile(self):
        self.plantManager.plants.clear()
        self.plantFileLoaded = False
        self.plantFileName = ""
        self.lastOpenedPlantFileName = ""
        if umain.MainForm != None:
            umain.MainForm.setPlantFileChanged(False)

    def checkForExistingDefaultTdoLibrary(self):
        result = False
        # returns False if user wants to cancel action
        result = True
        if not FileExists(self.defaultTdoLibraryFileName):
            MessageDialog("No 3D object library has been chosen." + chr(13) + chr(13) + "In order to continue with what you are doing," + chr(13) + "you need to choose a 3D object library" + chr(13) + "from the dialog that follows this one.", mtWarning, [mbOK, ], 0)
            self.defaultTdoLibraryFileName = usupport.getFileOpenInfo(usupport.kFileTypeTdo, self.defaultTdoLibraryFileName, "Choose a 3D object library (tdo) file")
            result = self.defaultTdoLibraryFileName != ""
        return result

    def totalUnregisteredExportsAtThisMoment(self):
        result = 0
        result = self.unregisteredExportCountBeforeThisSession + self.unregisteredExportCountThisSession
        return result

    # ------------------------------------------------------------------- file/directory utilities
    def nameIsAbsolute(self, fileName):
        result = False
        result = ((UNRESOLVED.pos("\\", fileName) == 1) or (UNRESOLVED.pos(":", fileName) == 2))
        return result

    def isFileInPath(self, fileName):
        result = False
        qualifiedName = ""

        result = True
        #see if file exists
        qualifiedName = fileName
        if not FileExists(qualifiedName):
            if not self.nameIsAbsolute(fileName):
                #this merging process could be more sophisticated in case
                #     file name has leading drive or leading slash - just not merging for now
                qualifiedName = ExtractFilePath(delphi_compatability.Application.exeName) + fileName
            if not FileExists(qualifiedName):
                result = False
        return result

    #searches for file according to name, and then in exe directory, and then gives up
    def buildFileNameInPath(self, fileName):
        result = ""
        result = ExpandFileName(fileName)
        if FileExists(result):
            return result
        result = ExtractFilePath(delphi_compatability.Application.exeName) + ExtractFileName(fileName)
        if FileExists(result):
            return result
        result = fileName
        return result

    def firstUnusedUnsavedFileName(self):
        result = ""
        fileNumber = 0

        result = ""
        fileNumber = 1
        while fileNumber < 100:
            result = ExtractFilePath(delphi_compatability.Application.exeName) + self.unsavedFileNameForNumber(fileNumber)
            if not FileExists(result):
                return result
            fileNumber += 1
        ShowMessage("Too many unnamed plant files. Delete some to reuse names.")
        return result

    def unsavedFileNameForNumber(self, aNumber):
        result = ""
        numberString = ""

        numberString = "%d" % (aNumber)
        if len(numberString) == 1:
            numberString = "0" + numberString
        result = kUnsavedFileName + numberString + ".pla"
        return result

    def getColorUsingCustomColors(self, originalColor):
        # may be more efficient to do this from main window, because a colorDialog component on the form
        # would keep the custom colors between uses without having to change the domain colors
        result = originalColor
        colorDialog = delphi_compatability.TColorDialog().Create(delphi_compatability.Application)
        colorDialog.Color = originalColor
        colorDialog.customColors.clear
        for i in range(0, kMaxCustomColors):
            if self.options.customColors[i] == originalColor:
                # add new color to custom colors if not already there and there is room
                # (this assumes they don't want black as a custom color)
                break
            if self.options.customColors[i] == delphi_compatability.clBlack:
                self.options.customColors[i] = originalColor
                break
        for i in range(0, kMaxCustomColors):
            # load our custom colors into color dialog custom colors
            colorString = "Color" + chr(ord("A") + i) + "=" + UNRESOLVED.Format("%.6x", [self.options.customColors[i], ])
            colorDialog.customColors.add(colorString)
        colorDialog.options = [UNRESOLVED.cdFullOpen, ]
        try:
            if colorDialog.Execute():
                result = colorDialog.Color
                for i in range(0, colorDialog.customColors.count):
                    colorString = colorDialog.customColors[i]
                    colorString = usupport.stringBeyond(colorString, "=")
                    color = StrToIntDef("$" + colorString, 0)
                    self.options.customColors[i] = color
        finally:
            colorDialog.free
        return result

    def sectionNumberFor3DExportType(self, anOutputType):
        result = 0
        if anOutputType == u3dexport.kDXF:
            result = kSectionDXF
        elif anOutputType == u3dexport.kPOV:
            result = kSectionPOV
        elif anOutputType == u3dexport.k3DS:
            result = kSection3DS
        elif anOutputType == u3dexport.kOBJ:
            result = kSectionOBJ
        elif anOutputType == u3dexport.kVRML:
            result = kSectionVRML
        elif anOutputType == u3dexport.kLWO:
            result = kSectionLWO
        else :
            raise GeneralException.create("Problem: Invalid type in PdDomain.sectionNumberFor3DExportType.")
        return result

    def plantDrawOffset_mm(self):
        result = usupport.setSinglePoint(0, 0)
        if self.plantManager == None:
            return result
        result = self.plantManager.plantDrawOffset_mm
        return result

    def plantDrawScale_PixelsPerMm(self):
        result = 1.0
        if self.plantManager == None:
            return result
        result = self.plantManager.plantDrawScale_PixelsPerMm
        return result

    def viewPlantsInMainWindowFreeFloating(self):
        result = self.options.mainWindowViewMode == kViewPlantsInMainWindowFreeFloating
        return result

    def viewPlantsInMainWindowOnePlantAtATime(self):
        result = self.options.mainWindowViewMode == kViewPlantsInMainWindowOneAtATime
        return result


# global var
domain = PdDomain()
# this also sets up the section manager
domain.parameterManager.makeParameters()
domain.getProfileInformationFromFile("")

if __name__ == "__main__":
    print "domain", domain
    print domain.parameterManager.parameters.list
    for p in domain.parameterManager.parameters.list:
        print p.fieldNumber, p.getName(), "=", p.fieldID
        print "   ", p.getHint()
        if p.fieldType == 5:
            print "   3D object", p.defaultValueString()
        else:
            print "   ", p.defaultValueString(), "between", p.lowerBound(), "and", p.upperBound()
        print "   ", "fieldType=%s" % (domain.parameterManager.fieldTypeName(p.fieldType))
        print "   ", p.accessString
        #print "   ", p.unitMetric, p.unitModel
    # p.fieldType defined in uparams.py
    print dir(domain.parameterManager.parameters.list[0])

