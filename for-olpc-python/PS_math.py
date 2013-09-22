### PS_math
### - used for SCurve data structure and safedivexcept, odd
### Dependencies:
###     - PS_sstream for reading Scurves only
###     - PS_support for reading Scurves only

import math

from PS_constants import *
import PS_sstream  # only used by Scurve.fromString
import PS_support


###---------------------------

# const
kPlantProximityNeeded = 4

# graphics
#CFK NOTE you may want to change this if you use this function
#  to actually click on plant parts
# this is not being used to select plant parts, the drawing surface is doing it
#!! check is using SinglePoints - them move to class
def pointsAreCloseEnough(point1, point2):
    result = false
    result = (abs(point1.X - point2.X) < kPlantProximityNeeded) and (abs(point1.Y - point2.Y) < kPlantProximityNeeded)
    return result


###----------------------------

# S curve support
class SCurveStructure(object):
    def __init__(self, x1=0.0, y1=0.0, x2=0.0, y2=0.0, c1=0.0, c2=0.0):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.c1 = c1
        self.c2 = c2

    def toString(self):
        return PS_support.digitValueString(self.x1) + " " + PS_support.digitValueString(self.y1) + " " + PS_support.digitValueString(self.x2) + " " + PS_support.digitValueString(self.y2)

    def fromString(self, aString):
        # format is x1 y1 x2 y2
        stream = PS_sstream.KfStringStream()
        stream.onStringSeparator(aString, " ")
        succesful, self.x1 = PS_support.boundForString(stream.nextToken(), kFieldFloat)
        succesful, self.y1 = PS_support.boundForString(stream.nextToken(), kFieldFloat)
        succesful, self.x2 = PS_support.boundForString(stream.nextToken(), kFieldFloat)
        succesful, self.y2 = PS_support.boundForString(stream.nextToken(), kFieldFloat)
        return(self)

    def calcSCurveCoeffs(self):
        if (0.0 < self.x1 < 1.0) and (0.0 < self.y1 < 1.0) and (0.0 < self.x2 < 1.0) and (0.0 < self.y2 < 1.0):
            xx = math.log(self.x1 / float(self.y1) - self.x1)
            self.c2 = (xx - math.log(self.x2 / float(self.y2) - self.x2)) / float(self.x2 - self.x1)
            self.c1 = xx + self.x1 * self.c2
        else:
            # instead of raising exception, just hard-code whole curve to acceptable values
            # don't use Parameters.tab default in case that was read in wrong also
            self.x1 = 0.25
            self.y1 = 0.1
            self.x2 = 0.65
            self.y2 = 0.85


# this function carries out a structure found in many EPIC equations.
def scurve(x, c1, c2):
    try:
        temp = c1 - c2 * x
        if temp > 85.0:
            temp = 85.0
            raise GeneralException.create("Problem: Exponent of number would have gone out of float range.")
        #result = safediv(x, x + safeExp(temp))
        result = x / ( x + math.exp(temp))
    except:
        # PDF PORT TEST
        raise
        result = ErrorMessage("Problem in s curve: numbers are %f, %f, and %f" % (x, c1, c2))
        raise
    return result


# enumerated const
kGetField = 0
kSetField = 1

def transferSCurveValue(direction, param, index, value):
    if (direction == kGetField):
        if index == 0:
            value = param.x1
        elif index == 1:
            value = param.y1
        elif index == 2:
            value = param.x2
        elif index == 3:
            value = param.y2
    else: # direction == kSetField
        if index == 0:
            param.x1 = value
        elif index == 1:
            param.y1 = value
        elif index == 2:
            param.x2 = value
        elif index == 3:
            param.y2 = value
    return value



#returns zero for convenience
#these consts are really defined in uplant.pas but we don't want to include it - keep current
# error message - returns zero for convenience
#!! should not be here... (PS_common..?)
def ErrorMessage(errorString):
    udebug.DebugPrint(errorString)
    return 0

# ---------------------------------------------------------------------------------------------- math functions

def odd(x):
    return x % 2 == 1


# same as safediv except that the user specifies what to return if the denominator is zero
def safedivExcept(x, y, exceptionResult):
    try:
        if (y != 0.0):
            result = 1.0 * x / y
        else:
            result = exceptionResult
    except:
        result = ErrorMessage("Problem in dividing %f by %f" % (x, y))
        raise
    return result





