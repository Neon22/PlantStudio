### PS_constants
### - holds all constants stripped from dependent files - to ease import crazyness
### Dependencies: None
### - !! need to rename constants to indicate where they camer from so relationships easier to understand.


### from PS_Plant
kGenderMale = 0
kGenderFemale = 1
kCompoundLeafPinnate = 0
kCompoundLeafPalmate = 1
kArrangementAlternate = 0
kArrangementOpposite = 1
kStageFlowerBud = 1
kStageOpenFlower = 2
kStageUnripeFruit = 3
kStageRipeFruit = 4
kPartTypeNone = 0
kPartTypeFlowerFruit = 1
kPartTypeInflorescence = 2
kPartTypeMeristem = 3
kPartTypePhytomer = 4
kPartTypeLeaf = 5
kDirectionLeft = 0
kDirectionRight = 1
kGetField = 0
kSetField = 1
kPlantNameLength = 80
kCheckForUnreadParams = True
kDontCheckForUnreadParams = False
kConsiderDomainScale = True
kDontConsiderDomainScale = False
kDrawNow = True
kDontDrawNow = False
kMutation = 0
kWeight = 1
kMaxBreedingSections = 20
kFromFirstPlant = 0
kFromSecondPlant = 1
kFromProbabilityBasedOnWeightsForSection = 2
kFromPlantWithGreaterWeightForSectionIfEqualFirstPlant = 3
kFromPlantWithGreaterWeightForSectionIfEqualSecondPlant = 4
kFromPlantWithGreaterWeightForSectionIfEqualChooseRandomly = 5
kPlantAsTextStartString = "start PlantStudio plant"
kPlantAsTextEndString = "end PlantStudio plant"
kStartNoteString = "=== start note"
kEndNoteString = "=== end note"
kInMainWindow = True
kNotInMainWindow = False
kBud = 0
kPistils = 1
kStamens = 2
kFirstPetals = 3
kSecondPetals = 4
kThirdPetals = 5
kFourthPetals = 6
kFifthPetals = 7
kSepals = 8
kHighestFloralPartConstant = kSepals
kDrawNoBud = 0
kDrawSingleTdoBud = 1
kDrawOpeningFlower = 2
kNotExactAge = False
kExactAge = True


### from PS_travers
kTraverseNone = 0
kTraverseLeft = 1
kTraverseRight = 2
kTraverseNext = 3
kTraverseDone = 4
kActivityNone = 0
kActivityNextDay = 1
kActivityDemandVegetative = 2
kActivityDemandReproductive = 3
kActivityGrowVegetative = 4
kActivityGrowReproductive = 5
kActivityStartReproduction = 6
kActivityFindPlantPartAtPosition = 7
kActivityDraw = 8
kActivityReport = 9
kActivityStream = 10
kActivityFree = 11
kActivityVegetativeBiomassThatCanBeRemoved = 12
kActivityRemoveVegetativeBiomass = 13
kActivityReproductiveBiomassThatCanBeRemoved = 14
kActivityRemoveReproductiveBiomass = 15
kActivityGatherStatistics = 16
kActivityStandingDeadBiomassThatCanBeRemoved = 17
kActivityRemoveStandingDeadBiomass = 18
kActivityCountPlantParts = 19
kActivityFindPartForPartID = 20
kActivityCountTotalMemoryUse = 21
kActivityCalculateBiomassForGravity = 22
kActivityCountPointsAndTrianglesFor3DExport = 23
#
kStatisticsPartTypeSeedlingLeaf = 0
kStatisticsPartTypeLeaf = 1
kStatisticsPartTypeFemaleInflorescence = 2
kStatisticsPartTypeMaleInflorescence = 3
kStatisticsPartTypeFemaleFlower = 4
kStatisticsPartTypeFemaleFlowerBud = 5
kStatisticsPartTypeMaleFlower = 6
kStatisticsPartTypeMaleFlowerBud = 7
kStatisticsPartTypeAxillaryBud = 8
kStatisticsPartTypeFruit = 9
kStatisticsPartTypeStem = 10
kStatisticsPartTypeUnripeFruit = 11
kStatisticsPartTypeFallenFruit = 12
kStatisticsPartTypeUnallocatedNewVegetativeBiomass = 13
kStatisticsPartTypeUnremovedDeadVegetativeBiomass = 14
kStatisticsPartTypeUnallocatedNewReproductiveBiomass = 15
kStatisticsPartTypeUnremovedDeadReproductiveBiomass = 16
kStatisticsPartTypeFallenFlower = 17
kStatisticsPartTypeAllVegetative = 18
kStatisticsPartTypeAllReproductive = 19
kStatisticsPartTypeLast = 19


