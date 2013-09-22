### PS_fruit
### - in growth cycle, calculates when fruit happen
### - Dependencies:
###      - PS_part for class, funcs
###      - PS_travers for linearGrowthResult
###      - PS_math for safediv
###      - math for math.floor

from PS_common import *
from PS_constants import *
import PS_part # inheritance and a couple of functions like: next Day
import PS_math
import PS_travers
import math # only uses math.floor


# const
kDrawFlowerAsOpening = True
kDontDrawFlowerAsOpening = False
kLine = True
kNotLine = False

# const
kDrawTDOOpen = True
kDrawTDOClosed = False

#  kBud = 0; kPistil = 1; kStamens = 2; kFirstPetals = 3; kSecondPetals = 4; kThirdPetals = 5; kSepals = 6;
class PdFlowerFruit(PS_part.PdPlantPart):
    def __init__(self):
        super(PdFlowerFruit, self).__init__()
        #PS_part.PdPlantPart.__init__(self)
        self.propFullSize = 0.0
        self.stage = 0
        self.hasBeenDrawn = False
        self.daysAccumulatingFruitBiomass = 0L
        self.daysOpen = 0L

    def initializeGender(self, aPlant, aGender):
        self.initialize(aPlant)
        self.gender = aGender
        self.propFullSize = 0.0
        self.liveBiomass_pctMPB = 0.0
        self.deadBiomass_pctMPB = 0.0
        self.biomassDemand_pctMPB = 0.0
        self.stage = kStageFlowerBud
        self.hasBeenDrawn = False

    def getName(self):
        result = "flower/fruit"
        return result

    def nextDay(self):
        if self.hasFallenOff:
            return
        try:
            PS_part.PdPlantPart.nextDay(self)
            if self.stage == kStageFlowerBud:
                if ((self.liveBiomass_pctMPB >= self.plant.pFlower[self.gender].minFractionOfOptimalBiomassToOpenFlower_frn * self.plant.pFlower[self.gender].optimalBiomass_pctMPB) or (self.age > self.plant.pFlower[self.gender].maxDaysToGrowIfOverMinFraction)) and (self.age > self.plant.pFlower[self.gender].minDaysToOpenFlower):
                    #if over required fraction of optimal or over max days to grow, open bud
                    self.stage = kStageOpenFlower
                    self.daysOpen = 0
            elif self.stage == kStageOpenFlower:
                #if over optimal or over min fraction to create fruit and over max days to grow, set fruit
                self.daysOpen += 1
                if self.daysOpen > self.plant.pFlower[self.gender].daysBeforeDrop:
                    self.hasFallenOff = True
                elif self.gender != kGenderMale:
                    if self.age > self.plant.pFlower[self.gender].minDaysBeforeSettingFruit:
                        # limit on time to set fruit (as opposed to grow) if want to keep flowers on plant longer
                        # upper limit on growth; must be at least as old as minDaysToGrow unless there is optimal biomass
                        minDaysWithOptimalBiomass = (self.age > self.plant.pFlower[self.gender].minDaysToGrow) and (self.liveBiomass_pctMPB >= self.plant.pFlower[self.gender].optimalBiomass_pctMPB)
                        # lower limit on growth; if don't have enough to make fruit, give up after max days and make anyway
                        biomassToMakeFruit_pctMPB = self.plant.pFlower[self.gender].minFractionOfOptimalBiomassToCreateFruit_frn * self.plant.pFlower[self.gender].optimalBiomass_pctMPB
                        maxDaysWithMinFraction = (self.age > self.plant.pFlower[self.gender].maxDaysToGrowIfOverMinFraction) or (self.liveBiomass_pctMPB >= biomassToMakeFruit_pctMPB)
                        if maxDaysWithMinFraction or minDaysWithOptimalBiomass:
                            self.stage = kStageUnripeFruit
                            self.daysAccumulatingFruitBiomass = 0
                            # flower biomass drops off, 50% goes into developing fruit (ovary)
                            # choice of 50% is arbitrary - could be parameter in future depending on size of flower parts/ovary
                            anthesisLoss_pctMPB = self.liveBiomass_pctMPB * 0.5
                            self.liveBiomass_pctMPB = self.liveBiomass_pctMPB - anthesisLoss_pctMPB
                            self.deadBiomass_pctMPB = self.deadBiomass_pctMPB + anthesisLoss_pctMPB
                            self.propFullSize = (min(1.0, PS_math.safedivExcept(self.totalBiomass_pctMPB(), self.plant.pFruit.optimalBiomass_pctMPB, 0.0)))
            elif self.stage == kStageUnripeFruit:
                if (self.stage == kStageUnripeFruit) and (self.daysAccumulatingFruitBiomass >= self.plant.pFruit.daysToRipen):
                    self.stage = kStageRipeFruit
                self.daysAccumulatingFruitBiomass += 1
            elif self.stage == kStageRipeFruit:
                if (self.stage == kStageUnripeFruit) and (self.daysAccumulatingFruitBiomass >= self.plant.pFruit.daysToRipen):
                    self.stage = kStageRipeFruit
                self.daysAccumulatingFruitBiomass += 1
        except Exception, e:
            # PDF PORT TEMP ADDED RAISE FOR TESTING
            raise
            usupport.messageForExceptionType(e, "PdFlowerFruit.nextDay")

    def traverseActivity(self, mode, traverserProxy):
        PS_part.PdPlantPart.traverseActivity(self, mode, traverserProxy)
        traverser = traverserProxy
        if traverser == None:
            return
        if self.hasFallenOff and (mode != kActivityStream) and (mode != kActivityFree) and (mode != kActivityGatherStatistics):
            return
        try:
            if mode == kActivityNone:
                pass
            elif mode == kActivityNextDay:
                self.nextDay()
            elif mode == kActivityDemandVegetative:
                pass
            elif mode == kActivityDemandReproductive:
                if self.stage == kStageFlowerBud:
                    # has no vegetative demand
                    # accum. biomass for flower
                    self.biomassDemand_pctMPB = PS_travers.linearGrowthResult(self.liveBiomass_pctMPB, self.plant.pFlower[self.gender].optimalBiomass_pctMPB, self.plant.pFlower[self.gender].minDaysToGrow)
                    traverser.total = traverser.total + self.biomassDemand_pctMPB
                elif self.stage == kStageOpenFlower:
                    # has no vegetative demand
                    # accum. biomass for flower
                    self.biomassDemand_pctMPB = PS_travers.linearGrowthResult(self.liveBiomass_pctMPB, self.plant.pFlower[self.gender].optimalBiomass_pctMPB, self.plant.pFlower[self.gender].minDaysToGrow)
                    traverser.total = traverser.total + self.biomassDemand_pctMPB
                elif self.stage == kStageUnripeFruit:
                    if self.daysAccumulatingFruitBiomass > self.plant.pFruit.maxDaysToGrow:
                        # accum. biomass for fruit
                        self.biomassDemand_pctMPB = 0.0
                    else:
                        fractionOfMaxAge_frn = PS_math.safedivExcept(self.daysAccumulatingFruitBiomass + 1, self.plant.pFruit.maxDaysToGrow, 0.0)
                        newPropFullSize = max(0.0, min(1.0, PS_math.scurve(fractionOfMaxAge_frn, self.plant.pFruit.sCurveParams.c1, self.plant.pFruit.sCurveParams.c2)))
                        newOptimalBiomass_pctMPB = newPropFullSize * self.plant.pFruit.optimalBiomass_pctMPB
                        self.biomassDemand_pctMPB = PS_travers.linearGrowthResult(self.liveBiomass_pctMPB, newOptimalBiomass_pctMPB, 1)
                        traverser.total = traverser.total + self.biomassDemand_pctMPB
                elif self.stage == kStageRipeFruit:
                    if self.daysAccumulatingFruitBiomass > self.plant.pFruit.maxDaysToGrow:
                        # accum. biomass for fruit
                        self.biomassDemand_pctMPB = 0.0
                    else:
                        fractionOfMaxAge_frn = PS_math.safedivExcept(self.daysAccumulatingFruitBiomass + 1, self.plant.pFruit.maxDaysToGrow, 0.0)
                        newPropFullSize = max(0.0, min(1.0, PS_math.scurve(fractionOfMaxAge_frn, self.plant.pFruit.sCurveParams.c1, self.plant.pFruit.sCurveParams.c2)))
                        newOptimalBiomass_pctMPB = newPropFullSize * self.plant.pFruit.optimalBiomass_pctMPB
                        self.biomassDemand_pctMPB = PS_travers.linearGrowthResult(self.liveBiomass_pctMPB, newOptimalBiomass_pctMPB, 1)
                        traverser.total = traverser.total + self.biomassDemand_pctMPB
            elif mode == kActivityGrowVegetative:
                pass
            elif mode == kActivityGrowReproductive:
                # cannot grow vegetatively
                #Allocate portion of total new biomass based on this demand over total demand.
                newBiomass_pctMPB = self.biomassDemand_pctMPB * traverser.fractionOfPotentialBiomass
                self.liveBiomass_pctMPB = self.liveBiomass_pctMPB + newBiomass_pctMPB
                if self.stage == kStageFlowerBud:
                    self.propFullSize = (min(1.0, PS_math.safedivExcept(self.totalBiomass_pctMPB(), self.plant.pFlower[self.gender].optimalBiomass_pctMPB, 0.0)))
                elif self.stage == kStageOpenFlower:
                    self.propFullSize = (min(1.0, PS_math.safedivExcept(self.totalBiomass_pctMPB(), self.plant.pFlower[self.gender].optimalBiomass_pctMPB, 0.0)))
                elif self.stage == kStageUnripeFruit:
                    self.propFullSize = (min(1.0, PS_math.safedivExcept(self.totalBiomass_pctMPB(), self.plant.pFruit.optimalBiomass_pctMPB, 0.0)))
                elif self.stage == kStageRipeFruit:
                    self.propFullSize = (min(1.0, PS_math.safedivExcept(self.totalBiomass_pctMPB(), self.plant.pFruit.optimalBiomass_pctMPB, 0.0)))
            elif mode == kActivityStartReproduction:
                pass
            elif mode == kActivityFindPlantPartAtPosition:
                if PS_math.pointsAreCloseEnough(traverser.point, self.position()):
                    # can't switch because has no vegetative mode
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
                pass
            elif mode == kActivityRemoveVegetativeBiomass:
                pass
            elif mode == kActivityReproductiveBiomassThatCanBeRemoved:
                # inflorescence should handle telling flowers to draw
                #streaming called by inflorescence
                # free called by inflorescence
                # none
                # do nothing
                traverser.total = traverser.total + self.liveBiomass_pctMPB
            elif mode == kActivityRemoveReproductiveBiomass:
                if self.liveBiomass_pctMPB <= 0.0:
                    return
                biomassToRemove_pctMPB = self.liveBiomass_pctMPB * traverser.fractionOfPotentialBiomass
                self.liveBiomass_pctMPB = self.liveBiomass_pctMPB - biomassToRemove_pctMPB
                self.deadBiomass_pctMPB = self.deadBiomass_pctMPB + biomassToRemove_pctMPB
                if self.liveBiomass_pctMPB <= 0.0:
                    if (self.stage == kStageUnripeFruit) or (self.stage == kStageRipeFruit):
                        self.hasFallenOff = True
            elif mode == kActivityGatherStatistics:
                if self.stage == kStageFlowerBud:
                    if self.gender == kGenderMale:
                        if self.hasFallenOff:
                            self.addToStatistics(traverser.statistics, kStatisticsPartTypeFallenFlower)
                        else:
                            self.addToStatistics(traverser.statistics, kStatisticsPartTypeMaleFlowerBud)
                    else:
                        if self.hasFallenOff:
                            self.addToStatistics(traverser.statistics, kStatisticsPartTypeFallenFlower)
                        else:
                            self.addToStatistics(traverser.statistics, kStatisticsPartTypeFemaleFlowerBud)
                elif self.stage == kStageOpenFlower:
                    if self.gender == kGenderMale:
                        if self.hasFallenOff:
                            self.addToStatistics(traverser.statistics, kStatisticsPartTypeFallenFlower)
                        else:
                            self.addToStatistics(traverser.statistics, kStatisticsPartTypeMaleFlower)
                    else:
                        if self.hasFallenOff:
                            self.addToStatistics(traverser.statistics, kStatisticsPartTypeFallenFlower)
                        else:
                            self.addToStatistics(traverser.statistics, kStatisticsPartTypeFemaleFlower)
                elif self.stage == kStageUnripeFruit:
                    if self.hasFallenOff:
                        self.addToStatistics(traverser.statistics, kStatisticsPartTypeFallenFruit)
                    else:
                        self.addToStatistics(traverser.statistics, kStatisticsPartTypeUnripeFruit)
                elif self.stage == kStageRipeFruit:
                    if self.hasFallenOff:
                        self.addToStatistics(traverser.statistics, kStatisticsPartTypeFallenFruit)
                    else:
                        self.addToStatistics(traverser.statistics, kStatisticsPartTypeFruit)
                else :
                    raise GeneralException.create("Problem: Invalid fruit stage in method PdFlowerFruit.traverseActivity.")
                self.addToStatistics(traverser.statistics, kStatisticsPartTypeAllReproductive)
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
                raise GeneralException.create("Problem: Unhandled mode for plant draw activity in method PdFlowerFruit.traverseActivity.")
        except Exception, e:
            #PDF PORT TEMP FOR TESTING
            raise
            usupport.messageForExceptionType(e, "PdFlowerFruit.traverseActivity")

    def report(self):
        PS_part.PdPlantPart.report(self)
        # DebugPrint(' flower/fruit, age %d biomas %f' % (age, self.liveBiomass_pctMPB))

    def dxfIndexForFloralLayerType(self, aType, line):
        result = 0
        if aType == kBud:
            result = kExportPartFlowerBudFemale
        elif aType == kPistils:
            if line:
                result = kExportPartStyleFemale
            else:
                result = kExportPartStigmaFemale
        elif aType == kStamens:
            if line:
                result = kExportPartFilamentFemale
            else:
                result = kExportPartAntherFemale
        elif aType == kFirstPetals:
            result = kExportPartFirstPetalsFemale
        elif aType == kSecondPetals:
            result = kExportPartSecondPetalsFemale
        elif aType == kThirdPetals:
            result = kExportPartThirdPetalsFemale
        elif aType == kFourthPetals:
            result = kExportPartFourthPetalsFemale
        elif aType == kFifthPetals:
            result = kExportPartFifthPetalsFemale
        elif aType == kSepals:
            result = kExportPartSepalsFemale
        return result

    def draw(self):
        if (self.plant.turtle == None):
            return
        turtle = self.plant.turtle
        self.boundsRect = Rect(0, 0, 0, 0)
        if self.hasFallenOff:
            return
        turtle.push()
        self.determineAmendmentAndAlsoForChildrenIfAny()
        if self.hiddenByAmendment():
            turtle.pop()
            return
        else:
            self.applyAmendmentRotations()
        try:
            if self.stage == kStageFlowerBud:
                if self.plant.pFlower[self.gender].budDrawingOption == kDrawNoBud:
                    # kDrawNoBud = 0; kDrawSingleTdoBud = 1; kDrawOpeningFlower = 2;
                    return
                elif self.plant.pFlower[self.gender].budDrawingOption == kDrawSingleTdoBud:
                    scale = ((self.plant.pFlower[self.gender].tdoParams[kBud].scaleAtFullSize / 100.0) * self.propFullSize)
                    turtle.rotateX(self.angleWithSway(self.plant.pFlower[self.gender].tdoParams[kBud].xRotationBeforeDraw))
                    turtle.rotateY(self.angleWithSway(self.plant.pFlower[self.gender].tdoParams[kBud].yRotationBeforeDraw))
                    turtle.rotateZ(self.angleWithSway(self.plant.pFlower[self.gender].tdoParams[kBud].zRotationBeforeDraw))
                    self.drawCircleOfTdos(self.plant.pFlower[self.gender].tdoParams[kBud].object3D, self.plant.pFlower[self.gender].tdoParams[kBud].faceColor, self.plant.pFlower[self.gender].tdoParams[kBud].backfaceColor, self.plant.pFlower[self.gender].tdoParams[kBud].pullBackAngle, scale, self.plant.pFlower[self.gender].tdoParams[kBud].repetitions, self.plant.pFlower[self.gender].tdoParams[kBud].radiallyArranged, kDrawTDOClosed, kExportPartFlowerBudFemale)
                elif self.plant.pFlower[self.gender].budDrawingOption == kDrawOpeningFlower:
                    self.drawFlower(kDrawFlowerAsOpening)
            elif self.stage == kStageOpenFlower:
                self.drawFlower(kDontDrawFlowerAsOpening)
            elif self.stage == kStageUnripeFruit:
                # ripe color is regular color; alternate color is unripe color
                scale = ((self.plant.pFruit.tdoParams.scaleAtFullSize / 100.0) * self.propFullSize)
                turtle.rotateX(self.angleWithSway(self.plant.pFruit.tdoParams.xRotationBeforeDraw))
                turtle.rotateY(self.angleWithSway(self.plant.pFruit.tdoParams.yRotationBeforeDraw))
                turtle.rotateZ(self.angleWithSway(self.plant.pFruit.tdoParams.zRotationBeforeDraw))
                self.drawCircleOfTdos(self.plant.pFruit.tdoParams.object3D, self.plant.pFruit.tdoParams.alternateFaceColor, self.plant.pFruit.tdoParams.alternateBackfaceColor, self.plant.pFruit.tdoParams.pullBackAngle, scale, self.plant.pFruit.tdoParams.repetitions, self.plant.pFruit.tdoParams.radiallyArranged, kDrawTDOClosed, kExportPartUnripeFruit)
            elif self.stage == kStageRipeFruit:
                scale = ((self.plant.pFruit.tdoParams.scaleAtFullSize / 100.0) * self.propFullSize)
                turtle.rotateX(self.angleWithSway(self.plant.pFruit.tdoParams.xRotationBeforeDraw))
                turtle.rotateY(self.angleWithSway(self.plant.pFruit.tdoParams.yRotationBeforeDraw))
                turtle.rotateZ(self.angleWithSway(self.plant.pFruit.tdoParams.zRotationBeforeDraw))
                self.drawCircleOfTdos(self.plant.pFruit.tdoParams.object3D, self.plant.pFruit.tdoParams.faceColor, self.plant.pFruit.tdoParams.backfaceColor, self.plant.pFruit.tdoParams.pullBackAngle, scale, self.plant.pFruit.tdoParams.repetitions, self.plant.pFruit.tdoParams.radiallyArranged, kDrawTDOClosed, kExportPartRipeFruit)
            self.hasBeenDrawn = True
            turtle.pop()
        except Exception, e:
            # PDF PORT ADDED RAISE FOR TESTIGN
            raise
            usupport.messageForExceptionType(e, "PdFlowerFruit.draw")

    def drawFlower(self, drawAsOpening):
        if (self.plant.turtle == None):
            return
        turtle = self.plant.turtle
        self.drawPistilsAndStamens(drawAsOpening)
        for layerType in range(kFirstPetals, kSepals + 1):
            turtle.push()
            scale = ((self.plant.pFlower[self.gender].tdoParams[layerType].scaleAtFullSize / 100.0) * self.propFullSize)
            angle = self.angleWithSway(self.plant.pFlower[self.gender].tdoParams[layerType].pullBackAngle)
            if drawAsOpening:
                angle = angle * self.propFullSize * 2
                if angle > self.plant.pFlower[self.gender].tdoParams[layerType].pullBackAngle:
                    angle = self.plant.pFlower[self.gender].tdoParams[layerType].pullBackAngle
            turtle.rotateX(self.angleWithSway(self.plant.pFlower[self.gender].tdoParams[layerType].xRotationBeforeDraw))
            turtle.rotateY(self.angleWithSway(self.plant.pFlower[self.gender].tdoParams[layerType].yRotationBeforeDraw))
            turtle.rotateZ(self.angleWithSway(self.plant.pFlower[self.gender].tdoParams[layerType].zRotationBeforeDraw))
            self.drawCircleOfTdos(self.plant.pFlower[self.gender].tdoParams[layerType].object3D, self.plant.pFlower[self.gender].tdoParams[layerType].faceColor, self.plant.pFlower[self.gender].tdoParams[layerType].backfaceColor, angle, scale, self.plant.pFlower[self.gender].tdoParams[layerType].repetitions, self.plant.pFlower[self.gender].tdoParams[layerType].radiallyArranged, kDrawTDOOpen, self.dxfIndexForFloralLayerType(layerType, kNotLine))
            turtle.pop()

    def drawPistilsAndStamens(self, drawAsOpening):
        if (self.plant.turtle == None):
            return
        turtle = self.plant.turtle
        turtle.push()
        if (self.plant.pFlower[self.gender].numPistils > 0):
            if ((self.plant.pFlower[self.gender].styleLength_mm > 0) and (self.plant.pFlower[self.gender].styleWidth_mm > 0)) or (self.plant.pFlower[self.gender].tdoParams[kPistils].scaleAtFullSize > 0):
                turtle.ifExporting_startNestedGroupOfPlantParts("pistils", "Pistils", kNestingTypeFloralLayers)
            turnPortion = 256 / self.plant.pFlower[self.gender].numPistils
            leftOverDegrees = 256 - turnPortion * self.plant.pFlower[self.gender].numPistils
            if leftOverDegrees > 0:
                addition = PS_math.safedivExcept(leftOverDegrees, self.plant.pFlower[self.gender].numPistils, 0)
            else:
                addition = 0
            carryOver = 0
            for i in range(0, self.plant.pFlower[self.gender].numPistils):
                turtle.push()
                if (self.plant.pFlower[self.gender].styleLength_mm > 0) and (self.plant.pFlower[self.gender].styleWidth_mm > 0):
                    length = max(0.0, self.propFullSize * self.plant.pFlower[self.gender].styleLength_mm)
                    width = max(0.0, self.propFullSize * self.plant.pFlower[self.gender].styleWidth_mm)
                    angle = self.angleWithSway(self.plant.pFlower[self.gender].tdoParams[kPistils].pullBackAngle)
                    if drawAsOpening:
                        angle = angle * self.propFullSize
                    self.drawStemSegment(length, width, angle, 0, self.plant.pFlower[self.gender].styleColor, self.plant.pFlower[self.gender].styleTaperIndex, self.dxfIndexForFloralLayerType(kPistils, kLine), kDontUseAmendment)
                scale = ((self.plant.pFlower[self.gender].tdoParams[kPistils].scaleAtFullSize / 100.0) * self.propFullSize)
                turtle.rotateX(self.angleWithSway(self.plant.pFlower[self.gender].tdoParams[kPistils].xRotationBeforeDraw))
                turtle.rotateY(self.angleWithSway(self.plant.pFlower[self.gender].tdoParams[kPistils].yRotationBeforeDraw))
                turtle.rotateZ(self.angleWithSway(self.plant.pFlower[self.gender].tdoParams[kPistils].zRotationBeforeDraw))
                self.drawCircleOfTdos(self.plant.pFlower[self.gender].tdoParams[kPistils].object3D, self.plant.pFlower[self.gender].tdoParams[kPistils].faceColor, self.plant.pFlower[self.gender].tdoParams[kPistils].backfaceColor, 0, scale, self.plant.pFlower[self.gender].tdoParams[kPistils].repetitions, self.plant.pFlower[self.gender].tdoParams[kPistils].radiallyArranged, kDrawTDOOpen, self.dxfIndexForFloralLayerType(kPistils, kNotLine))
                turtle.pop()
                addThisTime = math.floor(addition + carryOver)
                carryOver = carryOver + addition - addThisTime
                if carryOver < 0:
                    carryOver = 0
                turtle.rotateX(turnPortion + addThisTime)
            if ((self.plant.pFlower[self.gender].styleLength_mm > 0) and (self.plant.pFlower[self.gender].styleWidth_mm > 0)) or (self.plant.pFlower[self.gender].tdoParams[kPistils].scaleAtFullSize > 0):
                turtle.ifExporting_endNestedGroupOfPlantParts(kNestingTypeFloralLayers)
        turtle.pop()
        # stamens
        turtle.push()
        if self.plant.pFlower[self.gender].numStamens > 0:
            if ((self.plant.pFlower[self.gender].filamentLength_mm > 0) and (self.plant.pFlower[self.gender].filamentWidth_mm > 0)) or (self.plant.pFlower[self.gender].tdoParams[kStamens].scaleAtFullSize > 0):
                if self.gender == kGenderFemale:
                    turtle.ifExporting_startNestedGroupOfPlantParts("primary stamens", "1Stamens", kNestingTypeFloralLayers)
                else:
                    turtle.ifExporting_startNestedGroupOfPlantParts("secondary stamens", "2Stamens", kNestingTypeFloralLayers)
            turnPortion = 256 / self.plant.pFlower[self.gender].numStamens
            leftOverDegrees = 256 - turnPortion * self.plant.pFlower[self.gender].numStamens
            if leftOverDegrees > 0:
                addition = PS_math.safedivExcept(leftOverDegrees, self.plant.pFlower[self.gender].numStamens, 0)
            else:
                addition = 0
            carryOver = 0
            for i in range(0, self.plant.pFlower[self.gender].numStamens):
                turtle.push()
                if (self.plant.pFlower[self.gender].filamentLength_mm > 0) and (self.plant.pFlower[self.gender].filamentWidth_mm > 0):
                    length = max(0.0, self.propFullSize * self.plant.pFlower[self.gender].filamentLength_mm)
                    width = max(0.0, self.propFullSize * self.plant.pFlower[self.gender].filamentWidth_mm)
                    angle = self.angleWithSway(self.plant.pFlower[self.gender].tdoParams[kStamens].pullBackAngle)
                    if drawAsOpening:
                        angle = angle * self.propFullSize
                    self.drawStemSegment(length, width, angle, 0, self.plant.pFlower[self.gender].filamentColor, self.plant.pFlower[self.gender].filamentTaperIndex, self.dxfIndexForFloralLayerType(kStamens, kLine), kDontUseAmendment)
                scale = ((self.plant.pFlower[self.gender].tdoParams[kStamens].scaleAtFullSize / 100.0) * self.propFullSize)
                turtle.rotateX(self.angleWithSway(self.plant.pFlower[self.gender].tdoParams[kStamens].xRotationBeforeDraw))
                turtle.rotateY(self.angleWithSway(self.plant.pFlower[self.gender].tdoParams[kStamens].yRotationBeforeDraw))
                turtle.rotateZ(self.angleWithSway(self.plant.pFlower[self.gender].tdoParams[kStamens].zRotationBeforeDraw))
                self.drawCircleOfTdos(self.plant.pFlower[self.gender].tdoParams[kStamens].object3D, self.plant.pFlower[self.gender].tdoParams[kStamens].faceColor, self.plant.pFlower[self.gender].tdoParams[kStamens].backfaceColor, 0, scale, self.plant.pFlower[self.gender].tdoParams[kStamens].repetitions, self.plant.pFlower[self.gender].tdoParams[kStamens].radiallyArranged, kDrawTDOOpen, self.dxfIndexForFloralLayerType(kStamens, kNotLine))
                turtle.pop()
                addThisTime = math.floor(addition + carryOver)
                carryOver = carryOver + addition - addThisTime
                if carryOver < 0:
                    carryOver = 0
                turtle.rotateX(turnPortion + addThisTime)
            if ((self.plant.pFlower[self.gender].filamentLength_mm > 0) and (self.plant.pFlower[self.gender].filamentWidth_mm > 0)) or (self.plant.pFlower[self.gender].tdoParams[kStamens].scaleAtFullSize > 0):
                turtle.ifExporting_endNestedGroupOfPlantParts(kNestingTypeFloralLayers)
        turtle.pop()

    def countPointsAndTrianglesFor3DExportAndAddToTraverserTotals(self, traverser):
        if traverser == None:
            return
        if self.propFullSize <= 0:
            return
        if self.hasFallenOff:
            return
        if self.stage == kStageFlowerBud:
            if self.plant.pFlower[self.gender].budDrawingOption == kDrawNoBud:
                pass
            elif self.plant.pFlower[self.gender].budDrawingOption == kDrawSingleTdoBud:
                if self.plant.pFlower[self.gender].tdoParams[kBud].scaleAtFullSize > 0:
                    traverser.total3DExportPointsIn3DObjects += self.plant.pFlower[self.gender].tdoParams[kBud].object3D.pointsInUse * self.plant.pFlower[self.gender].tdoParams[kBud].repetitions
                    traverser.total3DExportTrianglesIn3DObjects += len(self.plant.pFlower[self.gender].tdoParams[kBud].object3D.triangles) * self.plant.pFlower[self.gender].tdoParams[kBud].repetitions
                    self.addExportMaterial(traverser, kExportPartFlowerBudFemale, kExportPartFlowerBudMale)
            elif self.plant.pFlower[self.gender].budDrawingOption == kDrawOpeningFlower:
                self.addFloralPartsCountsToTraverser(traverser)
        elif self.stage == kStageOpenFlower:
            self.addFloralPartsCountsToTraverser(traverser)
        elif self.stage == kStageUnripeFruit:
            if self.plant.pFruit.tdoParams.scaleAtFullSize > 0:
                traverser.total3DExportPointsIn3DObjects += self.plant.pFruit.tdoParams.object3D.pointsInUse * self.plant.pFruit.tdoParams.repetitions
                traverser.total3DExportTrianglesIn3DObjects += len(self.plant.pFruit.tdoParams.object3D.triangles) * self.plant.pFruit.tdoParams.repetitions
                if self.stage == kStageUnripeFruit:
                    self.addExportMaterial(traverser, kExportPartUnripeFruit, -1)
                else:
                    self.addExportMaterial(traverser, kExportPartRipeFruit, -1)
        elif self.stage == kStageRipeFruit:
            if self.plant.pFruit.tdoParams.scaleAtFullSize > 0:
                traverser.total3DExportPointsIn3DObjects += self.plant.pFruit.tdoParams.object3D.pointsInUse * self.plant.pFruit.tdoParams.repetitions
                traverser.total3DExportTrianglesIn3DObjects += len(self.plant.pFruit.tdoParams.object3D.triangles) * self.plant.pFruit.tdoParams.repetitions
                if self.stage == kStageUnripeFruit:
                    self.addExportMaterial(traverser, kExportPartUnripeFruit, -1)
                else:
                    self.addExportMaterial(traverser, kExportPartRipeFruit, -1)
        # pedicel handled by inflorescence

    def addFloralPartsCountsToTraverser(self, traverser):
        for partType in range(kPistils, kSepals + 1):
            if self.plant.pFlower[self.gender].tdoParams[partType].scaleAtFullSize > 0:
                if partType == kPistils:
                    traverser.total3DExportPointsIn3DObjects += self.plant.pFlower[self.gender].tdoParams[partType].object3D.pointsInUse * self.plant.pFlower[self.gender].tdoParams[partType].repetitions * self.plant.pFlower[self.gender].numPistils
                    traverser.total3DExportTrianglesIn3DObjects += len(self.plant.pFlower[self.gender].tdoParams[partType].object3D.triangles) * self.plant.pFlower[self.gender].tdoParams[partType].repetitions * self.plant.pFlower[self.gender].numPistils
                    self.addExportMaterial(traverser, kExportPartStyleFemale, -1)
                    self.addExportMaterial(traverser, kExportPartStigmaFemale, -1)
                elif partType == kStamens:
                    traverser.total3DExportPointsIn3DObjects += self.plant.pFlower[self.gender].tdoParams[partType].object3D.pointsInUse * self.plant.pFlower[self.gender].tdoParams[partType].repetitions * self.plant.pFlower[self.gender].numStamens
                    traverser.total3DExportTrianglesIn3DObjects += len(self.plant.pFlower[self.gender].tdoParams[partType].object3D.triangles) * self.plant.pFlower[self.gender].tdoParams[partType].repetitions * self.plant.pFlower[self.gender].numStamens
                    self.addExportMaterial(traverser, kExportPartFilamentFemale, kExportPartFilamentMale)
                    self.addExportMaterial(traverser, kExportPartAntherFemale, kExportPartAntherMale)
                else:
                    traverser.total3DExportPointsIn3DObjects += self.plant.pFlower[self.gender].tdoParams[partType].object3D.pointsInUse * self.plant.pFlower[self.gender].tdoParams[partType].repetitions
                    traverser.total3DExportTrianglesIn3DObjects += len(self.plant.pFlower[self.gender].tdoParams[partType].object3D.triangles) * self.plant.pFlower[self.gender].tdoParams[partType].repetitions
                    if partType == kFirstPetals:
                        self.addExportMaterial(traverser, kExportPartFirstPetalsFemale, kExportPartFirstPetalsMale)
                    elif partType == kSecondPetals:
                        self.addExportMaterial(traverser, kExportPartSecondPetalsFemale, -1)
                    elif partType == kThirdPetals:
                        self.addExportMaterial(traverser, kExportPartThirdPetalsFemale, -1)
                    elif partType == kFourthPetals:
                        self.addExportMaterial(traverser, kExportPartFourthPetalsFemale, -1)
                    elif partType == kFifthPetals:
                        self.addExportMaterial(traverser, kExportPartFifthPetalsFemale, -1)
                    elif partType == kSepals:
                        self.addExportMaterial(traverser, kExportPartSepalsFemale, kExportPartSepalsMale)

    def triangleCountInFloralParts(self):
        result = 0
        for partType in range(kPistils, kSepals + 1):
            if self.plant.pFlower[self.gender].tdoParams[partType].scaleAtFullSize > 0:
                if partType == kPistils:
                    result = result + len(self.plant.pFlower[self.gender].tdoParams[partType].object3D.triangles) * self.plant.pFlower[self.gender].tdoParams[partType].repetitions * self.plant.pFlower[self.gender].numPistils
                elif partType == kStamens:
                    result = result + len(self.plant.pFlower[self.gender].tdoParams[partType].object3D.triangles) * self.plant.pFlower[self.gender].tdoParams[partType].repetitions * self.plant.pFlower[self.gender].numStamens
                else:
                    result = result + len(self.plant.pFlower[self.gender].tdoParams[partType].object3D.triangles) * self.plant.pFlower[self.gender].tdoParams[partType].repetitions
        return result

    def tdoToSortLinesWith(self):
        result = None
        if self.plant == None:
            return result
        if self.hasFallenOff:
            return result
        if self.stage == kStageFlowerBud:
            result = self.plant.pFlower[self.gender].tdoParams[kBud].object3D
        elif self.stage == kStageOpenFlower:
            result = self.plant.pFlower[self.gender].tdoParams[kFirstPetals].object3D
        elif self.stage == kStageUnripeFruit:
            result = self.plant.pFruit.tdoParams.object3D
        elif self.stage == kStageRipeFruit:
            result = self.plant.pFruit.tdoParams.object3D
        return result

    def drawCircleOfTdos(self, tdo, faceColor, backfaceColor, pullBackAngle, scale, numParts, partsArranged, open, dxfIndex):
        try:
            if (scale <= 0.0):
                # v1.3
                # v1.3
                return
            turtle = self.plant.turtle
            if (turtle == None):
                return
            turtle.push()
            minZ = 0
            if (partsArranged) and (numParts > 0):
                turtle.ifExporting_startPlantPart(self.longNameForDXFPartConsideringGenderEtc(dxfIndex), self.shortNameForDXFPartConsideringGenderEtc(dxfIndex))
                turnPortion = 256 / numParts
                leftOverDegrees = 256 - turnPortion * numParts
                if leftOverDegrees > 0:
                    addition = PS_math.safedivExcept(leftOverDegrees, numParts, 0)
                else:
                    addition = 0
                carryOver = 0
                for i in range(1, numParts + 1):
                    addThisTime = math.floor(addition + carryOver)
                    carryOver = carryOver + addition - addThisTime
                    if carryOver < 0:
                        carryOver = 0
                    turtle.rotateX(turnPortion + addThisTime)
                    turtle.push()
                    #aligns object as stored in the file to way should draw on plant
                    turtle.rotateZ(-64)
                    if open:
                        #pulls petal up to plane of stalk (is perpendicular)
                        turtle.rotateY(32)
                    turtle.rotateX(pullBackAngle)
                    if tdo != None:
                        self.draw3DObject(tdo, scale, faceColor, backfaceColor, dxfIndex)
                        if i == 1:
                            minZ = tdo.zForSorting
                        elif tdo.zForSorting < minZ:
                            minZ = tdo.zForSorting
                    turtle.pop()
                if tdo != None:
                    tdo.zForSorting = minZ
                turtle.ifExporting_endPlantPart()
            else:
                turtle.push()
                if (self.stage == kStageUnripeFruit) or (self.stage == kStageRipeFruit):
                    turtle.rotateZ(-64)
                else:
                    #pulls petal up to plane of stalk (is perpendicular)
                    turtle.rotateZ(-pullBackAngle)
                if tdo != None:
                    self.draw3DObject(tdo, scale, faceColor, backfaceColor, dxfIndex)
                turtle.pop()
            turtle.pop()
        except Exception, e:
            usupport.messageForExceptionType(e, "PdFlowerFruit.drawCircleOfTdos")

    def partType(self):
        return kPartTypeFlowerFruit

    def classAndVersionInformation(self, cvir):
        cvir.classNumber = uclasses.kPdFlowerFruit
        cvir.versionNumber = 0
        cvir.additionNumber = 0

    def streamDataWithFiler(self, filer, cvir):
        PS_part.PdPlantPart.streamDataWithFiler(self, filer, cvir)
        self.propFullSize = filer.streamSingle(self.propFullSize)
        self.stage = filer.streamSmallint(self.stage)
        self.hasBeenDrawn = filer.streamBoolean(self.hasBeenDrawn)
        self.daysAccumulatingFruitBiomass = filer.streamLongint(self.daysAccumulatingFruitBiomass)
        self.daysOpen = filer.streamLongint(self.daysOpen)

# cfk remember this
# ---------------------------------------------------------------------- wilting/falling down
#procedure PdFlowerFruit.dragDownFromWeight;
#  begin
#  end;
#procedure PdFlowerFruit.dragDownFromWeight;
#  var
#    fractionOfOptimalFruitWeight_frn: single;
#    angle: integer;
#  begin
#  if (plant.turtle = nil) then exit;
#  fractionOfOptimalFruitWeight_frn := safedivExcept(liveBiomass_pctMPB, plant.pFruit.optimalBiomass_pctMPB, 0.0);
#  angle := round(abs(plant.turtle.angleZ + 32) * fractionOfOptimalFruitWeight_frn
#      * min(1.0, max(0.0, 100 - plant.pFruit.stalkStrengthIndex) / 100.0));
#  angle := -angle;
#  if plant.turtle.angleZ > -32 then
#    angle := -angle;
#  plant.turtle.rotateZ(angle);
#  end;