# same as scurve but does not show an errorMessage or re-raise the exception; just returns whether it failed;
#  used inside paint methods where you don't want error dialogs popping up
##def scurveWithResult(x, c1, c2, failed):
##    raise "function scurveWithResult with preexisting result had var parameters added to return; fixup manually"
##
##    failed = true
##    result = 0.0
##    temp = 0.0
##    try:
##        temp = c1 - c2 * x
##        if temp > 85.0:
##            return result, failed
##        temp = safeExpWithResult(temp, failed)
##        if failed:
##            return result, failed
##        temp = safedivWithResult(x, x + temp, failed)
##        if failed:
##            return result, failed
##    except:
##        return result, failed
##    failed = false
##    result = temp
##    return result, failed

# s curve params
# RE-RAISES EXCEPTION
# deal with zero s curve values by defaulting whole curve to hard-coded values
##def calcSCurveCoeffs(sCurve):
##    try:
##        if (sCurve.x1 <= 0.0) or (sCurve.y1 <= 0.0) or (sCurve.x2 <= 0.0) or (sCurve.y2 <= 0.0) or (sCurve.x1 >= 1.0) or (sCurve.y1 >= 1.0) or (sCurve.x2 >= 1.0) or (sCurve.y2 >= 1.0):
##            # instead of raising exception, just hard-code whole curve to acceptable values
##            # don't use Parameters.tab default in case that was read in wrong also
##            sCurve.x1 = 0.25
##            sCurve.y1 = 0.1
##            sCurve.x2 = 0.65
##            sCurve.y2 = 0.85
##        #xx = math.log(safediv(sCurve.x1, sCurve.y1) - sCurve.x1)
##        xx = math.log(sCurve.x1 / float(sCurve.y1) - sCurve.x1)
##        ##sCurve.c2 = safediv((xx - math.log(safediv(sCurve.x2, sCurve.y2) - sCurve.x2)), sCurve.x2 - sCurve.x1)
##        sCurve.c2 = (xx - math.log(sCurve.x2 / float(sCurve.y2) - sCurve.x2)) / float(sCurve.x2 - sCurve.x1)
##        sCurve.c1 = xx + sCurve.x1 * sCurve.c2
##    except Exception, e:
##        # set s curve to all acceptable values - safest
##        sCurve.x1 = 0.25
##        sCurve.y1 = 0.1
##        sCurve.x2 = 0.65
##        sCurve.y2 = 0.85
##        raise

### same as Utils_CalcSCurveCoeffs but does not show an errorMessage or re-raise the exception;
###  just returns whether it failed; used inside paint methods where you don't want error dialogs popping up
##def calcSCurveCoeffsWithResult(sCurve, failed):
##    failed = true
##    try:
##        quotientX1Y1 = safedivWithResult(sCurve.x1, sCurve.y1, failed)
##        if failed:
##            return failed
##        lnQuotientX1Y1MinusX1 = safeLnWithResult(quotientX1Y1 - sCurve.x1, failed)
##        if failed:
##            return failed
##        quotientX2Y2 = safedivWithResult(sCurve.x2, sCurve.y2, failed)
##        if failed:
##            return failed
##        lnQuotientX2Y2MinusX2 = safeLnWithResult(quotientX2Y2 - sCurve.x2, failed)
##        if failed:
##            return failed
##        c2temp = safedivWithResult(lnQuotientX1Y1MinusX1 - lnQuotientX2Y2MinusX2, sCurve.x2 - sCurve.x1, failed)
##        if failed:
##            return failed
##        c1temp = lnQuotientX1Y1MinusX1 + sCurve.x1 * c2temp
##    except:
##        return failed
##    sCurve.c1 = c1temp
##    sCurve.c2 = c2temp
##    failed = false
##    return failed


##def stringToSCurve(aString):
##    result = SCurveStructure()
##
##    result.x1 = 0
##    result.y1 = 0
##    result.x2 = 0
##    result.y2 = 0
##    result.c1 = 0
##    result.c2 = 0
##    # format is x1 y1 x2 y2
##    stream = PS_sstream.KfStringStream()
##    stream.onStringSeparator(aString, " ")
##    succesful, result.x1 = usupport.boundForString(stream.nextToken(), uparams.kFieldFloat)
##    succesful, result.y1 = usupport.boundForString(stream.nextToken(), uparams.kFieldFloat)
##    succesful, result.x2 = usupport.boundForString(stream.nextToken(), uparams.kFieldFloat)
##    succesful, result.y2 = usupport.boundForString(stream.nextToken(), uparams.kFieldFloat)
##    return result

##def sCurveToString(sCurve):
##    result = usupport.digitValueString(sCurve.x1) + " " + usupport.digitValueString(sCurve.y1) + " " + usupport.digitValueString(sCurve.x2) + " " + usupport.digitValueString(sCurve.y2)
##    return result




