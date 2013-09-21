# unit Uparams

import ucollect
import umakepm

"""
from conversion_common import *
import uunits
import usection
import usupport
import uexcept
import delphi_compatability
"""

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

# FieldType
#note: the longint type is NOT for use for parameters (in param panels or breeding).
#     if you want to use a longint for a parameter, you have to
#     update the breeding method and the method that creates param panels. the smallint panel will not
#     work correctly with a longint as it is now (but you could subclass it if you need one).
# IndexType - for arrays
# transferType - how data is transferred to and from model object
#mfd is short for MoveFieldData
#must be whole string to allow for tdos
# v2.1
# ---------------------------------------------------------- PdParameter

class PdParameter(object):
    ''' Primary class for manipulating paramters of a plant '''
    def __init__(self):
        self.fieldNumber = 0
        self.fieldID = ""
        self.name = ""
        self.fieldType = 0
        self.indexType = 0
        self.unitSet = 0
        self.unitModel = 0
        self.unitMetric = 0
        self.unitEnglish = 0
        self.lowerBoundOriginal = 0.0
        self.upperBoundOriginal = 0.0
        self.defaultValueStringOriginal = ""
        self.cannotOverride = False
        self.isOverridden = False
        self.lowerBoundOverride = 0.0
        self.upperBoundOverride = 0.0
        self.defaultValueStringOverride = ""
        self.regrow = False
        self.readOnly = False
        self.accessString = ""
        self.transferType = 0
        self.hint = ""
        self.valueHasBeenReadForCurrentPlant = False
        self.collapsed = True
        self.originalSectionName = ""

    def make(self, aFieldNumber, aFieldID, aName, aFieldType, anIndexType, aUnitSet, aUnitModel, aUnitMetric, aUnitEnglish, aLowerBound, anUpperBound, aDefaultValueString, aRegrow, aReadOnly, anAccessString, aTransferType, aHint):
        self.fieldNumber = aFieldNumber
        self.fieldID = aFieldID[:80]
        self.name = aName[:80]
        self.fieldType = aFieldType
        # v2.0 headers can have hints
        self.hint = aHint
        if self.fieldType == kFieldHeader:
            return self
        self.indexType = anIndexType
        self.unitSet = aUnitSet
        self.unitModel = aUnitModel
        self.unitMetric = aUnitMetric
        self.unitEnglish = aUnitEnglish
        self.lowerBoundOriginal = aLowerBound
        self.upperBoundOriginal = anUpperBound
        self.defaultValueStringOriginal = aDefaultValueString
        self.regrow = aRegrow
        self.readOnly = aReadOnly
        self.accessString = anAccessString[:80]
        self.transferType = aTransferType
        return self

    def indexCount(self):
        result = 1
        if self.indexType == kIndexTypeUndefined:
            result = 1
        elif self.indexType == kIndexTypeNone:
            result = 1
        elif self.indexType == kIndexTypeSCurve:
            result = 4
        else :
            raise GeneralException.create("Problem: Unexpected index type in method PdParameter.indexCount.")
        return result

    def getName(self):
        result = self.name
        return result

    def setName(self, newName):
        self.name = UNRESOLVED.copy(newName, 1, 80)

    def lowerBound(self):
        if (not self.cannotOverride) and (self.isOverridden):
            result = self.lowerBoundOverride
        else:
            result = self.lowerBoundOriginal
        return result

    def upperBound(self):
        if (not self.cannotOverride) and (self.isOverridden):
            result = self.upperBoundOverride
        else:
            result = self.upperBoundOriginal
        return result

    def defaultValueString(self):
        if (not self.cannotOverride) and (self.isOverridden):
            result = self.defaultValueStringOverride
        else:
            result = self.defaultValueStringOriginal
        return result

    # appears unused
    def getHint(self):
        result = self.hint
        return result