### from PS_3dexport
#colors
clBlack = 0x000000
clMaroon = 0x000080
clGreen = 0x008000
clOlive = 0x008080
clNavy = 0x800000
clPurple = 0x800080
clTeal = 0x808000
clGray = 0x808080
clSilver = 0xC0C0C0
clRed = 0x0000FF
clLime = 0x00FF00
clYellow = 0x00FFFF
clBlue = 0xFF0000
clFuchsia = 0xFF00FF
clAqua = 0xFFFF00
clLtGray = 0xC0C0C0
clDkGray = 0x808080
clWhite = 0xFFFFFF
clCream = 0xF0FBFF
clNone = 0x1FFFFFFF
#
kExportPartMeristem = 0
kExportPartInternode = 1
kExportPartSeedlingLeaf = 2
kExportPartLeaf = 3
kExportPartFirstPetiole = 4
kExportPartPetiole = 5
kExportPartLeafStipule = 6
kExportPartInflorescenceStalkFemale = 7
kExportPartInflorescenceInternodeFemale = 8
kExportPartInflorescenceBractFemale = 9
kExportPartInflorescenceStalkMale = 10
kExportPartInflorescenceInternodeMale = 11
kExportPartInflorescenceBractMale = 12
kExportPartPedicelFemale = 13
kExportPartFlowerBudFemale = 14
kExportPartStyleFemale = 15
kExportPartStigmaFemale = 16
kExportPartFilamentFemale = 17
kExportPartAntherFemale = 18
kExportPartFirstPetalsFemale = 19
kExportPartSecondPetalsFemale = 20
kExportPartThirdPetalsFemale = 21
kExportPartFourthPetalsFemale = 22
kExportPartFifthPetalsFemale = 23
kExportPartSepalsFemale = 24
kExportPartPedicelMale = 25
kExportPartFlowerBudMale = 26
kExportPartFilamentMale = 27
kExportPartAntherMale = 28
kExportPartFirstPetalsMale = 29
kExportPartSepalsMale = 30
kExportPartUnripeFruit = 31
kExportPartRipeFruit = 32
kExportPartRootTop = 33
kExportPartLast = 33
kLastDxfColorIndex = 10
dxfColors = [clRed, clYellow, clLime, clAqua, clBlue, clPurple, clBlack, clOlive, clFuchsia, clTeal, clGray, ]
kColorDXFFromPlantPartType = 0
kColorDXFFromRGB = 1
kColorDXFFromOneColor = 3
kNestingTypeInflorescence = 0
kNestingTypeLeafAndPetiole = 1
kNestingTypeCompoundLeaf = 2
kNestingTypePedicelAndFlowerFruit = 3
kNestingTypeFloralLayers = 4
kMaxPOVPlants = 1000
kMaxStoredMaterials = 1000
kVRMLVersionOne = 0
kVRMLVersionTwo = 1
kScreen = 0
kDXF = 1
kPOV = 2
k3DS = 3
kOBJ = 4
kVRML = 5
kLWO = 6
k3DExportTypeLast = 6
kLayerOutputAllTogether = 0
kLayerOutputByTypeOfPlantPart = 1
kLayerOutputByPlantPart = 2
kWriteColor = True
kDontWriteColor = False
kMax3DPoints = 65536
kMax3DFaces = 65536
kX = 0
kY = 1
kZ = 2


### from PS_params
# const
kFieldUndefined = 0
kFieldFloat = 1
kFieldSmallint = 2
kFieldColor = 3
kFieldBoolean = 4
kFieldThreeDObject = 5
kFieldEnumeratedList = 6
kFieldHeader = 7
kFieldLongint = 8

kIndexTypeUndefined = 0
kIndexTypeNone = 1
kIndexTypeSCurve = 3

kTransferTypeUndefined = 0
kTransferTypeMFD = 1
kTransferTypeGetSetSCurve = 2
kTransferTypeObject3D = 3
kNotArray = -1


### from PS-part
kAddingBiomassToPlant = True
kRemovingBiomassFromPlant = False
kDontTaper = -1.0
kUseAmendment = True
kDontUseAmendment = False
# const
kDrawingTdo = True
kDrawingLine = False
kRotateX = 0
kRotateY = 1
kRotateZ = 2

### from