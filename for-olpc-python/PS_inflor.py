### PS_inflor
### - in growth cycle, calculates when fruit happen
### Dependencies:
###     - PS_part for class, func
###     - PS_travers for linearGrowthResult
###     - PS_fruit - only user of this
###     - PS_math for safediv, pointsAreCloseEnough
###     - PS_support for error message


#The inflorescence is very simple; it creates a specified number of flowers over a specified period
#  of days. Each inflorescence on the plant has the same number of flowers. Since an inflorescence is
#  created by a meristem which accumulates biomass, nothing stands in the way of the inflorescence
#  producing the flowers according to schedule.
#  This method must act differently for inflorescences that produce flowers slowly (over a greater
#  number of days than flowers) than for those that produce many flowers in a few days.
#  The inflorescence can create no flowers until it reaches a specified fraction of its optimal biomass.
#Survey flowers and return true if all flowers have been drawn (they know), false if any have not been
#   drawn. This is mostly so a branched inflorescence can know if there are any flowers left to place
#   on its branched structure.

# unit uinflor

from PS_common import *
from PS_constants import *
import ucollect
import PS_part
import PS_math
import PS_travers
import udomain
import PS_fruit # only place imports this
#import PS_3dexport
import PS_support

import math
import udebug



class PdInflorescence(PS_part.PdPlantPart):
    def __init__(self):
        super(PdInflorescence, self).__init__()
        #PS_part.PdPlantPart.__init__(self)
        # structure
        self.phytomerAttachedTo = None
        #
        self.flowers = ucollect.TListCollection()
        self.numFlowers = 0
        self.numFlowersEachDay = 0
        self.daysBetweenFlowerAppearances = 0
        self.daysSinceLastFlowerAppeared = 0
        self.daysSinceStartedMakingFlowers = 0
        self.isApical = False
        self.meristemThatCreatedMe = None
        self.fractionOfOptimalSizeWhenCreated = 0.0

    def getName(self):
        result = "inflorescence"
        return result

    def determineAmendmentAndAlsoForChildrenIfAny(self):
        PS_part.PdPlantPart.determineAmendmentAndAlsoForChildrenIfAny(self)
        if self.amendment != None:
            amendmentToPass = self.amendment
        else:
            amendmentToPass = self.parentAmendment
        if len(self.flowers) > 0:
            for flower in self.flowers:
                flower.parentAmendment = amendmentToPass

    def initializeGenderApicalOrAxillary(self, aPlant, aGender, initAsApical, fractionOfOptimalSize):
        try:
            self.initialize(aPlant)
            self.gender = aGender
            self.isApical = initAsApical
            self.daysSinceLastFlowerAppeared = 0
            self.daysSinceStartedMakingFlowers = 0
            self.fractionOfOptimalSizeWhenCreated = min(1.0, fractionOfOptimalSize)
            #The inflorescence must know whether it produces flowers slowly (over a greater number of days than flowers)
            #  or produces many flowers in a few days.
            daysToAllFlowers = self.plant.pInflor[self.gender].daysToAllFlowersCreated
            self.numFlowers = self.plant.pInflor[self.gender].numFlowersOnMainBranch + self.plant.pInflor[self.gender].numFlowersPerBranch * self.plant.pInflor[self.gender].numBranches
            self.daysBetweenFlowerAppearances = 0
            self.numFlowersEachDay = 0
            if self.numFlowers > 0:
                if self.numFlowers == 1:
                    self.numFlowersEachDay = 1
                elif self.numFlowers == daysToAllFlowers:
                    self.numFlowersEachDay = 1
                elif self.numFlowers > daysToAllFlowers:
                    self.numFlowersEachDay = int(PS_math.safedivExcept(1.0 * self.numFlowers, 1.0 * daysToAllFlowers, 0))
                else:
                    self.daysBetweenFlowerAppearances = int(PS_math.safedivExcept(1.0 * daysToAllFlowers, 1.0 * self.numFlowers, 0))
        except Exception, e:
            # PDF PORT TEMP RAISE FOR TESTING
            raise
            PS_support.messageForExceptionType(e, "PdInflorescence.InitializeGenderApicalOrAxillary")

    def optimalInitialBiomass_pctMPB(self, drawingPlant, gender):
        if (gender < 0) or (gender > 1):
            result = 0.0
        else:
            result = drawingPlant.pInflor[gender].optimalBiomass_pctMPB * drawingPlant.pInflor[gender].minFractionOfOptimalBiomassToCreateInflorescence_frn
        return result
    optimalInitialBiomass_pctMPB = classmethod(optimalInitialBiomass_pctMPB)

    def nextDay(self):
        ''' calc for flowers '''
        try:
            PS_part.PdPlantPart.nextDay(self) # age+1
            for flower in self.flowers:
                flower.nextDay()
            #if self.age < plant.pInflor[gender].maxDaysToGrow then
            biomassToMakeFlowers_pctMPB = self.plant.pInflor[self.gender].minFractionOfOptimalBiomassToMakeFlowers_frn * self.plant.pInflor[self.gender].optimalBiomass_pctMPB
            if self.liveBiomass_pctMPB >= biomassToMakeFlowers_pctMPB:
                self.daysSinceStartedMakingFlowers += 1
                if (len(self.flowers) <= 0) and (self.numFlowers > 0):
                    # make first flower on first day
                    self.createFlower()
                elif (len(self.flowers) < self.numFlowers):
                    if (self.daysBetweenFlowerAppearances > 0):
                        if (self.daysSinceLastFlowerAppeared >= self.daysBetweenFlowerAppearances):
                            self.createFlower()
                            self.daysSinceLastFlowerAppeared = 0
                        else:
                            self.daysSinceLastFlowerAppeared += 1
                    else:
                        numFlowersToCreateToday = min(self.numFlowersEachDay, self.numFlowers - len(self.flowers))
                        if numFlowersToCreateToday > 0:
                            for i in range(0, numFlowersToCreateToday):
                                self.createFlower()
                        self.daysSinceLastFlowerAppeared = 0
        except Exception, e:
            # PDF PORT TEMP ADDED RAISE FOR TESTIGN
            raise
            PS_support.messageForExceptionType(e, "PdInflorescence.nextDay")

    def traverseActivity(self, mode, traverserProxy):
        ''' active when:
            - draw, calc triangles..
            - next day calcs
            - reproduction - mod biomass
            - finding part near position
        '''
        # do part aspect first
        PS_part.PdPlantPart.traverseActivity(self, mode, traverserProxy)
        traverser = traverserProxy
        if traverser == None:
            return
        if self.hasFallenOff and (mode != kActivityStream) and (mode != kActivityFree):
            return
        #
        try:
            if (mode != kActivityDraw):
                if len(self.flowers) > 0:
                    for flower in self.flowers:
                        flower.traverseActivity(mode, traverser)
            if mode == kActivityNone:
                pass
            elif mode == kActivityNextDay:
                self.nextDay()
            elif mode == kActivityDemandVegetative:
                pass
            elif mode == kActivityDemandReproductive:
                if (self.age > self.plant.pInflor[self.gender].maxDaysToGrow):
                    # no vegetative demand
                    self.biomassDemand_pctMPB = 0.0
                    return
                try:
                    self.biomassDemand_pctMPB = PS_travers.linearGrowthResult(self.liveBiomass_pctMPB, self.plant.pInflor[self.gender].optimalBiomass_pctMPB, self.plant.pInflor[self.gender].minDaysToGrow)
                    traverser.total = traverser.total + self.biomassDemand_pctMPB
                except Exception, e:
                    PS_support.messageForExceptionType(e, "PdInflorescence.traverseActivity (reproductive demand)")
            elif mode == kActivityGrowVegetative:
                pass
            elif mode == kActivityGrowReproductive:
                if self.age > self.plant.pInflor[self.gender].maxDaysToGrow:
                    # no vegetative growth
                    return
                newBiomass_pctMPB = self.biomassDemand_pctMPB * traverser.fractionOfPotentialBiomass
                self.liveBiomass_pctMPB = self.liveBiomass_pctMPB + newBiomass_pctMPB
            elif mode == kActivityStartReproduction:
                pass
            elif mode == kActivityFindPlantPartAtPosition:
                if PS_math.pointsAreCloseEnough(traverser.point, self.position()):
                    # cannot switch
                    traverser.foundPlantPart = self
                    traverser.finished = True
            elif mode == kActivityDraw:
                self.draw()
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
                #streaming called by phytomer
                # free called by phytomer
                # none
                # none
                traverser.total = traverser.total + self.liveBiomass_pctMPB
            elif mode == kActivityRemoveReproductiveBiomass:
                biomassToRemove_pctMPB = self.liveBiomass_pctMPB * traverser.fractionOfPotentialBiomass
                self.liveBiomass_pctMPB = self.liveBiomass_pctMPB - biomassToRemove_pctMPB
                self.deadBiomass_pctMPB = self.deadBiomass_pctMPB + biomassToRemove_pctMPB
            elif mode == kActivityGatherStatistics:
                if self.gender == kGenderMale:
                    self.addToStatistics(traverser.statistics, kStatisticsPartTypeMaleInflorescence)
                else:
                    self.addToStatistics(traverser.statistics, kStatisticsPartTypeFemaleInflorescence)
                self.addToStatistics(traverser.statistics, kStatisticsPartTypeAllReproductive)
            elif mode == kActivityCountPlantParts:
                pass
            elif mode == kActivityFindPartForPartID:
                pass
            elif mode == kActivityCountTotalMemoryUse:
                traverser.totalMemorySize += self.instanceSize
            elif mode == kActivityCalculateBiomassForGravity:
                self.biomassOfMeAndAllPartsAboveMe_pctMPB = self.biomassOfMeAndAllPartsConnectedToMe_pctMPB()
            elif mode == kActivityCountPointsAndTrianglesFor3DExport:
                self.countPointsAndTrianglesFor3DExportAndAddToTraverserTotals(traverser)
            else :
                raise GeneralException.create("Problem: Unhandled mode in method PdInflorescence.traverseActivity.")
        except Exception, e:
            # PDF PORT ADDED RAISE FOR TESTING
            raise
            PS_support.messageForExceptionType(e, "PdInflorescence.traverseActivity")

    def countPointsAndTrianglesFor3DExportAndAddToTraverserTotals(self, traverser):
        if traverser == None:
            return
        if self.plant.pInflor[self.gender].bractTdoParams.scaleAtFullSize > 0:
            # bracts
            traverser.total3DExportPointsIn3DObjects += self.plant.pInflor[self.gender].bractTdoParams.object3D.pointsInUse * self.plant.pInflor[self.gender].bractTdoParams.repetitions
            traverser.total3DExportTrianglesIn3DObjects += len(self.plant.pInflor[self.gender].bractTdoParams.object3D.triangles) * self.plant.pInflor[self.gender].bractTdoParams.repetitions
            self.addExportMaterial(traverser, kExportPartInflorescenceBractFemale, kExportPartInflorescenceBractMale)
        # pedicels and inflorescence internodes
        numLines = self.plant.pInflor[self.gender].numBranches
        if not self.plant.pInflor[self.gender].branchesAreAlternate:
            numLines = numLines * 2
        if self.plant.pInflor[self.gender].internodeLength_mm > 0:
            self.addExportMaterial(traverser, kExportPartInflorescenceInternodeFemale, kExportPartInflorescenceInternodeMale)
        # peduncle
        numLines += 1
        traverser.total3DExportStemSegments += numLines
        if self.plant.pInflor[self.gender].peduncleLength_mm > 0:
            self.addExportMaterial(traverser, kExportPartInflorescenceStalkFemale, kExportPartInflorescenceStalkMale)

    def report(self):
        PS_part.PdPlantPart.report(self)
        udebug.DebugPrint("%d flowers" % (self.numFlowers))
        # note flowers will print first
        # debugPrint('inflorescence, age %d' % (age))
        #DebugForm.printNested(plant.turtle.stackSize, 'inflorescence, age %d' % (age))

    def biomassOfMeAndAllPartsConnectedToMe_pctMPB(self):
        result = self.totalBiomass_pctMPB()
        if len(self.flowers) > 0:
            for flower in self.flowers:
                result = result + flower.totalBiomass_pctMPB()
        return result

    def allFlowersHaveBeenDrawn(self):
        result = True
        if len(self.flowers) > 0:
            for flower in self.flowers:
                if not flower.hasBeenDrawn:
                    result = False
                    return result
        return result

    def addDependentPartsToList(self, aList):
        if len(self.flowers) > 0:
            for flower in self.flowers:
                aList.Add(flower)

    def createFlower(self):
        if self.plant.partsCreated > udomain.domain.options.maxPartsPerPlant_thousands * 1000:
            # create new flower/fruit object
            # v1.6b1
            return
        aFlowerFruit = PS_fruit.PdFlowerFruit()
        aFlowerFruit.initializeGender(self.plant, self.gender)
        self.flowers.Add(aFlowerFruit)

    def deleteFlower(self, theFlower):
        # remove flower object from list
        self.flowers.Remove(theFlower)

    def draw(self):
        if not self.shouldDraw():
            return
        turtle = self.plant.turtle
        self.boundsRect = Rect(0, 0, 0, 0)
        turtle.push()
        if self.hiddenByAmendment():
            # amendment rotation handled in drawStemSegment for peduncle
            turtle.pop()
            return
        try:
            for flower in self.flowers:
                flower.hasBeenDrawn = False
            self.calculateColors()
            turtle.ifExporting_startNestedGroupOfPlantParts(self.genderString() + " inflorescence", self.genderString() + "Inflor", kNestingTypeInflorescence)
            if self.flowers:
                self.drawBracts()
                self.drawPeduncle()
                if (self.plant.pInflor[self.gender].isHead):
                    self.drawHead()
                else:
                    self.drawApex(self.plant.pInflor[self.gender].numFlowersOnMainBranch, 0, True)
            turtle.ifExporting_endNestedGroupOfPlantParts(kNestingTypeInflorescence)
            turtle.pop()
        except Exception, e:
            # PDF PORT ADDED TEMP RAISE FOR TESTING
            raise
            PS_support.messageForExceptionType(e, "PdInflorescence.draw")

    def shouldDraw(self):
        # if inflorescence has at least one flower or non-fallen fruit, should draw
        result = True
        for flowerFruit in self.flowers:
            if flowerFruit == None:
                continue
            if not flowerFruit.hasFallenOff:
                return result
        result = False
        return result

    def drawApex(self, internodeCount, flowerIndexOffset, mainBranch):
        i = 0
        #Draw inflorescence in raceme, panicle, or umbel form. This method uses the recursive algorithm
        #     we first developed to draw the entire plant.
        turtle = self.plant.turtle
        if turtle == None:
            return
        branchesDrawn = 0
        if internodeCount > 0:
            if mainBranch:
                # draw the flowers on the main stem first, because if any are not going to be drawn for
                # want of available flowers, the branches should lose them.
                turtle.push()
            if mainBranch:
                while branchesDrawn < self.plant.pInflor[self.gender].numBranches:
                    self.drawInternode(i)
                    branchesDrawn += 1
            # draw flowers on main stem first
            i = internodeCount
            while i >= 1:
                if self.plant.pInflor[self.gender].flowersSpiralOnStem:
                    #param
                    turtle.rotateX(98)
                self.drawInternode(i)
                turtle.push()
                self.drawFlower(flowerIndexOffset + i)
                turtle.pop()
                i -= 1
            if mainBranch:
                turtle.pop()
        branchesDrawn = 0
        if mainBranch:
            while branchesDrawn < self.plant.pInflor[self.gender].numBranches:
                if self.plant.pInflor[self.gender].flowersSpiralOnStem:
                    # draw branches
                    #param
                    turtle.rotateX(98)
                self.drawInternode(i)
                self.drawAxillaryBud(self.plant.pInflor[self.gender].numFlowersPerBranch, self.plant.pInflor[self.gender].numFlowersOnMainBranch + branchesDrawn * self.plant.pInflor[self.gender].numFlowersPerBranch)
                branchesDrawn += 1
                if (not self.plant.pInflor[self.gender].branchesAreAlternate) and (branchesDrawn < self.plant.pInflor[self.gender].numBranches):
                    turtle.push()
                    turtle.rotateX(128)
                    self.drawAxillaryBud(self.plant.pInflor[self.gender].numFlowersPerBranch, self.plant.pInflor[self.gender].numFlowersOnMainBranch + branchesDrawn * self.plant.pInflor[self.gender].numFlowersPerBranch)
                    branchesDrawn += 1
                    turtle.pop()

    def drawBracts(self):
        if (self.plant.turtle == None):
            return
        if self.plant.pInflor[self.gender].bractTdoParams.scaleAtFullSize <= 0:
            return
        turtle = self.plant.turtle
        turtle.push()
        turtle.ifExporting_startNestedGroupOfPlantParts(self.longNameForDXFPartConsideringGenderEtc(kExportPartInflorescenceBractFemale), self.shortNameForDXFPartConsideringGenderEtc(kExportPartInflorescenceBractFemale), kNestingTypeInflorescence)
        propFullSize = PS_math.safedivExcept(self.liveBiomass_pctMPB, self.plant.pInflor[self.gender].optimalBiomass_pctMPB, 0)
        scale = ((self.plant.pInflor[self.gender].bractTdoParams.scaleAtFullSize / 100.0) * propFullSize)
        turtle.rotateX(self.angleWithSway(self.plant.pInflor[self.gender].bractTdoParams.xRotationBeforeDraw))
        turtle.rotateY(self.angleWithSway(self.plant.pInflor[self.gender].bractTdoParams.yRotationBeforeDraw))
        turtle.rotateZ(self.angleWithSway(self.plant.pInflor[self.gender].bractTdoParams.zRotationBeforeDraw))
        if (self.plant.pInflor[self.gender].bractTdoParams.radiallyArranged) and (self.plant.pInflor[self.gender].bractTdoParams.repetitions > 0):
            turnPortion = 256 / self.plant.pInflor[self.gender].bractTdoParams.repetitions
            leftOverDegrees = 256 - turnPortion * self.plant.pInflor[self.gender].bractTdoParams.repetitions
            if leftOverDegrees > 0:
                addition = PS_math.safedivExcept(leftOverDegrees, self.plant.pInflor[self.gender].bractTdoParams.repetitions, 0)
            else:
                addition = 0
            carryOver = 0
            for i in range(0, self.plant.pInflor[self.gender].bractTdoParams.repetitions):
                turtle.push()
                #aligns object as stored in the file to way should draw on plant
                turtle.rotateY(-64)
                # why? i don't know.
                turtle.rotateX(64)
                turtle.rotateX(self.plant.pInflor[self.gender].bractTdoParams.pullBackAngle)
                self.draw3DObject(self.plant.pInflor[self.gender].bractTdoParams.object3D, scale, self.plant.pInflor[self.gender].bractTdoParams.faceColor, self.plant.pInflor[self.gender].bractTdoParams.backfaceColor, kExportPartInflorescenceBractFemale)
                turtle.pop()
                addThisTime = math.floor(addition + carryOver)
                carryOver = carryOver + addition - addThisTime
                if carryOver < 0:
                    carryOver = 0
                turtle.rotateX(turnPortion + addThisTime)
        else:
            turtle.push()
            #aligns object as stored in the file to way should draw on plant
            turtle.rotateY(-64)
            # why? i don't know.
            turtle.rotateX(64)
            turtle.rotateX(self.plant.pInflor[self.gender].bractTdoParams.pullBackAngle)
            self.draw3DObject(self.plant.pInflor[self.gender].bractTdoParams.object3D, scale, self.plant.pInflor[self.gender].bractTdoParams.faceColor, self.plant.pInflor[self.gender].bractTdoParams.backfaceColor, kExportPartInflorescenceBractFemale)
            turtle.pop()
        turtle.pop()
        turtle.ifExporting_endNestedGroupOfPlantParts(kNestingTypeInflorescence)

    def drawPeduncle(self):
        try:
            #Draw peduncle, which is the primary inflorescence stalk. If the inflorescence has only one flower,
            #     this is the only part drawn. If the inflorescence is apical, the stalk may be longer (e.g. in bolting
            #     plants) and is specified by a different parameter.
            zAngle = 0
            if (self.phytomerAttachedTo != None):
                if (self.phytomerAttachedTo.leftBranchPlantPart == self):
                    zAngle = self.plant.pInflor[self.gender].peduncleAngleFromVegetativeStem
                elif (self.phytomerAttachedTo.rightBranchPlantPart == self):
                    zAngle = self.plant.pInflor[self.gender].peduncleAngleFromVegetativeStem
                    self.plant.turtle.rotateX(128)
                elif self.isApical:
                    zAngle = self.plant.pInflor[self.gender].apicalStalkAngleFromVegetativeStem
            propFullSize = PS_math.safedivExcept(self.liveBiomass_pctMPB, self.plant.pInflor[self.gender].optimalBiomass_pctMPB, 0)
            if self.isApical:
                length = self.lengthOrWidthAtAgeForFraction(self.plant.pInflor[self.gender].terminalStalkLength_mm, propFullSize)
            else:
                length = self.lengthOrWidthAtAgeForFraction(self.plant.pInflor[self.gender].peduncleLength_mm, propFullSize)
            width = self.lengthOrWidthAtAgeForFraction(self.plant.pInflor[self.gender].internodeWidth_mm, propFullSize)
            #Use no angle here because phytomer makes the rotation before the inflorescence is drawn.
            self.drawStemSegment(length, width, zAngle, 0, self.plant.pInflor[self.gender].stalkColor, kDontTaper, kExportPartInflorescenceStalkFemale, kUseAmendment)
        except Exception, e:
            PS_support.messageForExceptionType(e, "PdInflorescence.drawPeduncle")

    def drawAxillaryBud(self, internodeCount, flowerIndexOffset):
        #This message is sent when the inflorescence is branched. The decision to create a branch is
        #     made before the message is sent. Note the check if all flowers have been drawn; this prevents
        #     scrawly lines with no flowers.
        turtle = self.plant.turtle
        if (turtle == None):
            return
        if (self.allFlowersHaveBeenDrawn()):
            return
        angle = self.angleWithSway(self.plant.pInflor[self.gender].branchAngle)
        turtle.push()
        turtle.rotateZ(angle)
        self.drawApex(internodeCount, flowerIndexOffset, False)
        turtle.pop()

    def drawFlower(self, internodeCount):
        try:
            if (self.allFlowersHaveBeenDrawn()):
                #Draw one flower, remembering that internodeCount goes from flowers size down to 1,
                #  but flowers are in the order formed.
                #  If the oldest flowers on the inflorescence are at the bottom (acropetal),
                #  draw the flowers in reverse order from internodeCount (which is in the order they were formed).
                #  If the oldest flowers on the inflorescence are at the top (basipetal),
                #  draw the flowers in the order presented by internodeCount
                #     which is in reverse order to how they were formed).
                #  In most plants the older flowers are lower.
                return
            propFullSize = PS_math.safedivExcept(self.liveBiomass_pctMPB, self.plant.pInflor[self.gender].optimalBiomass_pctMPB, 0)
            length = self.lengthOrWidthAtAgeForFraction(self.plant.pInflor[self.gender].pedicelLength_mm, propFullSize)
            width = self.lengthOrWidthAtAgeForFraction(self.plant.pInflor[self.gender].internodeWidth_mm, propFullSize)
            angle = self.angleWithSway(self.plant.pInflor[self.gender].pedicelAngle)
            if (self.plant.pInflor[self.gender].flowersDrawTopToBottom):
                flowerIndex = internodeCount
            else:
                flowerIndex = len(self.flowers) - internodeCount + 1
            self.plant.turtle.ifExporting_startNestedGroupOfPlantParts(self.genderString() + " pedicel and flower/fruit", self.genderString() + "PedicelFlower", kNestingTypePedicelAndFlowerFruit)
            self.drawStemSegment(length, width, angle, 0, self.plant.pInflor[self.gender].pedicelColor, self.plant.pInflor[self.gender].pedicelTaperIndex, kExportPartPedicelFemale, kDontUseAmendment)
            if (flowerIndex - 1 >= 0) and (flowerIndex - 1 <= len(self.flowers) - 1):
                self.flowers[flowerIndex - 1].draw()
            self.plant.turtle.ifExporting_endNestedGroupOfPlantParts(kNestingTypePedicelAndFlowerFruit)
        except Exception, e:
            # PDF PORT ADDED RAISE FOR TESTING
            raise
            PS_support.messageForExceptionType(e, "PdInflorescence.drawFlower")

    def drawHead(self):
        # v1.4
        # v1.4
        #Draw the inflorescences in a radial pattern; this is for a head such as a sunflower.
        turtle = self.plant.turtle
        if (turtle == None):
            return
        turtle.rotateY(64)
        turtle.rotateZ(64)
        # give a little angle down to make it look more natural
        turtle.rotateY(32)
        if len(self.flowers) > 0:
            # new v1.4
            turnPortion = 256 / len(self.flowers)
            leftOverDegrees = 256 - turnPortion * len(self.flowers)
            if leftOverDegrees > 0:
                addition = PS_math.safedivExcept(leftOverDegrees, len(self.flowers), 0)
            else:
                addition = 0
            carryOver = 0
            for i in range(len(self.flowers) - 1, -1, -1):
                addThisTime = math.floor(addition + carryOver)
                carryOver = carryOver + addition - addThisTime
                if carryOver < 0:
                    carryOver = 0
                # was 256 / flowers.count
                turtle.rotateZ(turnPortion + addThisTime)
                turtle.push()
                # v1.4 added one, was bug, was not drawing first flower
                self.drawFlower(i + 1)
                turtle.pop()

    def drawInternode(self, internodeCount):
        try:
            if (self.allFlowersHaveBeenDrawn()):
                #Draw the inflorescence internode, which is the portion of inflorescence stem between where successive
                #  flower pedicels come off. Note that this is not drawn if all flowers have been drawn; this prevents
                #  straggly lines in branched inflorescences.
                return
            if (self.plant.pInflor[self.gender].internodeLength_mm == 0.0):
                return
            propFullSize = PS_math.safedivExcept(self.liveBiomass_pctMPB, self.plant.pInflor[self.gender].optimalBiomass_pctMPB, 0)
            length = self.lengthOrWidthAtAgeForFraction(self.plant.pInflor[self.gender].internodeLength_mm, propFullSize)
            width = self.lengthOrWidthAtAgeForFraction(self.plant.pInflor[self.gender].internodeWidth_mm, propFullSize)
            zAngle = self.angleWithSway(self.plant.pInflor[self.gender].angleBetweenInternodes)
            yAngle = self.angleWithSway(0)
            self.drawStemSegment(length, width, zAngle, yAngle, self.plant.pInflor[self.gender].stalkColor, kDontTaper, kExportPartInflorescenceInternodeFemale, kDontUseAmendment)
        except Exception, e:
            PS_support.messageForExceptionType(e, "PdInflorescence.drawInternode")

    def lengthOrWidthAtAgeForFraction(self, starting, fraction):
        result = 0.0
        try:
            ageBounded = min(self.plant.pInflor[self.gender].daysToAllFlowersCreated, self.daysSinceStartedMakingFlowers)
            if self.plant.pInflor[self.gender].daysToAllFlowersCreated != 0:
                result = PS_math.safedivExcept(starting * ageBounded, self.plant.pInflor[self.gender].daysToAllFlowersCreated, 0) * fraction
            else:
                result = starting * ageBounded * fraction
        except Exception, e:
            PS_support.messageForExceptionType(e, "PdInflorescence.lengthOrWidthAtAgeForFraction")
        return result

    def flower(self, index):
        result = self.flowers[index]
        return result

    def partType(self):
        result = kPartTypeInflorescence
        return result

    def classAndVersionInformation(self, cvir):
        cvir.classNumber = uclasses.kPdInflorescence
        cvir.versionNumber = 0
        cvir.additionNumber = 0