# ---------------------------------------------------- PdParameterManager
# used by udomain/PdDomain class
class PdParameterManager:
    def __init__(self):
        self.parameters = ucollect.TListCollection()

    # used by addParameterForSection
    def addParameter(self, newParameter):
        if newParameter != None:
            self.parameters.Add(newParameter)

    # used by umakepm
    def addParameterForSection(self, sectionName, orthogonalSectionName, newParameter):
        # import done here due to circularity issues
        import udomain
        section = udomain.domain.sectionManager.sectionForName(sectionName)
        if section == None:
            section = udomain.domain.sectionManager.addSection(sectionName)
            # the 'no section' section is hidden from the parameters window but we still want the section for writing out
            section.showInParametersWindow = not (sectionName.upper() == "(no section)".upper())
        self.addParameter(newParameter)
        if section != None:
            newParameter.originalSectionName = sectionName
            section.addSectionItem(newParameter.fieldNumber)
        # v2.1 orthogonal sections
        # limitation - each param can only have one orthogonal section specified
        # if want to add more later, use delimiter and parse
        orthogonalSectionName = orthogonalSectionName.strip()
        if orthogonalSectionName != "":
            section = udomain.domain.sectionManager.sectionForName(orthogonalSectionName)
            if section == None:
                section = udomain.domain.sectionManager.addOrthogonalSection(orthogonalSectionName)
                section.showInParametersWindow = True
                section.isOrthogonal = True
            if section != None:
                section.addSectionItem(newParameter.fieldNumber)

    # used in udomain for debug
    def fieldTypeName(self, fieldType):
        if fieldType == kFieldUndefined:
            result = "Undefined"
        elif fieldType == kFieldFloat:
            result = "Single"
        elif fieldType == kFieldSmallint:
            result = "Smallint"
        elif fieldType == kFieldColor:
            result = "Color"
        elif fieldType == kFieldBoolean:
            result = "Boolean"
        elif fieldType == kFieldThreeDObject:
            result = "3D object"
        elif fieldType == kFieldEnumeratedList:
            result = "List of choices"
        elif fieldType == kFieldLongint:
            result = "Longint"
        else:
            result = "not in list"
        return result

##    def indexTypeName(self, indexType):
##        if indexType == kIndexTypeUndefined:
##            result = "Undefined"
##        elif indexType == kIndexTypeNone:
##            result = "None"
##        elif indexType == kIndexTypeSCurve:
##            result = "S curve"
##        else:
##            result = "not in list"
##        return result

##    def parameterForIndex(self, index):
##        result = self.parameters[index]
##        return result

    # used by umakepm/CreateParameters
    def clearParameters(self):
        self.parameters.clear()

    # used by uplant/PlantLoader.loadPlantsFromFile
    def setAllReadFlagsToFalse(self):
        for parameter in self.parameters:
            parameter.valueHasBeenReadForCurrentPlant = False

    # used by updcom/PdChangeValueCommand.description
    # used by uplant/PdPlant.writeToPlantFile and useBreedingOptionsAndPlantsToSetParameters
    # used by usection/PdSectionManager.parameterForSectionAndName
    def parameterForFieldNumber(self, fieldNumber):
        ''' return parameter into self.parameters where:
            - fieldNumber matches (unique in range 1..399)   '''
        result = None
        for parameter in self.parameters:
            if fieldNumber == parameter.fieldNumber:
                result = parameter
                return result
        raise GeneralException.create("Problem: Parameter not found for field number %d in method PdParameterManager.parameterForFieldNumber." % (fieldNumber))
        return result

##    def parameterForFieldID(self, fieldID):
##        ''' return parameter from self.parameters where:
##            - fieldID matches (unique for a parameter). E.g. "kGeneralRandomSway"   '''
##        result = None
##        for parameter in self.parameters:
##            if fieldID.upper().strip() == parameter.fieldID.upper().strip():
##                result = parameter
##                return result
##        raise GeneralException.create("Problem: Parameter not found for field ID " + fieldID + " in method PdParameterManager.parameterForFieldID.")
##        return result

    # used by usection/PdSectionManager.parameterForSectionAndName
    def parameterForName(self, name):
        ''' return parameter from self.parameters where:
            - name matches (unique for a non header parameter). E.g. "Random sway in drawing angles"   '''
        result = None
        for parameter in self.parameters:
            if name.upper().strip() == parameter.name.upper().strip():
                result = parameter
                return result
        raise GeneralException.create("Problem: Parameter not found for name " + name + " in method PdParameterManager.parameterForName.")
        return result

##    def parameterIndexForFieldNumber(self, fieldNumber):
##        ''' return index into self.parameters where:
##            - fieldNumber matches (unique in range 1..399)   '''
##        result = 0
##        for i in range(0, len(self.parameters)):
##            parameter = self.parameters[i]
##            if fieldNumber == parameter.fieldNumber:
##                result = i
##                return result
##        raise GeneralException.create("Problem: Parameter index not found for field number %d in method PdParameterManager.parameterIndexForFieldNumber." % (fieldNumber))
##        return result
##
##    def parameterIndexForFieldID(self, fieldID):
##        ''' return index into self.parameters where:
##            - fieldID matches (unique for a parameter). E.g. "kGeneralRandomSway" '''
##        result = 0
##        for i in range(0, len(self.parameters)):
##            parameter = self.parameters[i]
##            if fieldID.upper().strip() == parameter.fieldID.upper().strip():
##                result = i
##                return result
##        raise GeneralException.create("Problem: Parameter index not found for field ID " + fieldID + " in method PdParameterManager.parameterIndexForFieldID.")
##        return result

    # used by udomain/PdDomain.startupLoading and on import (weirdly)
    def makeParameters(self):
        umakepm.CreateParameters(self)

