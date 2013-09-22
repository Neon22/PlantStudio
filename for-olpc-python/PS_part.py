# unit upart

###
# Base class for Plant parts.
# Inherited by PdInternode, PdMeristem, PdInflorescence, PdFlowerFruit, PdLeaf



from PS_common import *
from PS_constants import *
#import ufiler
#mport uplant
#mport delphi_compatability
import PS_travers
import udomain
import PS_3dexport
import PS_support

import udebug



### const
##kAddingBiomassToPlant = True
##kRemovingBiomassFromPlant = False
##kDontTaper = -1.0
##kUseAmendment = True
##kDontUseAmendment = False
##
### const
##kDrawingTdo = True
##kDrawingLine = False
##kRotateX = 0
##kRotateY = 1
##kRotateZ = 2

# const
kMaxLineOutputPoints = 200

class PdPlantPart(object):#ufiler.PdStreamableObject): # object):#!! removed
    def __init__(self):
        # structure
        self.plant = None
        #
        self.liveBiomass_pctMPB = 0.0
        self.deadBiomass_pctMPB = 0.0
        self.biomassDemand_pctMPB = 0.0
        self.gender = 0
        self.age = 0  #0L
        self.randomSwayIndex = 0.0
        self.hasFallenOff = False
        self.isSeedlingLeaf = False
        self.partID = 0 #0L
        self.boundsRect = Rect()
        self.amendment = None
        self.parentAmendment = None
        self.biomassOfMeAndAllPartsAboveMe_pctMPB = 0.0

    # ---------------------------------------------------------------------------------- initialize
    def initialize(self, thePlant):
        #initialize generic plant part
        self.plant = thePlant
        # v1.6b1
        self.plant.partsCreated += 1
        self.partID = self.plant.partsCreated
        self.age = 0
        self.gender = kGenderFemale
        self.hasFallenOff = False
        self.randomSwayIndex = self.plant.randomNumberGenerator.zeroToOne()

    def nextDay(self):
        #next day procedure for generic plant part
        self.age += 1

    def getName(self):
        result = ""
        # subclasses should override
        result = "plant part"
        return result

    def getFullName(self):
        result = ""
        result = "part %d (" % (self.partID) + self.getName() + ")"
        return result

    # ---------------------------------------------------------------------------------- traversing
    def traverseActivity(self, mode, traverserProxy):
        ''' first thing each phytomer part does when traversing is call here
            then process their own
            - deals with Biomass and veg or reproductive %
            - also used for finding a part, or counting triangles
        '''
        traverser = traverserProxy
        if traverser == None:
            return
        if mode == kActivityNone:
            pass
        elif mode == kActivityNextDay:
            pass
        elif mode == kActivityDemandVegetative:
            #inc(traverser.totalPlantParts)
            self.biomassDemand_pctMPB = 0.0
        elif mode == kActivityDemandReproductive:
            self.biomassDemand_pctMPB = 0.0
        elif mode == kActivityGrowVegetative:
            pass
        elif mode == kActivityGrowReproductive:
            pass
        elif mode == kActivityStartReproduction:
            pass
        elif mode == kActivityFindPlantPartAtPosition:
            pass
        elif mode == kActivityDraw:
            traverser.totalPlantParts += 1
            self.determineAmendmentAndAlsoForChildrenIfAny()
        elif mode == kActivityReport:
            self.report()
        elif mode == kActivityStream:
            pass
        elif mode == kActivityFree:
            pass
        elif mode == kActivityVegetativeBiomassThatCanBeRemoved:
            pass
        elif mode == kActivityRemoveVegetativeBiomass:
            pass
        elif mode == kActivityReproductiveBiomassThatCanBeRemoved:
            pass
        elif mode == kActivityRemoveReproductiveBiomass:
            pass
        elif mode == kActivityStandingDeadBiomassThatCanBeRemoved:
            traverser.total = traverser.total + self.deadBiomass_pctMPB
        elif mode == kActivityRemoveStandingDeadBiomass:
            biomassToRemove_pctMPB = self.deadBiomass_pctMPB * traverser.fractionOfPotentialBiomass
            self.deadBiomass_pctMPB = self.deadBiomass_pctMPB - biomassToRemove_pctMPB
        elif mode == kActivityGatherStatistics:
            pass
        elif mode == kActivityCountPlantParts:
            traverser.totalPlantParts += 1
        elif mode == kActivityFindPartForPartID:
            if traverser.partID == self.partID:
                traverser.foundPlantPart = self
                traverser.finished = True
        elif mode == kActivityCountTotalMemoryUse:
            pass
        elif mode == kActivityCalculateBiomassForGravity:
            self.biomassOfMeAndAllPartsAboveMe_pctMPB = self.totalBiomass_pctMPB()
        elif mode == kActivityCountPointsAndTrianglesFor3DExport:
            traverser.totalPlantParts += 1
        else :
            raise GeneralException.create("Problem: Unhandled mode in method PdPlantPart.traverseActivity.")

    # procedure fillInInfoForDXFPart(index: smallint; var realIndex: smallint; var longName: string; var shortName: string);
    def position(self):
        result = TPoint()
        result = Point(self.boundsRect.Left + (self.boundsRect.Right - self.boundsRect.Left) / 2, self.boundsRect.Top + (self.boundsRect.Bottom - self.boundsRect.Top) / 2)
        return result

    def addExportMaterial(self, traverserProxy, femaleIndex, maleIndex):
        traverser = PdTraverser()

        # remember that this is not a true count; each part only adds at LEAST one
        # if you wanted to use this for a true export-type-part count you would have to amend some code
        traverser = traverserProxy
        if traverser == None:
            return
        if maleIndex < 0:
            # means to ignore gender
            traverser.exportTypeCounts[femaleIndex] += 1
        elif self.gender == kGenderFemale:
            traverser.exportTypeCounts[femaleIndex] += 1
        else:
            traverser.exportTypeCounts[maleIndex] += 1

    def addToStatistics(self, statisticsProxy, partType):
        statistics = PdPlantStatistics()

        statistics = PS_travers.PdPlantStatistics(statisticsProxy)
        if statistics == None:
            return
        if self.hasFallenOff:
            return
        statistics.count[partType] = statistics.count[partType] + 1
        statistics.liveBiomass_pctMPB[partType] = statistics.liveBiomass_pctMPB[partType] + self.liveBiomass_pctMPB
        statistics.deadBiomass_pctMPB[partType] = statistics.deadBiomass_pctMPB[partType] + self.deadBiomass_pctMPB

    def totalBiomass_pctMPB(self):
        result = 0.0
        result = self.liveBiomass_pctMPB + self.deadBiomass_pctMPB
        return result

    def fractionLive(self):
        result = 0.0
        result = 0.0
        try:
            if self.totalBiomass_pctMPB() > 0.0:
                result = umath.safedivExcept(self.liveBiomass_pctMPB, self.totalBiomass_pctMPB(), 0)
            else:
                result = 0.0
        except Exception, e:
            PS_support.messageForExceptionType(e, "PdPlantPart.fractionLive")
        return result

    def draw(self):
        pass
        # implemented by subclasses

    def isPhytomer(self):
        return False

    def addOrRemove(self, addOrRemoveFlag):
        if addOrRemoveFlag == kAddingBiomassToPlant:
            self.hasFallenOff = False
        else:
            self.hasFallenOff = True

    def setColorsToParameters(self):
        pass
        #subclasses can override

    def genderString(self):
        result = ""
        if self.gender == kGenderFemale:
            result = "primary"
        else:
            result = "secondary"
        return result

    def report(self):
        partName = ""

        if self.partType() == kPartTypeFlowerFruit:
            partName = "flower/fruit"
        elif self.partType() == kPartTypeInflorescence:
            partName = "inflorescence"
        elif self.partType() == kPartTypeMeristem:
            partName = "meristem"
        elif self.partType() == kPartTypePhytomer:
            partName = "internode"
        elif self.partType() == kPartTypeLeaf:
            partName = "leaf"
        udebug.DebugPrint("Part %d, %14s" % (self.partID, partName) + " Biomass: %4.2f live=%4.2f dead=%4.2f" % (self.biomassDemand_pctMPB, self.liveBiomass_pctMPB, self.deadBiomass_pctMPB) )

    # ---------------------------------------------------------------------------------- drawing
    def draw3DObject(self, tdo, scale, faceColor, backfaceColor, dxfIndex):
        if tdo == None:
            return
        turtle = self.plant.turtle
        if (turtle == None):
            return
        if self.setColorsWithAmendmentAndReturnTrueIfNoOverrides(kDrawingTdo):
            turtle.setForeColorBackColor(faceColor, backfaceColor)
            turtle.setLineColor(PS_support.darkerColor(faceColor))
        realScale = scale * self.scaleMultiplierConsideringAmendments()
        turtle.setLineWidth(1.0)
        tdo.draw(turtle, realScale, self.longNameForDXFPartConsideringGenderEtc(dxfIndex), self.shortNameForDXFPartConsideringGenderEtc(dxfIndex), self.realDxfIndexForBaseDXFPart(dxfIndex), self.partID)

    def drawStemSegment(self, length, width, angleZ, angleY, color, taperIndex, dxfIndex, useAmendment):
        turtle = self.plant.turtle
        if (turtle == None):
            return
        if turtle.ifExporting_excludeStem(length):
            return
        if self.setColorsWithAmendmentAndReturnTrueIfNoOverrides(kDrawingLine):
            turtle.setLineColor(color)
        realLength = length * self.lengthMultiplierConsideringAmendments()
        realWidth = width * self.widthMultiplierConsideringAmendments()
        # set up for export
        #for POV you want radius not diameter
        turtle.ifExporting_startStemSegment(self.longNameForDXFPartConsideringGenderEtc(dxfIndex), self.shortNameForDXFPartConsideringGenderEtc(dxfIndex), color, realWidth / 2.0, dxfIndex)
        if turtle.drawOptions.straightLinesOnly:
            # get number of segments
            lineDivisions = 1
        else:
            lineDivisions = self.plant.pGeneral.lineDivisions
        # figure length and turn of each segment
        realAngleX = self.rotateAngleConsideringAmendment(kRotateX, useAmendment, 0)
        realAngleY = self.rotateAngleConsideringAmendment(kRotateY, useAmendment, angleY)
        realAngleZ = self.rotateAngleConsideringAmendment(kRotateZ, useAmendment, angleZ)
        if lineDivisions > 1:
            turnPortionZ = realAngleZ / lineDivisions
            turnPortionY = realAngleY / lineDivisions
            drawPortion = realLength / lineDivisions
        else:
            turnPortionZ = realAngleZ
            turnPortionY = realAngleY
            drawPortion = realLength
        # figure width for tapering
        startWidth = realWidth
        if taperIndex > 0:
            endWidth = startWidth * taperIndex / 100.0
        else:
            endWidth = realWidth
        startPortionWidth = startWidth
        endPortionWidth = startPortionWidth
        if realAngleX != 0:
            turtle.rotateX(realAngleX)
        for i in range(0, lineDivisions):
            isLastSegment = (i >= lineDivisions - 1)
            if not isLastSegment:
                # because of rounding, last segment uses leftover, not equal portion
                segmentTurnZ = turnPortionZ
                segmentTurnY = turnPortionY
                segmentLength = drawPortion
            else:
                segmentTurnZ = (realAngleZ - (turnPortionZ * (lineDivisions - 1)))
                segmentTurnY = (realAngleY - (turnPortionY * (lineDivisions - 1)))
                segmentLength = (realLength - (drawPortion * (lineDivisions - 1)))
            if (taperIndex > 0) and (lineDivisions > 1):
                # figure tapering for section
                # lineDivisions part added in v1.6b3
                startPortionWidth = startWidth - (i / (lineDivisions - 1)) * (startWidth - endWidth)
                if not isLastSegment:
                    endPortionWidth = startWidth - ((i + 1) / (lineDivisions - 1)) * (startWidth - endWidth)
                else:
                    endPortionWidth = endWidth
            # set width, rotate, draw line
            turtle.setLineWidth(startPortionWidth)
            turtle.rotateY(segmentTurnY)
            turtle.rotateZ(segmentTurnZ)
            if turtle.exportingToFile():
                self.write3DExportLine(self.partID, segmentLength, startPortionWidth, endPortionWidth, i)
            else:
                triangleMade = turtle.drawInMillimeters(segmentLength, self.partID)
                if (turtle.drawOptions.sortTdosAsOneItem) and (triangleMade != None):
                    triangleMade.tdo = self.tdoToSortLinesWith()
        turtle.ifExporting_endStemSegment()

    def write3DExportLine(self, partID, length, startWidth, endWidth, segmentNumber):
        turtle = self.plant.turtle
        if turtle == None:
            return
        if turtle.writingToPOV():
            # POV draws cylinders directly, not with faces
            turtle.drawInMillimeters(length, partID)
            return
        faces = turtle.ifExporting_stemCylinderFaces()
        if faces == 0:
            return
        startPoints = [None] * faces
        endPoints = [None] * faces
        if segmentNumber <= 0:
            # get startWidth points; if done before, copy from last endWidth points
            pipeRadius = 0.5 * startWidth
            for i in range(0, faces):
                turtle.push()
                turtle.rotateX(i * 256 / faces)
                turtle.rotateZ(64)
                turtle.moveInMillimeters(pipeRadius)
                startPoints[i] = turtle.position()
                turtle.pop()

        else:
            #for i in range(0, faces):
            # PDF PORT -- this code seems useless, copying from unassigned varialbes, so changed as following line
                #startPoints[i] = endPoints[i]
                startPoints[i] = u3dsupport.KfPoint3D()

        turtle.moveInMillimeters(length)
        # get endWidth points
        pipeRadius = 0.5 * endWidth
        for i in range(0, faces):
            turtle.push()
            turtle.rotateX(i * 256 / faces)
            turtle.rotateZ(64)
            turtle.moveInMillimeters(pipeRadius)
            endPoints[i] = turtle.position()
            turtle.pop()
        # draw pipe faces from stored points
        turtle.drawFileExportPipeFaces(startPoints, endPoints, faces, segmentNumber)

    def tdoToSortLinesWith(self):
        # subclasses can override
        result = None
        return result

    def partType(self):
        result = 0
        # implemented by subclasses
        result = 0
        return result

    def angleWithSway(self, angle):
        result = 0.0
        result = angle
        if self.plant == None:
            return result
        result = angle + ((self.randomSwayIndex - 0.5) * self.plant.pGeneral.randomSway)
        return result

    # ---------------------------------------------------------------------------------- amendments
    def determineAmendmentAndAlsoForChildrenIfAny(self):
        self.amendment = self.plant.amendmentForPartID(self.partID)

    def hiddenByAmendment(self):
        result = False
        if not udomain.domain.options.showPosingAtAll:
            return result
        if self.plant.turtle == None:
            return result
        iHaveAnAmendment = self.amendment != None
        iDontHaveAnAmendment = self.amendment == None
        myParentHasAnAmendment = self.parentAmendment != None
        myAmendmentSaysIAmHidden = (self.amendment != None) and (self.amendment.hide)
        myParentsAmendmentSaysIAmHidden = (self.parentAmendment != None) and (self.parentAmendment.hide)
        drawingToMainWindow = (self.plant.turtle.writingTo == kScreen) and (not udomain.domain.drawingToMakeCopyBitmap)
        if (iHaveAnAmendment and myAmendmentSaysIAmHidden) or (iDontHaveAnAmendment and myParentHasAnAmendment and myParentsAmendmentSaysIAmHidden):
            if drawingToMainWindow:
                result = not udomain.domain.options.showGhostingForHiddenParts
            else:
                result = True
        return result

    def applyAmendmentRotations(self):
        if (self.amendment != None) and (self.amendment.addRotations) and (udomain.domain.options.showPosingAtAll):
            self.plant.turtle.rotateX(self.amendment.xRotation * 256 / 360)
            self.plant.turtle.rotateY(self.amendment.yRotation * 256 / 360)
            self.plant.turtle.rotateZ(self.amendment.zRotation * 256 / 360)

    def setColorsWithAmendmentAndReturnTrueIfNoOverrides(self, drawingTdo):
        result = True
        if not udomain.domain.options.showPosingAtAll:
            return result
        if self.plant.turtle == None:
            return result
        color = 0
        backfaceColor = 0
        lineColor = 0
        iHaveAnAmendment = self.amendment != None
        iDontHaveAnAmendment = self.amendment == None
        myParentHasAnAmendment = self.parentAmendment != None
        myAmendmentSaysIAmHidden = (self.amendment != None) and (self.amendment.hide)
        myParentsAmendmentSaysIAmHidden = (self.parentAmendment != None) and (self.parentAmendment.hide)
        iAmSelectedInTheMainWindow = False
        ### PDF PORT __ TEMP COMMENTED OUT iAmSelectedInTheMainWindow = (self.partID == umain.MainForm.selectedPlantPartID) and (umain.MainForm.focusedPlant() == self.plant)
        showHighlights = udomain.domain.options.showHighlightingForNonHiddenPosedParts and (self.plant.turtle.writingTo == kScreen) and (not udomain.domain.drawingToMakeCopyBitmap) and (not self.plant.drawingIntoPreviewCache)
        if iHaveAnAmendment or myParentHasAnAmendment:
            result = False
            if (iHaveAnAmendment and iAmSelectedInTheMainWindow and showHighlights):
                color = udomain.domain.options.selectedPosedColor
            elif (iHaveAnAmendment and myAmendmentSaysIAmHidden) or (iDontHaveAnAmendment and myParentHasAnAmendment and myParentsAmendmentSaysIAmHidden):
                color = udomain.domain.options.ghostingColor
            elif (iHaveAnAmendment and showHighlights):
                color = udomain.domain.options.nonHiddenPosedColor
            else:
                result = True
        if result == False:
            if backfaceColor == 0:
                backfaceColor = color
            if lineColor == 0:
                lineColor = color
            if drawingTdo:
                self.plant.turtle.setForeColorBackColor(color, backfaceColor)
                self.plant.turtle.setLineColor(PS_support.darkerColor(color))
            else:
                self.plant.turtle.setLineColor(lineColor)
        return result

    # posed color part > if put this back, put it AFTER ghostingColor and BEFORE nonHiddenPosedColor
    #
    #    else if ((amendment <> nil) and (amendment.changeColors))
    #        or ((parentAmendment <> nil) and (parentAmendment.changeColors) and (parentAmendment.propagateColors)) then
    #      begin
    #      // directly changed colors take precedence over highlighting
    #      if amendment <> nil then amendmentToUse := amendment else amendmentToUse := parentAmendment;
    #      color := amendmentToUse.faceColor;
    #      backFaceColor := amendmentToUse.backfaceColor;
    #      lineColor := amendmentToUse.lineColor;
    #      end
    #
    def rotateAngleConsideringAmendment(self, rotateWhat, useAmendment, angle):
        result = angle
        if (useAmendment) and (self.amendment != None) and (self.amendment.addRotations) and (udomain.domain.options.showPosingAtAll):
            if rotateWhat == kRotateX:
                result = angle + self.amendment.xRotation * 256 / 360
            elif rotateWhat == kRotateY:
                result = angle + self.amendment.yRotation * 256 / 360
            elif rotateWhat == kRotateZ:
                result = angle + self.amendment.zRotation * 256 / 360
        return result

    def scaleMultiplierConsideringAmendments(self):
        result = 1.0
        if not udomain.domain.options.showPosingAtAll:
            return result
        if (self.amendment != None) or (self.parentAmendment != None):
            if ((self.amendment != None) and (self.amendment.multiplyScale)) or ((self.parentAmendment != None) and (self.parentAmendment.multiplyScale) and (self.parentAmendment.propagateScale)):
                if self.amendment != None:
                    amendmentToUse = self.amendment
                else:
                    amendmentToUse = self.parentAmendment
                result = 1.0 * amendmentToUse.scaleMultiplier_pct / 100.0
        return result

    def lengthMultiplierConsideringAmendments(self):
        result = 1.0
        if not udomain.domain.options.showPosingAtAll:
            return result
        if (self.amendment != None) or (self.parentAmendment != None):
            if ((self.amendment != None) and (self.amendment.multiplyScale)) or ((self.parentAmendment != None) and (self.parentAmendment.multiplyScale) and (self.parentAmendment.propagateScale)):
                if self.amendment != None:
                    amendmentToUse = self.amendment
                else:
                    amendmentToUse = self.parentAmendment
                result = 1.0 * amendmentToUse.lengthMultiplier_pct / 100.0
        return result

    def widthMultiplierConsideringAmendments(self):
        result = 1.0
        if not udomain.domain.options.showPosingAtAll:
            return result
        if (self.amendment != None) or (self.parentAmendment != None):
            if ((self.amendment != None) and (self.amendment.multiplyScale)) or ((self.parentAmendment != None) and (self.parentAmendment.multiplyScale) and (self.parentAmendment.propagateScale)):
                if self.amendment != None:
                    amendmentToUse = self.amendment
                else:
                    amendmentToUse = self.parentAmendment
                result = 1.0 * amendmentToUse.widthMultiplier_pct / 100.0
        return result

    # ---------------------------------------------------------------------------------- streaming
    def classAndVersionInformation(self, cvir):
        cvir.classNumber = uclasses.kPdPlantPart
        cvir.versionNumber = 0
        cvir.additionNumber = 0

    #this will stream entire the entire object -
    #but the included object references need to be fixed up afterwards
    #or the objects streamed out separately afterwards - subclasses overrides
    #need to call inherited to get this behavior
    def streamDataWithFiler(self, filer, cvir):
        PdStreamableObject.streamDataWithFiler(self, filer, cvir)
        self.liveBiomass_pctMPB = filer.streamSingle(self.liveBiomass_pctMPB)
        self.deadBiomass_pctMPB = filer.streamSingle(self.deadBiomass_pctMPB)
        self.biomassDemand_pctMPB = filer.streamSingle(self.biomassDemand_pctMPB)
        self.gender = filer.streamSmallint(self.gender)
        self.age = filer.streamLongint(self.age)
        self.hasFallenOff = filer.streamBoolean(self.hasFallenOff)
        self.isSeedlingLeaf = filer.streamBoolean(self.isSeedlingLeaf)
        self.partID = filer.streamLongint(self.partID)
        self.biomassOfMeAndAllPartsAboveMe_pctMPB = filer.streamSingle(self.biomassOfMeAndAllPartsAboveMe_pctMPB)
        self.randomSwayIndex = filer.streamSingle(self.randomSwayIndex)

    def addDependentPartsToList(self, aList):
        pass
        # subclasses can override

    def blendColorsStrength(self, aColor, aStrength):
        pass
        #subclasses can override

    def calculateColors(self):
        self.setColorsToParameters()

    def longNameForDXFPartConsideringGenderEtc(self, index):
        result = ""
        result = PS_3dexport.longNameForDXFPartType(self.realDxfIndexForBaseDXFPart(index))
        return result

    def shortNameForDXFPartConsideringGenderEtc(self, index):
        result = ""
        result = PS_3dexport.shortNameForDXFPartType(self.realDxfIndexForBaseDXFPart(index))
        return result

    def realDxfIndexForBaseDXFPart(self, index):
        result = 0
        result = index
        if index == kExportPartLeaf:
            if self.isSeedlingLeaf:
                result = kExportPartSeedlingLeaf
        elif index == kExportPartPetiole:
            if self.isSeedlingLeaf:
                result = kExportPartFirstPetiole
        elif index == kExportPartInflorescenceStalkFemale:
            if self.gender == kGenderMale:
                result = kExportPartInflorescenceStalkMale
        elif index == kExportPartInflorescenceInternodeFemale:
            if self.gender == kGenderMale:
                result = kExportPartInflorescenceInternodeMale
        elif index == kExportPartInflorescenceBractFemale:
            if self.gender == kGenderMale:
                result = kExportPartInflorescenceBractMale
        elif index == kExportPartPedicelFemale:
            if self.gender == kGenderMale:
                result = kExportPartPedicelMale
        elif index == kExportPartFlowerBudFemale:
            if self.gender == kGenderMale:
                result = kExportPartFlowerBudMale
        elif index == kExportPartFilamentFemale:
            if self.gender == kGenderMale:
                result = kExportPartFilamentMale
        elif index == kExportPartAntherFemale:
            if self.gender == kGenderMale:
                result = kExportPartAntherMale
        elif index == kExportPartFirstPetalsFemale:
            if self.gender == kGenderMale:
                result = kExportPartFirstPetalsMale
        elif index == kExportPartSepalsFemale:
            if self.gender == kGenderMale:
                result = kExportPartSepalsMale
        return result