##    def streamDataWithFiler(self, filer, cvir):
##        PS_part.PdPlantPart.streamDataWithFiler(self, filer, cvir)
##        self.daysSinceStartedMakingFlowers = filer.streamSmallint(self.daysSinceStartedMakingFlowers)
##        self.numFlowersEachDay = filer.streamSmallint(self.numFlowersEachDay)
##        self.numFlowers = filer.streamSmallint(self.numFlowers)
##        self.daysBetweenFlowerAppearances = filer.streamSmallint(self.daysBetweenFlowerAppearances)
##        self.daysSinceLastFlowerAppeared = filer.streamSmallint(self.daysSinceLastFlowerAppeared)
##        self.isApical = filer.streamBoolean(self.isApical)
##        self.fractionOfOptimalSizeWhenCreated = filer.streamSingle(self.fractionOfOptimalSizeWhenCreated)
##        if filer.isReading():
##            self.meristemThatCreatedMe = None
##        self.flowers.streamUsingFiler(filer, PS_fruit.PdFlowerFruit)
##        if filer.isReading() and (len(self.flowers) > 0):
##            for flower in self.flowers:
##                # fix up plant in flowers if needed
##                flower.plant = self.plant

#The inflorescence is very simple; it creates a specified number of flowers over a specified period
#  of days. Each inflorescence on the plant has the same number of flowers. Since an inflorescence is
#  created by a meristem which accumulates biomass, nothing stands in the way of the inflorescence
#  producing the flowers according to schedule.
#  This method must act differently for inflorescences that produce flowers slowly (over a greater
#  number of days than flowers) than for those that produce many flowers in a few days.
#  The inflorescence can create no flowers until it reaches a specified fraction of its optimal biomass.
#Survey flowers and return true if all flowers have been drawn (they know), false if any have not been
#   drawn. This is mostly so a branched inflorescence can know if there are any flowers left to place
#   on its branched structure.
