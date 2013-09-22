### PS_leaf
### - in growth cycle, calculates when budding happens
### - called by PS_merist and PS_intern
### Dependencies:
###     - PS_part for class, func
###     -
###     - PS_math for safediv, pointsAreCloseEnough, odd, Scurves...
###     - PS_support for error message

from PS_common import *
from PS_constants import *
import PS_part
import PS_math
import PS_support
import PS_travers


import math


# const
kNumCompoundLeafRandomSwayIndexes = 49

class PdLeaf(PS_part.PdPlantPart):
    def __init__(self):
        super(PdLeaf, self).__init__()
        #PS_part.PdPlantPart.__init__(self)
        self.sCurveParams = PS_math.SCurveStructure()
        self.propFullSize = 0.0
        self.biomassAtCreation_pctMPB = 0.0
        self.compoundLeafRandomSwayIndexes = [0] * (kNumCompoundLeafRandomSwayIndexes + 1)

    def NewWithPlantFractionOfOptimalSize(self, aPlant, aFraction):
        self.initializeFractionOfOptimalSize(aPlant, aFraction)
        return self

    def initializeFractionOfOptimalSize(self, thePlant, aFraction):
        try:
            self.initialize(thePlant)
            #Plant sets this from outside on first phytomer.
            self.isSeedlingLeaf = False
            self.liveBiomass_pctMPB = aFraction * PdLeaf.optimalInitialBiomass_pctMPB(self.plant)
            self.deadBiomass_pctMPB = 0.0
            self.propFullSize = PS_math.safedivExcept(self.liveBiomass_pctMPB, self.plant.pLeaf.optimalBiomass_pctMPB, 1.0)
            if self.plant.pLeaf.compoundNumLeaflets > 1:
                for i in range(0, kNumCompoundLeafRandomSwayIndexes + 1):
                    self.compoundLeafRandomSwayIndexes[i] = self.plant.randomNumberGenerator.zeroToOne()
        except Exception, e:
            # PDF PORT __ FOR TESTING
            raise
            PS_support.messageForExceptionType(e, "PdLeaf.initializeFractionOfOptimalSize")

    def optimalInitialBiomass_pctMPB(self, drawingPlant):
        result = drawingPlant.pLeaf.optimalFractionOfOptimalBiomassAtCreation_frn * drawingPlant.pLeaf.optimalBiomass_pctMPB
        return result
    optimalInitialBiomass_pctMPB = classmethod(optimalInitialBiomass_pctMPB)

    def getName(self):
        result = "leaf"
        return result

    def nextDay(self):
        try:
            PS_part.PdPlantPart.nextDay(self)
            self.checkIfHasAbscissed()
        except Exception, e:
            PS_support.messageForExceptionType(e, "PdLeaf.nextDay")

    def traverseActivity(self, mode, traverserProxy):
        PS_part.PdPlantPart.traverseActivity(self, mode, traverserProxy)
        traverser = traverserProxy
        if traverser == None:
            return
        if self.hasFallenOff and (mode != kActivityStream) and (mode != kActivityFree):
            return
        try:
            if mode == kActivityNone:
                pass
            elif mode == kActivityNextDay:
                self.nextDay()
            elif mode == kActivityDemandVegetative:
                if self.age > self.plant.pLeaf.maxDaysToGrow:
                    self.biomassDemand_pctMPB = 0.0
                    return
                fractionOfMaxAge_frn = PS_math.safedivExcept(self.age + 1, self.plant.pLeaf.maxDaysToGrow, 0.0)
                propFullSizeWanted = max(0.0, min(1.0, PS_math.scurve(fractionOfMaxAge_frn, self.plant.pLeaf.sCurveParams.c1, self.plant.pLeaf.sCurveParams.c2)))
                self.biomassDemand_pctMPB = PS_travers.linearGrowthResult(self.liveBiomass_pctMPB, propFullSizeWanted * self.plant.pLeaf.optimalBiomass_pctMPB, self.plant.pLeaf.minDaysToGrow)
                traverser.total = traverser.total + self.biomassDemand_pctMPB
            elif mode == kActivityDemandReproductive:
                pass
            elif mode == kActivityGrowVegetative:
                if self.age > self.plant.pLeaf.maxDaysToGrow:
                    # no repro. demand
                    return
                newBiomass_pctMPB = self.biomassDemand_pctMPB * traverser.fractionOfPotentialBiomass
                self.liveBiomass_pctMPB = self.liveBiomass_pctMPB + newBiomass_pctMPB
                self.propFullSize = min(1.0, PS_math.safedivExcept(self.totalBiomass_pctMPB(), self.plant.pLeaf.optimalBiomass_pctMPB, 0))
            elif mode == kActivityGrowReproductive:
                pass
            elif mode == kActivityStartReproduction:
                pass
            elif mode == kActivityFindPlantPartAtPosition:
                if PS_math.pointsAreCloseEnough(traverser.point, self.position()):
                    # no repro. growth
                    # no response
                    traverser.foundPlantPart = self
                    traverser.finished = True
            elif mode == kActivityDraw:
                pass
            elif mode == kActivityReport:
                pass
            elif mode == kActivityStream:
                pass
            elif mode == kActivityFree:
                pass
            elif mode == kActivityVegetativeBiomassThatCanBeRemoved:
                # phytomer will control drawing
                #streaming will be done by internode
                # free will be called by phytomer
                traverser.total = traverser.total + self.liveBiomass_pctMPB
            elif mode == kActivityRemoveVegetativeBiomass:
                biomassToRemove_pctMPB = self.liveBiomass_pctMPB * traverser.fractionOfPotentialBiomass
                self.liveBiomass_pctMPB = self.liveBiomass_pctMPB - biomassToRemove_pctMPB
                self.deadBiomass_pctMPB = self.deadBiomass_pctMPB + biomassToRemove_pctMPB
            elif mode == kActivityReproductiveBiomassThatCanBeRemoved:
                pass
            elif mode == kActivityRemoveReproductiveBiomass:
                pass
            elif mode == kActivityGatherStatistics:
                if self.isSeedlingLeaf:
                    # none
                    self.addToStatistics(traverser.statistics, kStatisticsPartTypeSeedlingLeaf)
                else:
                    self.addToStatistics(traverser.statistics, kStatisticsPartTypeLeaf)
                self.addToStatistics(traverser.statistics, kStatisticsPartTypeAllVegetative)
            elif mode == kActivityCountPlantParts:
                pass
            elif mode == kActivityFindPartForPartID:
                pass
            elif mode == kActivityCountTotalMemoryUse:
                traverser.totalMemorySize += self.instanceSize
            elif mode == kActivityCalculateBiomassForGravity:
                pass
            elif mode == kActivityCountPointsAndTrianglesFor3DExport:
                self.countPointsAndTrianglesFor3DExportAndAddToTraverserTotals(traverser)
            else :
                raise GeneralException.create("Problem: Unhandled mode in method PdLeaf.traverseActivity.")
        except Exception, e:
            # PDF PORT __ TEMPORARILY ADDED raise FOR TESTING
            raise
            PS_support.messageForExceptionType(e, "PdLeaf.traverseActivity")

    def checkIfHasAbscissed(self):
        pass
        # if enough biomass removed (parameter), absciss leaf or leaves
        # not doing anymore
        #if (self.fractionLive < plant.pLeaf.fractionOfLiveBiomassWhenAbscisses_frn) and (not self.hasFallenOff) then
        #  self.hasFallenOff := True;

    def destroy(self):
        PS_part.PdPlantPart.destroy(self)

    def isPhytomer(self):
        return False

    def countPointsAndTrianglesFor3DExportAndAddToTraverserTotals(self, traverser):
        if traverser == None:
            return
        if self.hasFallenOff:
            return
        if self.propFullSize <= 0:
            return
        if self.isSeedlingLeaf:
            if self.plant.pSeedlingLeaf.leafTdoParams.scaleAtFullSize > 0:
                # seedling leaf
                traverser.total3DExportPointsIn3DObjects += self.plant.pSeedlingLeaf.leafTdoParams.object3D.pointsInUse
                traverser.total3DExportTrianglesIn3DObjects += len(self.plant.pSeedlingLeaf.leafTdoParams.object3D.triangles)
                self.addExportMaterial(traverser, kExportPartSeedlingLeaf, -1)
            # not seedling leaf
        else:
            if self.plant.pLeaf.leafTdoParams.scaleAtFullSize > 0:
                # leaf (considering compound leaf)
                traverser.total3DExportPointsIn3DObjects += self.plant.pLeaf.leafTdoParams.object3D.pointsInUse * self.plant.pLeaf.compoundNumLeaflets
                traverser.total3DExportTrianglesIn3DObjects += len(self.plant.pLeaf.leafTdoParams.object3D.triangles) * self.plant.pLeaf.compoundNumLeaflets
                self.addExportMaterial(traverser, kExportPartLeaf, -1)
            if self.plant.pLeaf.stipuleTdoParams.scaleAtFullSize > 0:
                # stipule
                traverser.total3DExportPointsIn3DObjects += self.plant.pLeaf.stipuleTdoParams.object3D.pointsInUse
                traverser.total3DExportTrianglesIn3DObjects += len(self.plant.pLeaf.stipuleTdoParams.object3D.triangles)
                self.addExportMaterial(traverser, kExportPartLeafStipule, -1)
        if self.plant.pLeaf.petioleLengthAtOptimalBiomass_mm > 0:
            # petiole
            traverser.total3DExportStemSegments += 1
            if self.isSeedlingLeaf:
                self.addExportMaterial(traverser, kExportPartFirstPetiole, -1)
            else:
                self.addExportMaterial(traverser, kExportPartPetiole, -1)
            if self.plant.pLeaf.compoundNumLeaflets > 1:
                # petiolets + compound leaf internodes
                traverser.total3DExportStemSegments += self.plant.pLeaf.compoundNumLeaflets * 2

    def tdoToSortLinesWith(self):
        result = None
        if self.plant == None:
            return result
        if self.isSeedlingLeaf:
            result = self.plant.pSeedlingLeaf.leafTdoParams.object3D
        else:
            result = self.plant.pLeaf.leafTdoParams.object3D
        return result

    def drawWithDirection(self, direction):
        turtle = self.plant.turtle
        if (turtle == None):
            return
        self.boundsRect = Rect(0, 0, 0, 0)
        if self.hasFallenOff:
            return
        turtle.push()
        self.determineAmendmentAndAlsoForChildrenIfAny()
        if self.hiddenByAmendment():
            # amendment rotations handled in drawStemSegment for petiole
            turtle.pop()
            return
        try:
            if self.plant.needToRecalculateColors:
                self.calculateColors()
            self.plant.turtle.push()
            if (direction == kDirectionRight):
                turtle.rotateX(128)
            length = self.plant.pLeaf.petioleLengthAtOptimalBiomass_mm * self.propFullSize
            if (self.isSeedlingLeaf):
                length = length / 2
            width = self.plant.pLeaf.petioleWidthAtOptimalBiomass_mm * self.propFullSize
            angle = self.angleWithSway(self.plant.pLeaf.petioleAngle)
            turtle.ifExporting_startNestedGroupOfPlantParts("leaf, petiole and stipule", "LeafPetiole", kNestingTypeLeafAndPetiole)
            if self.isSeedlingLeaf:
                self.drawStemSegment(length, width, angle, 0, self.plant.pLeaf.petioleColor, self.plant.pLeaf.petioleTaperIndex, kExportPartPetiole, kUseAmendment)
                scale = (self.propFullSize * (self.plant.pSeedlingLeaf.leafTdoParams.scaleAtFullSize / 100.0)) * 1.0
                self.DrawLeafOrLeaflet(scale)
            else:
                if (self.plant.pLeaf.stipuleTdoParams.scaleAtFullSize > 0):
                    self.drawStipule()
                if (self.plant.pLeaf.compoundNumLeaflets <= 1) or self.plant.turtle.drawOptions.simpleLeavesOnly:
                    self.drawStemSegment(length, width, angle, 0, self.plant.pLeaf.petioleColor, self.plant.pLeaf.petioleTaperIndex, kExportPartPetiole, kUseAmendment)
                    scale = self.propFullSize * self.plant.pLeaf.leafTdoParams.scaleAtFullSize / 100.0
                    self.DrawLeafOrLeaflet(scale)
                else:
                    self.drawStemSegment(length, width, angle, 0, self.plant.pLeaf.petioleColor, kDontTaper, kExportPartPetiole, kUseAmendment)
                    turtle.ifExporting_startNestedGroupOfPlantParts("compound leaf", "CompoundLeaf", kNestingTypeCompoundLeaf)
                    if (self.plant.pLeaf.compoundPinnateOrPalmate == kCompoundLeafPinnate):
                        self.drawCompoundLeafPinnate()
                    else:
                        self.drawCompoundLeafPalmate()
                    turtle.ifExporting_endNestedGroupOfPlantParts(kNestingTypeCompoundLeaf)
            turtle.pop()
            turtle.ifExporting_endNestedGroupOfPlantParts(kNestingTypeLeafAndPetiole)
            turtle.pop()
        except Exception, e:
            # PDF PORT ADDED FOR TESTING
            raise
            PS_support.messageForExceptionType(e, "PdLeaf.drawWithDirection")

    def wiltLeaf(self):
        if (self.plant.turtle == None):
            #  var
            #    angle: integer;
            return
        # angle := round(abs(plant.turtle.angleX + 32) * plant.pGeneral.wiltingPercent / 100.0);
        #  if plant.turtle.angleX > -32 then
        #    angle := -angle;
        #  plant.turtle.rotateX(angle);

    def drawStipule(self):
        turtle = self.plant.turtle
        if (turtle == None):
            return
        if self.isSeedlingLeaf:
            return
        turtle.push()
        turtle.rotateX(self.angleWithSway(self.plant.pLeaf.stipuleTdoParams.xRotationBeforeDraw))
        turtle.rotateY(self.angleWithSway(self.plant.pLeaf.stipuleTdoParams.yRotationBeforeDraw))
        turtle.rotateZ(self.angleWithSway(self.plant.pLeaf.stipuleTdoParams.zRotationBeforeDraw))
        scale = (self.propFullSize * (self.plant.pLeaf.stipuleTdoParams.scaleAtFullSize / 100.0)) * 1.0
        if self.plant.pLeaf.stipuleTdoParams.repetitions > 1:
            turnPortion = 256 / self.plant.pLeaf.stipuleTdoParams.repetitions
            leftOverDegrees = 256 - turnPortion * self.plant.pLeaf.stipuleTdoParams.repetitions
            if leftOverDegrees > 0:
                addition = leftOverDegrees / self.plant.pLeaf.stipuleTdoParams.repetitions
            else:
                addition = 0
            carryOver = 0
            for i in range(0, self.plant.pLeaf.stipuleTdoParams.repetitions):
                #addThisTime = trunc(addition + carryOver)
                addThisTime = math.floor(addition + carryOver)
                carryOver = carryOver + addition - addThisTime
                if carryOver < 0:
                    carryOver = 0
                turtle.rotateY(turnPortion + addThisTime)
                if self.plant.pLeaf.stipuleTdoParams.object3D != None:
                    self.draw3DObject(self.plant.pLeaf.stipuleTdoParams.object3D, scale, self.plant.pLeaf.stipuleTdoParams.faceColor, self.plant.pLeaf.stipuleTdoParams.backfaceColor, kExportPartLeafStipule)
        elif self.plant.pLeaf.stipuleTdoParams.object3D != None:
            self.draw3DObject(self.plant.pLeaf.stipuleTdoParams.object3D, scale, self.plant.pLeaf.stipuleTdoParams.faceColor, self.plant.pLeaf.stipuleTdoParams.backfaceColor, kExportPartLeafStipule)
        turtle.pop()

    def DrawLeafOrLeaflet(self, aScale):
        #Draw leaf only. If seedling leaf (on first phytomer), draw seedling leaf 3D object and colors instead.
        #    Wilt leaf according to water stress and age.
        turtle = self.plant.turtle
        if (turtle == None):
            return
        if self.isSeedlingLeaf:
            turtle.setLineWidth(1.0)
            useFaceColor = self.plant.pSeedlingLeaf.leafTdoParams.faceColor
            useBackfaceColor = self.plant.pSeedlingLeaf.leafTdoParams.backfaceColor
        else:
            turtle.setLineWidth(1.0)
            useFaceColor = self.plant.pLeaf.leafTdoParams.faceColor
            useBackfaceColor = self.plant.pLeaf.leafTdoParams.backfaceColor
        if self.isSeedlingLeaf:
            #this aligns the 3D object as stored in the file to the way it should draw on the plant
            # turtle.RotateX(64)  // flip over; in 3D designer you design the leaf from the underside
            #rotateAngle := self.angleWithSway(plant.pLeaf.object3DXRotationBeforeDraw * 256 / 360);
            #turtle.rotateX(rotateAngle);
            # no longer doing this because default X rotation is 90 degrees
            turtle.rotateX(self.angleWithSway(self.plant.pSeedlingLeaf.leafTdoParams.xRotationBeforeDraw))
            turtle.rotateY(self.angleWithSway(self.plant.pSeedlingLeaf.leafTdoParams.yRotationBeforeDraw))
            turtle.rotateZ(self.angleWithSway(self.plant.pSeedlingLeaf.leafTdoParams.zRotationBeforeDraw))
        else:
            turtle.rotateX(self.angleWithSway(self.plant.pLeaf.leafTdoParams.xRotationBeforeDraw))
            turtle.rotateY(self.angleWithSway(self.plant.pLeaf.leafTdoParams.yRotationBeforeDraw))
            turtle.rotateZ(self.angleWithSway(self.plant.pLeaf.leafTdoParams.zRotationBeforeDraw))
        #pull leaf up to plane of petiole (is perpendicular)
        turtle.rotateZ(-64)
        self.wiltLeaf()
        if self.isSeedlingLeaf:
            tdo = self.plant.pSeedlingLeaf.leafTdoParams.object3D
        else:
            tdo = self.plant.pLeaf.leafTdoParams.object3D
        if tdo != None:
            self.draw3DObject(tdo, aScale, useFaceColor, useBackfaceColor, kExportPartLeaf)

    def drawCompoundLeafPinnate(self):
        #Draw compound leaf. Use recursion structure we used to use for whole plant, with no branching.
        #    Leaflets decrease in size as you move up the leaf, simulating a gradual appearance of leaflets.
        #    Note that seedling leaves are never compound.
        turtle = self.plant.turtle
        if turtle == None:
            return
        if self.plant.pLeaf.compoundNumLeaflets <= 0:
            return
        # wnats plus one in original source
        for i in range(self.plant.pLeaf.compoundNumLeaflets, 0, -1):
            if (self.plant.pLeaf.compoundPinnateLeafletArrangement == kArrangementOpposite):
                if (i != 1) and (i % 2 == 1):
                    # v2 added opposite leaflets
                    self.drawCompoundLeafInternode(i)
            elif (i != 1):
                self.drawCompoundLeafInternode(i)
            turtle.push()
            scale = self.propFullSize * self.plant.pLeaf.leafTdoParams.scaleAtFullSize / 100.0
            self.DrawCompoundLeafPetioletCount(scale, i)
            self.DrawLeafOrLeaflet(scale)
            turtle.pop()

    def drawCompoundLeafInternode(self, count):
        #Draw internode of leaflet (portion of rachis). This is almost identical to drawing the petiole, etc,
        #   but a bit of random drift is included to make the compound leaf look more single.
        length = self.plant.pLeaf.petioleLengthAtOptimalBiomass_mm * self.propFullSize * self.plant.pLeaf.compoundRachisToPetioleRatio / 100.0
        width = self.plant.pLeaf.petioleWidthAtOptimalBiomass_mm * self.propFullSize
        # v1.6b3
        angleZ = self.compoundLeafAngleWithSway(self.bendAngleForCompoundLeaf(count), count)
        angleY = self.compoundLeafAngleWithSway(0, count)
        self.drawStemSegment(length, width, angleZ, angleY, self.plant.pLeaf.petioleColor, kDontTaper, kExportPartPetiole, kDontUseAmendment)

    # v1.6b3
    def bendAngleForCompoundLeaf(self, count):
        result = 0
        if self.plant == None:
            return result
        difference = abs(self.plant.pLeaf.compoundCurveAngleAtFullSize - self.plant.pLeaf.compoundCurveAngleAtStart)
        leafletNumberEffect = 0.75 + 0.25 * PS_math.safedivExcept(count, self.plant.pLeaf.compoundNumLeaflets - 1, 0)
        propFullSizeThisLeaflet = max(0.0, min(1.0, (0.25 + 0.75 * self.propFullSize) * leafletNumberEffect))
        if self.plant.pLeaf.compoundCurveAngleAtFullSize > self.plant.pLeaf.compoundCurveAngleAtStart:
            result = self.plant.pLeaf.compoundCurveAngleAtStart + difference * propFullSizeThisLeaflet
        else:
            result = self.plant.pLeaf.compoundCurveAngleAtStart - difference * propFullSizeThisLeaflet
        return result

    def DrawCompoundLeafPetioletCount(self, scale, aCount):
        #Draw petiolet, which is the leaflet stem coming off the compound leaf rachis.
        length = scale * self.plant.pLeaf.petioleLengthAtOptimalBiomass_mm * self.propFullSize
        width = scale * self.plant.pLeaf.petioleWidthAtOptimalBiomass_mm * self.propFullSize
        if (aCount == 1):
            angle = 0
        else:
            if (PS_math.odd(aCount)):
                angle = 32
            else:
                angle = -32
        angle = self.compoundLeafAngleWithSway(angle, aCount)
        self.drawStemSegment(length, width, 0, angle, self.plant.pLeaf.petioleColor, self.plant.pLeaf.petioleTaperIndex, kExportPartPetiole, kDontUseAmendment)

    def compoundLeafAngleWithSway(self, angle, count):
        result = angle
        if self.plant == None:
            return result
        if count < 0:
            count = 0
        count = count % kNumCompoundLeafRandomSwayIndexes
        randomNumber = self.compoundLeafRandomSwayIndexes[count]
        result = angle + ((randomNumber - 0.5) * self.plant.pGeneral.randomSway)
        return result

    def drawCompoundLeafPalmate(self):
        #Draw palmate compound leaf. Use recursion structure we used to use for whole plant, with no branching.
        #    In a palmate leaf, leaflets increase in size as you move toward the middle of the leaf.
        #    Note that seedling leaves are never compound.
        turtle = self.plant.turtle
        if (turtle == None):
            return
        angleOne = PS_math.safedivExcept(64, self.plant.pLeaf.compoundNumLeaflets, 0)
        if self.plant.pLeaf.compoundNumLeaflets > 0:
            for i in range(self.plant.pLeaf.compoundNumLeaflets, 0, -1):
                turtle.push()
                if (i == 1):
                    angle = 0
                elif (PS_math.odd(i)):
                    angle = angleOne * i * -1
                else:
                    angle = angleOne * i * 1
                length = self.plant.pLeaf.petioleLengthAtOptimalBiomass_mm * self.propFullSize * self.plant.pLeaf.compoundRachisToPetioleRatio / 100.0
                width = self.plant.pLeaf.petioleWidthAtOptimalBiomass_mm * self.propFullSize
                self.drawStemSegment(length, width, 0, angle, self.plant.pLeaf.petioleColor, self.plant.pLeaf.petioleTaperIndex, kExportPartPetiole, kDontUseAmendment)
                scale = self.propFullSize * self.plant.pLeaf.leafTdoParams.scaleAtFullSize / 100.0
                #scale := safedivExcept(scale, plant.pLeaf.compoundNumLeaflets, 0);
                self.DrawLeafOrLeaflet(scale)
                turtle.pop()

    def report(self):
        PS_part.PdPlantPart.report(self)
        #debugPrint('leaf, age %d biomass %f' % (age, liveBiomass_pctMPB))
        #DebugForm.printNested(plant.turtle.stackSize, 'leaf, age %d' % (age))

    def partType(self):
        result = kPartTypeLeaf
        return result

    def classAndVersionInformation(self, cvir):
        cvir.classNumber = uclasses.kPdLeaf
        cvir.versionNumber = 0
        cvir.additionNumber = 0

    def streamDataWithFiler(self, filer, cvir):
        PS_part.PdPlantPart.streamDataWithFiler(self, filer, cvir)
        self.sCurveParams = filer.streamBytes(self.sCurveParams, FIX_sizeof(self.sCurveParams))
        self.propFullSize = filer.streamSingle(self.propFullSize)
        self.biomassAtCreation_pctMPB = filer.streamSingle(self.biomassAtCreation_pctMPB)
        self.isSeedlingLeaf = filer.streamBoolean(self.isSeedlingLeaf)
