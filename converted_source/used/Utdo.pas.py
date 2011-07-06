# unit Utdo

from conversion_common import *
import u3dexport
import u3dsupport
import uplant
import udebug
import usupport
import uclasses
import uturtle
import ufiler
import usstream
import ucollect
import delphi_compatability

# const
kMaximumRecordedPoints = 10000
kAdjustForOrigin = true
kDontAdjustForOrigin = false
kEmbeddedInPlant = true
kInTdoLibrary = false
kStandAloneFile = false
kTdoForeColor = delphi_compatability.clSilver
kTdoBackColor = delphi_compatability.clGray
kTdoLineContrastIndex = 10
kStartTdoString = "start 3D object"
kEndTdoString = "end 3D object"

# v1.6b2 changed from 200 to 1000 ; v2.0 changed to 10000 (not in tdo anymore)
# v1.11 moved up here
# v1.11 moved up here
# record
class KfPoint3D:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0

# ---------------------------------------------------------------------------------- KfPoint3D 
def KfPoint3D_setXYZ(thePoint, aX, aY, aZ):
    thePoint.x = aX
    thePoint.y = aY
    thePoint.z = aZ

def KfPoint3D_addXYZ(thePoint, xOffset, yOffset, zOffset):
    #pdf - shift point by x y and z.
    thePoint.x = thePoint.x + xOffset
    thePoint.y = thePoint.y + yOffset
    thePoint.z = thePoint.z + zOffset

def KfPoint3D_scaleBy(thePoint, aScale):
    #pdf - multiply point by scale.
    thePoint.x = thePoint.x * aScale
    thePoint.y = thePoint.y * aScale
    thePoint.z = thePoint.z * aScale

def KfPoint3D_subtract(thePoint, aPoint):
    #pdf - subtract point from this point.
    thePoint.x = thePoint.x - aPoint.x
    thePoint.y = thePoint.y - aPoint.y
    thePoint.z = thePoint.z - aPoint.z

def KfPoint3D_matchXYZ(pointOne, pointTwo, matchDistance):
    result = false
    # v1.6b1 added
    result = (abs(pointOne.x - pointTwo.x) <= matchDistance) and (abs(pointOne.y - pointTwo.y) <= matchDistance) and (abs(pointOne.z - pointTwo.z) <= matchDistance)
    return result

def KfPoint3D_addPointToBoundsRect(boundsRect, aPoint):
    x = 0L
    y = 0L
    
    try:
        x = intround(aPoint.x)
    except:
        x = 0
    try:
        y = intround(aPoint.y)
    except:
        y = 0
    if (boundsRect.Left == 0) and (boundsRect.Right == 0) and (boundsRect.Top == 0) and (boundsRect.Bottom == 0):
        # on first point entered, initialize bounds rect
        boundsRect.Left = x
        boundsRect.Right = x
        boundsRect.Top = y
        boundsRect.Bottom = y
    else:
        if x < boundsRect.Left:
            boundsRect.Left = x
        elif x > boundsRect.Right:
            boundsRect.Right = x
        if y < boundsRect.Top:
            boundsRect.Top = y
        elif y > boundsRect.Bottom:
            boundsRect.Bottom = y

# const
kPointAllocationIncrement = 8

def betweenBrackets(aString):
    result = ""
    # lose letter and [ on front, lose ] on back 
    result = UNRESOLVED.copy(aString, 3, len(aString) - 3)
    return result

class KfIndexTriangle(PdStreamableObject):
    def __init__(self):
        self.pointIndexes = [0] * (range(0, 2 + 1) + 1)
    
    # ---------------------------------------------------------------------------------- KfIndexTriangle 
    def createABC(self, a, b, c):
        self.create()
        self.pointIndexes[0] = a
        self.pointIndexes[1] = b
        self.pointIndexes[2] = c
        return self
    
    def flip(self):
        savePoint = 0L
        
        savePoint = self.pointIndexes[0]
        self.pointIndexes[0] = self.pointIndexes[2]
        self.pointIndexes[2] = savePoint
    
    def copyFrom(self, aTriangle):
        if aTriangle == None:
            return
        self.pointIndexes[0] = aTriangle.pointIndexes[0]
        self.pointIndexes[1] = aTriangle.pointIndexes[1]
        self.pointIndexes[2] = aTriangle.pointIndexes[2]
    
    def classAndVersionInformation(self, cvir):
        cvir.classNumber = uclasses.kKfIndexTriangle
        cvir.versionNumber = 0
        cvir.additionNumber = 0
    
    def streamDataWithFiler(self, filer, cvir):
        PdStreamableObject.streamDataWithFiler(self, filer, cvir)
        self.pointIndexes = filer.streamBytes(self.pointIndexes, FIX_sizeof(self.pointIndexes))
    
class KfObject3D(PdStreamableObject):
    def __init__(self):
        self.pointData = PKfPoint3DArray()
        self.pointsInUse = 0L
        self.pointsAllocated = 0L
        self.originPointIndex = 0L
        self.triangles = TListCollection()
        self.name = ""
        self.originalIfCopy = KfObject3D()
        self.inUse = false
        self.zForSorting = 0.0
        self.indexWhenRemoved = 0
        self.selectedIndexWhenRemoved = 0
        self.boundsRect = TRect()
    
    # doesn't need to be streamed, only used while drawing
    # ---------------------------------------------------------------------------------- KfObject3D 
    def create(self):
        PdStreamableObject.create(self)
        self.triangles = ucollect.TListCollection().Create()
        return self
    
    def destroy(self):
        self.triangles.free
        self.triangles = None
        if self.pointData != None:
            UNRESOLVED.FreeMem(self.pointData)
        PdStreamableObject.destroy(self)
    
    def ensureEnoughSpaceForNewPointData(self, totalNumberOfPointsToBeUsed):
        if self.pointsAllocated >= totalNumberOfPointsToBeUsed:
            return
        if self.pointData == None:
            if totalNumberOfPointsToBeUsed < kPointAllocationIncrement:
                totalNumberOfPointsToBeUsed = kPointAllocationIncrement
            # assuming this throws its own memory exception
            UNRESOLVED.GetMem(self.pointData, totalNumberOfPointsToBeUsed * FIX_sizeof(KfPoint3D))
        else:
            if totalNumberOfPointsToBeUsed % kPointAllocationIncrement != 0:
                totalNumberOfPointsToBeUsed = totalNumberOfPointsToBeUsed + kPointAllocationIncrement - (totalNumberOfPointsToBeUsed % kPointAllocationIncrement)
            UNRESOLVED.ReallocMem(self.pointData, totalNumberOfPointsToBeUsed * FIX_sizeof(KfPoint3D))
            # assuming this throws its own memory exception
        self.pointsAllocated = totalNumberOfPointsToBeUsed
    
    def getPoint(self, index):
        result = KfPoint3d()
        result = self.pointData.PDF_FIX_POINTER_ACCESS[index]
        return result
    
    def setPoint(self, index, aPoint):
        if self.pointData == None:
            raise GeneralException.create("Problem: Nil pointer in method KfObject3D.setPoint.")
        self.pointData.PDF_FIX_POINTER_ACCESS[index] = aPoint
    
    def clear(self):
        self.clearPoints()
        self.name = ""
    
    def clearPoints(self):
        self.pointsInUse = 0
        self.originPointIndex = 0
        self.triangles.clear()
    
    def copyFrom(self, original):
        i = 0
        theTriangle = KfIndexTriangle()
        
        if original == None:
            return
        self.setName(original.name)
        self.ensureEnoughSpaceForNewPointData(original.pointsInUse)
        if original.pointsInUse > 0:
            for i in range(0, original.pointsInUse):
                self.points[i] = original.points[i]
        self.pointsInUse = original.pointsInUse
        self.originPointIndex = original.originPointIndex
        self.triangles.clear()
        if original.triangles.Count > 0:
            for i in range(0, original.triangles.Count):
                theTriangle = original.triangles.Items[i]
                self.addTriangle(KfIndexTriangle().createABC(theTriangle.pointIndexes[0], theTriangle.pointIndexes[1], theTriangle.pointIndexes[2]))
        self.inUse = original.inUse
    
    def isSameAs(self, other):
        result = false
        i = 0L
        j = 0L
        thePoint = KfPoint3d()
        theTriangle = KfIndexTriangle()
        otherPoint = KfPoint3d()
        otherTriangle = KfIndexTriangle()
        
        #false if fails any test
        result = false
        if self.name != other.name:
            return result
        if self.pointsInUse != other.pointsInUse:
            return result
        if self.originPointIndex != other.originPointIndex:
            return result
        if self.triangles.Count != other.triangles.Count:
            return result
        if self.pointsInUse > 0:
            for i in range(0, self.pointsInUse):
                thePoint = self.points[i]
                otherPoint = other.points[i]
                if (intround(thePoint.x) != intround(otherPoint.x)) or (intround(thePoint.y) != intround(otherPoint.y)) or (intround(thePoint.z) != intround(otherPoint.z)):
                    # round these because otherwise i/o inaccuracies could make a tdo seem different when it isn't,
                    # and most numbers are far enough to be integers anyway
                    return result
        if self.triangles.Count > 0:
            for i in range(0, self.triangles.Count):
                theTriangle = self.triangles.Items[i]
                otherTriangle = other.triangles.Items[i]
                for j in range(0, 2 + 1):
                    if theTriangle.pointIndexes[j] != otherTriangle.pointIndexes[j]:
                        return result
        #passed all the tests
        result = true
        return result
    
    def getName(self):
        result = ""
        result = self.name
        return result
    
    def setName(self, newName):
        self.name = UNRESOLVED.copy(newName, 1, 80)
    
    def addPoint(self, aPoint):
        result = 0
        # v2.0 removed this check
        #if pointsInUse >= kMaximumRecordedPoints then
        #  raise Exception.create('Problem: Too many points in 3D object.');
        self.ensureEnoughSpaceForNewPointData(self.pointsInUse + 1)
        self.points[self.pointsInUse] = aPoint
        self.pointsInUse += 1
        result = self.pointsInUse
        return result
    
    def removePoint(self, point):
        i = 0
        
        if Point <= self.pointsInUse - 2:
            for i in range(Point, self.pointsInUse - 2 + 1):
                self.points[i] = self.points[i + 1]
        self.deletePointIndexInTriangles(Point)
        # never releasing memory until entire object freed
        self.pointsInUse -= 1
        if self.originPointIndex > self.pointsInUse - 1:
            self.originPointIndex = self.pointsInUse - 1
    
    def addPointIfNoMatch(self, aPoint, matchDistance):
        result = 0
        i = 0
        
        if self.pointsInUse > 0:
            for i in range(0, self.pointsInUse):
                if KfPoint3D_matchXYZ(aPoint, self.points[i], matchDistance):
                    #add 1 because triangle indexes start at 1
                    result = i + 1
                    return result
        result = self.addPoint(aPoint)
        return result
    
    #PDF FIX - may want to optimize this to use var to pass around result rather than assign
    def pointForIndex(self, anIndex):
        result = KfPoint3D()
        if (anIndex < 1) or (anIndex > self.pointsInUse):
            raise GeneralException.create("Problem: Point index out of range in method KfObject3D.pointForIndex.")
        result = self.points[anIndex - 1]
        return result
    
    def addTriangle(self, aTriangle):
        self.triangles.Add(aTriangle)
    
    def triangleForIndex(self, anIndex):
        result = KfIndexTriangle()
        if (anIndex < 1) or (anIndex > self.triangles.Count):
            raise GeneralException.create("Problem: Triangle index out of range in method KfObject3D.triangleForIndex.")
        result = self.triangles.Items[anIndex - 1]
        return result
    
    #adjust all points for origin, which is assumed to be at the first point
    #in terms of plant organs, this means the first point is
    #where the organ is attached to the plant
    def adjustForOrigin(self):
        i = 0L
        tempPoint = KfPoint3d()
        
        if self.pointsInUse < 1:
            return
        if self.originPointIndex < 0:
            self.originPointIndex = 0
        if self.originPointIndex > self.pointsInUse - 1:
            self.originPointIndex = self.pointsInUse - 1
        if self.pointsInUse > 1:
            for i in range(0, self.pointsInUse):
                if i != self.originPointIndex:
                    tempPoint = self.points[i]
                    KfPoint3D_subtract(tempPoint, self.points[self.originPointIndex])
                    self.points[i] = tempPoint
        #makes the first point zero
        tempPoint = self.points[self.originPointIndex]
        KfPoint3D_setXYZ(tempPoint, 0.0, 0.0, 0.0)
        self.points[self.originPointIndex] = tempPoint
    
    def setOriginPointIndex(self, newOriginPointIndex):
        changed = false
        
        changed = (self.originPointIndex != newOriginPointIndex)
        self.originPointIndex = newOriginPointIndex
        if changed:
            self.adjustForOrigin()
    
    def makeMirrorTriangles(self):
        triangleCountAtStart = 0
        newPointIndexes = [0] * (range(0, 2 + 1) + 1)
        i = 0
        j = 0
        aPoint = KfPoint3D()
        triangle = KfIndexTriangle()
        
        self.adjustForOrigin()
        triangleCountAtStart = self.triangles.Count
        if triangleCountAtStart > 0:
            for i in range(0, triangleCountAtStart):
                triangle = KfIndexTriangle(self.triangles[i])
                for j in range(0, 2 + 1):
                    aPoint = self.pointForIndex(triangle.pointIndexes[j])
                    aPoint.x = -1 * aPoint.x
                    newPointIndexes[j] = self.addPointIfNoMatch(aPoint, 1.0)
                # reversing order of points makes triangle have correct facing for opposite side
                self.addTriangle(KfIndexTriangle().createABC(newPointIndexes[2], newPointIndexes[1], newPointIndexes[0]))
    
    def reverseZValues(self):
        i = 0
        tempPoint = KfPoint3d()
        
        self.adjustForOrigin()
        if self.pointsInUse > 0:
            for i in range(0, self.pointsInUse):
                tempPoint = self.points[i]
                tempPoint.z = -1 * tempPoint.z
                self.points[i] = tempPoint
    
    def bestPointForDrawingAtScale(self, turtleProxy, origin, bitmapSize, scale):
        result = TPoint()
        i = 0L
        turtle = KfTurtle()
        
        turtle = uturtle.KfTurtle(turtleProxy)
        self.boundsRect = Rect(0, 0, 0, 0)
        turtle.reset()
        if self.pointsInUse > 0:
            for i in range(0, self.pointsInUse):
                KfPoint3D_addPointToBoundsRect(self.boundsRect, turtle.transformAndRecord(self.points[i], scale))
        result.X = origin.X + bitmapSize.X / 2 - usupport.rWidth(self.boundsRect) / 2 - self.boundsRect.Left
        result.Y = origin.Y + bitmapSize.Y / 2 - usupport.rHeight(self.boundsRect) / 2 - self.boundsRect.Top
        return result
    
    def draw(self, turtleProxy, scale, longName, shortName, dxfIndex, partID):
        result = TRect()
        i = 0L
        triangle = KfIndexTriangle()
        realTriangle = KfTriangle()
        turtle = KfTurtle()
        minZ = 0.0
        
        result = Rect(0, 0, 0, 0)
        minZ = 0
        self.zForSorting = 0
        turtle = uturtle.KfTurtle(turtleProxy)
        if turtle.ifExporting_exclude3DObject(scale):
            return result
        turtle.clearRecording()
        self.boundsRect = Rect(0, 0, 0, 0)
        if self.pointsInUse > 0:
            for i in range(0, self.pointsInUse):
                KfPoint3D_addPointToBoundsRect(self.boundsRect, turtle.transformAndRecord(self.points[i], scale))
        result = self.boundsRect
        if not turtle.drawOptions.draw3DObjects:
            return result
        if turtle.drawOptions.draw3DObjectsAsRects:
            turtle.drawTrianglesFromBoundsRect(self.boundsRect)
            return result
        # prepare
        turtle.ifExporting_start3DObject(longName + " 3D object", shortName, turtle.drawingSurface.foreColor, dxfIndex)
        if turtle.exportingToFile():
            # draw
            self.write3DExportElements(turtle, scale, partID)
        elif self.triangles.Count > 0:
            for i in range(1, self.triangles.Count + 1):
                triangle = self.triangleForIndex(i)
                realTriangle = turtle.drawTriangleFromIndexes(triangle.pointIndexes[0], triangle.pointIndexes[1], triangle.pointIndexes[2], partID)
                if (turtle.drawOptions.sortPolygons) and (turtle.drawOptions.sortTdosAsOneItem) and (realTriangle != None):
                    if i == 1:
                        minZ = realTriangle.zForSorting
                    elif realTriangle.zForSorting < minZ:
                        minZ = realTriangle.zForSorting
                    realTriangle.tdo = self
        self.zForSorting = minZ
        turtle.ifExporting_end3DObject()
        return result
    
    def overlayBoundsRect(self, turtleProxy, scale):
        i = 0L
        turtle = KfTurtle()
        oldSetting = false
        
        turtle = uturtle.KfTurtle(turtleProxy)
        oldSetting = turtle.drawingSurface.fillingTriangles
        turtle.drawingSurface.fillingTriangles = false
        turtle.drawTrianglesFromBoundsRect(self.boundsRect)
        turtle.drawingSurface.fillingTriangles = oldSetting
    
    def write3DExportElements(self, turtleProxy, scale, partID):
        fileExportSurface = KfFileExportSurface()
        i = 0
        turtle = KfTurtle()
        triangle = KfIndexTriangle()
        firstPtIndex = 0L
        
        # do NOT pass the array on because a tdo could be really big
        # some write out lists of points then triangles; some draw each triangle
        turtle = uturtle.KfTurtle(turtleProxy)
        fileExportSurface = turtle.fileExportSurface()
        if fileExportSurface == None:
            raise GeneralException.create("Problem: No 3D drawing surface in method KfObject3D.write3DExportElements.")
        if turtle.writingTo == u3dexport.k3DS:
            fileExportSurface.startVerticesAndTriangles()
            if turtle.writingToLWO():
                firstPtIndex = fileExportSurface.numPoints
            else:
                firstPtIndex = 0
            if self.pointsInUse > 0:
                for i in range(0, self.pointsInUse):
                    fileExportSurface.addPoint(turtle.transformAndRecord(self.points[i], scale))
            for i in range(1, self.triangles.Count + 1):
                triangle = self.triangleForIndex(i)
                fileExportSurface.addTriangle(firstPtIndex + triangle.pointIndexes[0] - 1, firstPtIndex + triangle.pointIndexes[1] - 1, firstPtIndex + triangle.pointIndexes[2] - 1)
                if fileExportSurface.options.makeTrianglesDoubleSided:
                    fileExportSurface.addTriangle(firstPtIndex + triangle.pointIndexes[0] - 1, firstPtIndex + triangle.pointIndexes[2] - 1, firstPtIndex + triangle.pointIndexes[1] - 1)
            fileExportSurface.endVerticesAndTriangles()
            # PDF PORT -- added semicolon
        elif turtle.writingTo == u3dexport.kOBJ:
            fileExportSurface.startVerticesAndTriangles()
            if turtle.writingToLWO():
                firstPtIndex = fileExportSurface.numPoints
            else:
                firstPtIndex = 0
            if self.pointsInUse > 0:
                for i in range(0, self.pointsInUse):
                    fileExportSurface.addPoint(turtle.transformAndRecord(self.points[i], scale))
            for i in range(1, self.triangles.Count + 1):
                triangle = self.triangleForIndex(i)
                fileExportSurface.addTriangle(firstPtIndex + triangle.pointIndexes[0] - 1, firstPtIndex + triangle.pointIndexes[1] - 1, firstPtIndex + triangle.pointIndexes[2] - 1)
                if fileExportSurface.options.makeTrianglesDoubleSided:
                    fileExportSurface.addTriangle(firstPtIndex + triangle.pointIndexes[0] - 1, firstPtIndex + triangle.pointIndexes[2] - 1, firstPtIndex + triangle.pointIndexes[1] - 1)
            fileExportSurface.endVerticesAndTriangles()
            # PDF PORT -- added semicolon
        elif turtle.writingTo == u3dexport.kVRML:
            fileExportSurface.startVerticesAndTriangles()
            if turtle.writingToLWO():
                firstPtIndex = fileExportSurface.numPoints
            else:
                firstPtIndex = 0
            if self.pointsInUse > 0:
                for i in range(0, self.pointsInUse):
                    fileExportSurface.addPoint(turtle.transformAndRecord(self.points[i], scale))
            for i in range(1, self.triangles.Count + 1):
                triangle = self.triangleForIndex(i)
                fileExportSurface.addTriangle(firstPtIndex + triangle.pointIndexes[0] - 1, firstPtIndex + triangle.pointIndexes[1] - 1, firstPtIndex + triangle.pointIndexes[2] - 1)
                if fileExportSurface.options.makeTrianglesDoubleSided:
                    fileExportSurface.addTriangle(firstPtIndex + triangle.pointIndexes[0] - 1, firstPtIndex + triangle.pointIndexes[2] - 1, firstPtIndex + triangle.pointIndexes[1] - 1)
            fileExportSurface.endVerticesAndTriangles()
            # PDF PORT -- added semicolon
        elif turtle.writingTo == u3dexport.kLWO:
            fileExportSurface.startVerticesAndTriangles()
            if turtle.writingToLWO():
                firstPtIndex = fileExportSurface.numPoints
            else:
                firstPtIndex = 0
            if self.pointsInUse > 0:
                for i in range(0, self.pointsInUse):
                    fileExportSurface.addPoint(turtle.transformAndRecord(self.points[i], scale))
            for i in range(1, self.triangles.Count + 1):
                triangle = self.triangleForIndex(i)
                fileExportSurface.addTriangle(firstPtIndex + triangle.pointIndexes[0] - 1, firstPtIndex + triangle.pointIndexes[1] - 1, firstPtIndex + triangle.pointIndexes[2] - 1)
                if fileExportSurface.options.makeTrianglesDoubleSided:
                    fileExportSurface.addTriangle(firstPtIndex + triangle.pointIndexes[0] - 1, firstPtIndex + triangle.pointIndexes[2] - 1, firstPtIndex + triangle.pointIndexes[1] - 1)
            fileExportSurface.endVerticesAndTriangles()
            # PDF PORT -- added semicolon
        else :
            for i in range(1, self.triangles.Count + 1):
                triangle = self.triangleForIndex(i)
                turtle.drawTriangleFromIndexes(triangle.pointIndexes[0], triangle.pointIndexes[1], triangle.pointIndexes[2], partID)
                if fileExportSurface.options.makeTrianglesDoubleSided:
                    turtle.drawTriangleFromIndexes(triangle.pointIndexes[0], triangle.pointIndexes[2], triangle.pointIndexes[1], partID)
    
    def addTriangleWithVerticesABC(self, a, b, c):
        self.addTriangle(KfIndexTriangle().createABC(a, b, c))
    
    def removeTriangle(self, aTriangle):
        self.triangles.Remove(aTriangle)
        self.removePointsNotInUse()
    
    def removePointsNotInUse(self):
        i = 0
        pointToRemove = 0
        done = false
        
        if self.pointsInUse <= 0:
            return
        done = false
        while not done:
            pointToRemove = -1
            for i in range(0, self.pointsInUse):
                if not self.pointIsReallyInUse(i):
                    pointToRemove = i
                    break
            if pointToRemove >= 0:
                self.removePoint(pointToRemove)
            else:
                done = true
    
    def pointIsReallyInUse(self, point):
        result = false
        triangle = KfIndexTriangle()
        i = 0
        j = 0
        adjustedPoint = 0
        
        result = false
        # triangle indexes start at 1, not 0 
        adjustedPoint = Point + 1
        if self.triangles.Count > 0:
            for i in range(0, self.triangles.Count):
                triangle = KfIndexTriangle(self.triangles.Items[i])
                for j in range(0, 2 + 1):
                    if triangle.pointIndexes[j] == adjustedPoint:
                        result = true
                        return result
        return result
    
    def deletePointIndexInTriangles(self, oldPointIndex):
        triangle = KfIndexTriangle()
        i = 0
        j = 0
        adjustedOldPointIndex = 0
        
        # triangle indexes start at 1, not 0 
        adjustedOldPointIndex = oldPointIndex + 1
        if self.triangles.Count > 0:
            for i in range(0, self.triangles.Count):
                triangle = KfIndexTriangle(self.triangles.Items[i])
                for j in range(0, 2 + 1):
                    if triangle.pointIndexes[j] > adjustedOldPointIndex:
                        triangle.pointIndexes[j] = triangle.pointIndexes[j] - 1
    
    #parse string into xyz positions and add point to collection
    def addPointString(self, stream):
        aPoint3D = KfPoint3D()
        x = 0
        y = 0
        z = 0
        
        x = 0
        y = 0
        z = 0
        x = stream.nextInteger()
        y = stream.nextInteger()
        z = stream.nextInteger()
        KfPoint3D_setXYZ(aPoint3D, x, y, z)
        self.addPoint(aPoint3D)
    
    #parse string into three point indexes and add triangle to collection
    def addTriangleString(self, stream):
        p1 = 0
        p2 = 0
        p3 = 0
        
        p1 = 0
        p2 = 0
        p3 = 0
        p1 = stream.nextInteger()
        p2 = stream.nextInteger()
        p3 = stream.nextInteger()
        if (p1 == 0) or (p2 == 0) or (p3 == 0) or (p1 > self.pointsInUse) or (p2 > self.pointsInUse) or (p3 > self.pointsInUse):
            MessageDialog("Bad triangle: " + IntToStr(p1) + " " + IntToStr(p2) + " " + IntToStr(p3) + ". Point indexes must be between 1 and " + IntToStr(self.pointsInUse) + ".", delphi_compatability.TMsgDlgType.mtError, [mbOK, ], 0)
        else:
            self.addTriangle(KfIndexTriangle().createABC(p1, p2, p3))
    
    def writeToFile(self, fileName):
        outputFile = TextFile()
        
        AssignFile(outputFile, fileName)
        try:
            # v1.5
            usupport.setDecimalSeparator()
            Rewrite(outputFile)
            self.writeToFileStream(outputFile, kStandAloneFile)
        finally:
            CloseFile(outputFile)
    
    def readFromFile(self, fileName):
        inputFile = TextFile()
        
        AssignFile(inputFile, fileName)
        try:
            # v1.5
            usupport.setDecimalSeparator()
            Reset(inputFile)
            self.readFromFileStream(inputFile, kStandAloneFile)
        finally:
            CloseFile(inputFile)
    
    def writeToMemo(self, aMemo):
        i = 0
        triangle = KfIndexTriangle()
        
        aMemo.Lines.Add("  " + kStartTdoString)
        aMemo.Lines.Add("  Name=" + self.getName())
        if self.pointsInUse > 0:
            for i in range(0, self.pointsInUse):
                aMemo.Lines.Add("  Point=" + IntToStr(intround(self.points[i].x)) + " " + IntToStr(intround(self.points[i].y)) + " " + IntToStr(intround(self.points[i].z)))
        aMemo.Lines.Add("; Origin=" + IntToStr(self.originPointIndex))
        if self.triangles.Count > 0:
            for i in range(0, self.triangles.Count):
                triangle = KfIndexTriangle(self.triangles[i])
                aMemo.Lines.Add("  Triangle=" + IntToStr(triangle.pointIndexes[0]) + " " + IntToStr(triangle.pointIndexes[1]) + " " + IntToStr(triangle.pointIndexes[2]))
        aMemo.Lines.Add("  " + kEndTdoString)
    
    def writeToFileStream(self, outputFile, embeddedInPlant):
        i = 0
        triangle = KfIndexTriangle()
        
        if embeddedInPlant:
            writeln(outputFile, "  " + kStartTdoString)
        if embeddedInPlant:
            write(outputFile, "  ")
        writeln(outputFile, "Name=" + self.getName())
        if self.pointsInUse > 0:
            for i in range(0, self.pointsInUse):
                writeln(outputFile, "  Point=" + IntToStr(intround(self.points[i].x)) + " " + IntToStr(intround(self.points[i].y)) + " " + IntToStr(intround(self.points[i].z)))
        writeln(outputFile, "; Origin=" + IntToStr(self.originPointIndex))
        if self.triangles.Count > 0:
            for i in range(0, self.triangles.Count):
                triangle = KfIndexTriangle(self.triangles[i])
                writeln(outputFile, "  Triangle=" + IntToStr(triangle.pointIndexes[0]) + " " + IntToStr(triangle.pointIndexes[1]) + " " + IntToStr(triangle.pointIndexes[2]))
        if embeddedInPlant:
            writeln(outputFile, "  " + kEndTdoString)
        else:
            writeln(outputFile)
    
    def readFromFileStream(self, inputFile, embeddedInPlant):
        inputLine = ""
        fieldType = ""
        stream = KfStringStream()
        
        self.pointsInUse = 0
        self.originPointIndex = 0
        self.triangles.clear()
        if embeddedInPlant:
            UNRESOLVED.readln(inputFile, inputLine)
            if (embeddedInPlant) and (trim(inputLine) == ""):
                # cfk change for v1.3 added '' case
                UNRESOLVED.readln(inputFile, inputLine)
            if (UNRESOLVED.copy(inputLine, 1, 1) == ";") and (UNRESOLVED.pos("ORIGIN", uppercase(inputLine)) <= 0):
                # cfk change for v1.6b2 mistake with origin, placed with comment
                UNRESOLVED.readln(inputFile, inputLine)
            if UNRESOLVED.pos(uppercase(kStartTdoString), uppercase(inputLine)) <= 0:
                raise GeneralException.create("Problem: Expected start of 3D object.")
        stream = None
        try:
            #read info for 3D object from file at current position
            stream = usstream.KfStringStream.create
            while not UNRESOLVED.eof(inputFile):
                UNRESOLVED.readln(inputFile, inputLine)
                if (embeddedInPlant) and (trim(inputLine) == ""):
                    # cfk change v1.3 added '' case
                    continue
                if (UNRESOLVED.copy(inputLine, 1, 1) == ";") and (UNRESOLVED.pos("ORIGIN", uppercase(inputLine)) <= 0):
                    # cfk change for v1.6b2 mistake with origin, placed with comment
                    continue
                if (not embeddedInPlant) and (UNRESOLVED.pos("[", inputLine) == 1):
                    #ignore old thing in brackets
                    continue
                stream.onStringSeparator(inputLine, "=")
                fieldType = stream.nextToken()
                stream.spaceSeparator()
                if UNRESOLVED.pos("POINT", uppercase(fieldType)) > 0:
                    self.addPointString(stream)
                elif UNRESOLVED.pos("ORIGIN", uppercase(fieldType)) > 0:
                    self.setOriginPointIndex(StrToIntDef(stream.remainder, 0))
                elif UNRESOLVED.pos("TRIANGLE", uppercase(fieldType)) > 0:
                    self.addTriangleString(stream)
                elif UNRESOLVED.pos("NAME", uppercase(fieldType)) > 0:
                    self.setName(stream.remainder)
                else:
                    break
            self.adjustForOrigin()
            if embeddedInPlant:
                if UNRESOLVED.pos(uppercase(kEndTdoString), uppercase(inputLine)) <= 0:
                    raise GeneralException.create("Problem: Expected end of 3D object.")
        finally:
            stream.free
    
    def readFromDXFFile(self, inputFile):
        identifierLine = ""
        valueLine = ""
        newPoints = [0] * (range(0, 2 + 1) + 1)
        newTriangleIndexes = [0] * (range(0, 2 + 1) + 1)
        pointsRead = 0
        
        self.pointsInUse = 0
        self.originPointIndex = 0
        pointsRead = 0
        self.triangles.clear()
        newPoints[0].x = 0
        newPoints[0].y = 0
        newPoints[0].z = 0
        newPoints[1].x = 0
        newPoints[1].y = 0
        newPoints[1].z = 0
        newPoints[2].x = 0
        newPoints[2].y = 0
        newPoints[2].z = 0
        while not UNRESOLVED.eof(inputFile):
            UNRESOLVED.readln(inputFile, identifierLine)
            identifierLine = trim(identifierLine)
            UNRESOLVED.readln(inputFile, valueLine)
            valueLine = trim(valueLine)
            if identifierLine == "10":
                # v1.60final changed this from else to all ifs; something wrong in Delphi, I think
                # first point
                newPoints[0].x = StrToFloat(valueLine)
            if identifierLine == "20":
                newPoints[0].y = -1 * StrToFloat(valueLine)
            if identifierLine == "30":
                newPoints[0].z = StrToFloat(valueLine)
            if identifierLine == "11":
                # second point
                newPoints[1].x = StrToFloat(valueLine)
            if identifierLine == "21":
                newPoints[1].y = -1 * StrToFloat(valueLine)
            if identifierLine == "31":
                newPoints[1].z = StrToFloat(valueLine)
            if identifierLine == "12":
                # third point
                newPoints[2].x = StrToFloat(valueLine)
            if identifierLine == "22":
                newPoints[2].y = -1 * StrToFloat(valueLine)
            if identifierLine == "32":
                newPoints[2].z = StrToFloat(valueLine)
            if identifierLine == "13":
                # end (ignoring fourth point)
                pointsRead += 3
                # make new triangle
                newTriangleIndexes[0] = self.addPointIfNoMatch(newPoints[0], 0.1)
                newTriangleIndexes[1] = self.addPointIfNoMatch(newPoints[1], 0.1)
                newTriangleIndexes[2] = self.addPointIfNoMatch(newPoints[2], 0.1)
                self.addTriangle(KfIndexTriangle().createABC(newTriangleIndexes[0], newTriangleIndexes[1], newTriangleIndexes[2]))
                # reset points for next time
                newPoints[0].x = 0
                newPoints[0].y = 0
                newPoints[0].z = 0
                newPoints[1].x = 0
                newPoints[1].y = 0
                newPoints[1].z = 0
                newPoints[2].x = 0
                newPoints[2].y = 0
                newPoints[2].z = 0
        self.adjustForOrigin()
    
    def readFromMemo(self, aMemo, readingMemoLine):
        inputLine = ""
        fieldType = ""
        stream = KfStringStream()
        
        self.pointsInUse = 0
        self.originPointIndex = 0
        self.triangles.clear()
        inputLine = aMemo.Lines.Strings[readingMemoLine]
        readingMemoLine += 1
        if trim(inputLine) == "":
            # cfk change v1.60final added '' case
            # skip commented lines 
            inputLine = aMemo.Lines.Strings[readingMemoLine]
            readingMemoLine += 1
        if (UNRESOLVED.copy(inputLine, 1, 1) == ";") and (UNRESOLVED.pos("ORIGIN", uppercase(inputLine)) <= 0):
            # cfk change for v1.6b2 mistake with origin, placed with comment
            # skip commented lines 
            inputLine = aMemo.Lines.Strings[readingMemoLine]
            readingMemoLine += 1
        if UNRESOLVED.pos(uppercase(kStartTdoString), uppercase(inputLine)) <= 0:
            raise GeneralException.create("Problem: Expected start of 3D object.")
        stream = None
        try:
            #read info for 3D object from file at current position
            stream = usstream.KfStringStream.create
            while readingMemoLine <= aMemo.Lines.Count - 1:
                inputLine = aMemo.Lines.Strings[readingMemoLine]
                readingMemoLine += 1
                if trim(inputLine) == "":
                    # cfk change v1.60final added '' case
                    continue
                if (UNRESOLVED.copy(inputLine, 1, 1) == ";") and (UNRESOLVED.pos("ORIGIN", uppercase(inputLine)) <= 0):
                    # cfk change for v1.6b2 mistake with origin, placed with comment
                    # skip commented lines 
                    continue
                stream.onStringSeparator(inputLine, "=")
                fieldType = stream.nextToken()
                stream.spaceSeparator()
                if UNRESOLVED.pos("POINT", uppercase(fieldType)) > 0:
                    self.addPointString(stream)
                elif UNRESOLVED.pos("ORIGIN", uppercase(fieldType)) > 0:
                    self.setOriginPointIndex(StrToIntDef(stream.remainder, 0))
                elif UNRESOLVED.pos("TRIANGLE", uppercase(fieldType)) > 0:
                    self.addTriangleString(stream)
                elif UNRESOLVED.pos("NAME", uppercase(fieldType)) > 0:
                    self.setName(stream.remainder)
                else:
                    break
            self.adjustForOrigin()
            if UNRESOLVED.pos(uppercase(kEndTdoString), uppercase(inputLine)) <= 0:
                raise GeneralException.create("Problem: Expected end of 3D object.")
        finally:
            stream.free
        return readingMemoLine
    
    def readFromInputString(self, aString, doAdjustForOrigin):
        part = ""
        firstLetter = ""
        stream = KfStringStream()
        partStream = KfStringStream()
        
        # format is n[name],p[# # #],p[# # #],p[# # #],t[# # #],t[# # #],t[# # #] 
        self.pointsInUse = 0
        self.originPointIndex = 0
        self.triangles.clear()
        stream = usstream.KfStringStream.create
        partStream = usstream.KfStringStream.create
        try:
            stream.onStringSeparator(aString, ",")
            part = "none"
            while part != "":
                part = stream.nextToken()
                firstLetter = UNRESOLVED.copy(part, 1, 1)
                if uppercase(firstLetter) == "N":
                    self.setName(betweenBrackets(part))
                elif uppercase(firstLetter) == "P":
                    partStream.onStringSeparator(betweenBrackets(part), " ")
                    self.addPointString(partStream)
                elif uppercase(firstLetter) == "T":
                    partStream.onStringSeparator(betweenBrackets(part), " ")
                    self.addTriangleString(partStream)
            if doAdjustForOrigin:
                self.adjustForOrigin()
        finally:
            stream.free
            partStream.free
    
    # ------------------------------------------------------------------------- data transfer for binary copy 
    def classAndVersionInformation(self, cvir):
        cvir.classNumber = uclasses.kKfObject3D
        cvir.versionNumber = 0
        cvir.additionNumber = 0
    
    def streamDataWithFiler(self, filer, cvir):
        i = 0
        tempPoint = KfPoint3d()
        
        PdStreamableObject.streamDataWithFiler(self, filer, cvir)
        self.name = filer.streamShortString(self.name)
        self.pointsInUse = filer.streamLongint(self.pointsInUse)
        self.originPointIndex = filer.streamLongint(self.originPointIndex)
        self.ensureEnoughSpaceForNewPointData(self.pointsInUse)
        if self.pointsInUse > 0:
            for i in range(0, self.pointsInUse):
                if filer.isWriting():
                    tempPoint = self.points[i]
                tempPoint = filer.streamBytes(tempPoint, FIX_sizeof(tempPoint))
                if filer.isReading():
                    self.points[i] = tempPoint
        if filer.isReading():
            #may have triangles already, because we are keeping them around now
            self.triangles.clear()
        self.triangles.streamUsingFiler(filer, KfIndexTriangle)
    
    def totalMemorySize(self):
        result = 0L
        i = 0L
        
        result = self.instanceSize
        result = result + self.triangles.instanceSize
        if self.triangles.Count > 0:
            for i in range(0, self.triangles.Count):
                result = result + KfIndexTriangle(self.triangles.Items[i]).instanceSize
        result = result + self.pointsAllocated * FIX_sizeof(KfPoint3D)
        return result
    
    def writeToDXFFile(self, fileName, frontFaceColor, backFaceColor):
        outputFile = TextFile()
        i = 0
        triangle = KfIndexTriangle()
        colorToDraw = TColorRef()
        
        AssignFile(outputFile, fileName)
        try:
            # v1.5
            usupport.setDecimalSeparator()
            Rewrite(outputFile)
            writeln(outputFile, "0")
            writeln(outputFile, "SECTION")
            writeln(outputFile, "2")
            writeln(outputFile, "ENTITIES")
            for i in range(0, self.triangles.Count):
                triangle = KfIndexTriangle(self.triangles.Items[i])
                if self.triangleIsBackFacing(triangle):
                    colorToDraw = backFaceColor
                else:
                    colorToDraw = frontFaceColor
                self.writeTriangleToDXFFIle(outputFile, self.points[triangle.pointIndexes[0] - 1], self.points[triangle.pointIndexes[1] - 1], self.points[triangle.pointIndexes[2] - 1], colorToDraw)
            writeln(outputFile, "0")
            writeln(outputFile, "ENDSEC")
            writeln(outputFile, "0")
            writeln(outputFile, "EOF")
        finally:
            CloseFile(outputFile)
    
    def writeTriangleToDXFFIle(self, outputFile, p1, p2, p3, color):
        writeln(outputFile, "0")
        writeln(outputFile, "3DFACE")
        writeln(outputFile, "8")
        writeln(outputFile, "3dObject")
        writeln(outputFile, "62")
        writeln(outputFile, IntToStr(color))
        # v1.60final changed intToStr(round(p|.|)) to digitValueString(p|.|)
        # can't see that there was ever any reason to round these; it's probably left over from
        # when I didn't understand DXF very well
        writeln(outputFile, "10")
        writeln(outputFile, usupport.digitValueString(p1.x))
        writeln(outputFile, "20")
        writeln(outputFile, usupport.digitValueString(-p1.y))
        writeln(outputFile, "30")
        writeln(outputFile, usupport.digitValueString(p1.z))
        writeln(outputFile, "11")
        writeln(outputFile, usupport.digitValueString(p2.x))
        writeln(outputFile, "21")
        writeln(outputFile, usupport.digitValueString(-p2.y))
        writeln(outputFile, "31")
        writeln(outputFile, usupport.digitValueString(p2.z))
        writeln(outputFile, "12")
        writeln(outputFile, usupport.digitValueString(p3.x))
        writeln(outputFile, "22")
        writeln(outputFile, usupport.digitValueString(-p3.y))
        writeln(outputFile, "32")
        writeln(outputFile, usupport.digitValueString(p3.z))
        writeln(outputFile, "13")
        writeln(outputFile, usupport.digitValueString(p3.x))
        writeln(outputFile, "23")
        writeln(outputFile, usupport.digitValueString(-p3.y))
        writeln(outputFile, "33")
        writeln(outputFile, usupport.digitValueString(p3.z))
    
    def writeToPOV_INCFile(self, fileName, frontFaceColor, embeddedInPlant, rotateCount):
        outputFile = TextFile()
        i = 0
        triangle = KfIndexTriangle()
        colorToDraw = TColorRef()
        nameString = ""
        
        AssignFile(outputFile, fileName)
        try:
            # v1.5
            usupport.setDecimalSeparator()
            Rewrite(outputFile)
            nameString = usupport.replacePunctuationWithUnderscores(self.getName())
            writeln(outputFile, "// POV-format INC file of PlantStudio v1.x 3D object")
            writeln(outputFile, "//     \"" + self.getName() + "\"")
            if (not embeddedInPlant):
                writeln(outputFile, "// include this file in a POV file thus to use it:")
                writeln(outputFile, "//     #include \"" + usupport.stringUpTo(ExtractFileName(fileName), ".") + ".inc\"")
                writeln(outputFile, "//     object { " + nameString + " }")
                if rotateCount > 1:
                    writeln(outputFile, "//  or")
                    writeln(outputFile, "//     object { " + nameString + "_rotated }")
                writeln(outputFile)
            writeln(outputFile, "#declare " + nameString + "=mesh {")
            for i in range(0, self.triangles.Count):
                triangle = KfIndexTriangle(self.triangles.Items[i])
                self.writeTriangleToPOV_INCFIle(outputFile, self.points[triangle.pointIndexes[0] - 1], self.points[triangle.pointIndexes[1] - 1], self.points[triangle.pointIndexes[2] - 1])
            writeln(outputFile, chr(9) + "pigment { color rgb <" + usupport.digitValueString(UNRESOLVED.getRValue(frontFaceColor) / 256.0) + ", " + usupport.digitValueString(UNRESOLVED.getGValue(frontFaceColor) / 256.0) + ", " + usupport.digitValueString(UNRESOLVED.getBValue(frontFaceColor) / 256.0) + "> }")
            writeln(outputFile, "}")
            if rotateCount > 1:
                writeln(outputFile)
                writeln(outputFile, "#declare " + nameString + "_rotated=union {")
                writeln(outputFile, chr(9) + "object { " + nameString + " }")
                for i in range(1, rotateCount):
                    writeln(outputFile, chr(9) + "object { " + nameString + " rotate " + IntToStr(i) + "*365/" + IntToStr(rotateCount) + "*y }")
                writeln(outputFile, "}")
        finally:
            CloseFile(outputFile)
    
    def writeTriangleToPOV_INCFIle(self, outputFile, p1, p2, p3):
        write(outputFile, chr(9) + "triangle { <")
        # all y values must be negative because it seems our coordinate systems are different
        write(outputFile, IntToStr(intround(p1.x)) + ", " + IntToStr(-intround(p1.y)) + ", " + IntToStr(intround(p1.z)) + ">, <")
        write(outputFile, IntToStr(intround(p2.x)) + ", " + IntToStr(-intround(p2.y)) + ", " + IntToStr(intround(p2.z)) + ">, <")
        writeln(outputFile, IntToStr(intround(p3.x)) + ", " + IntToStr(-intround(p3.y)) + ", " + IntToStr(intround(p3.z)) + "> }")
    
    def triangleIsBackFacing(self, aTriangle):
        result = false
        point0 = KfPoint3d()
        point1 = KfPoint3d()
        point2 = KfPoint3d()
        backfacingResult = 0.0
        
        result = false
        point0 = self.points[aTriangle.pointIndexes[0] - 1]
        point1 = self.points[aTriangle.pointIndexes[1] - 1]
        point2 = self.points[aTriangle.pointIndexes[2] - 1]
        backfacingResult = ((point1.x - point0.x) * (point2.y - point0.y)) - ((point1.y - point0.y) * (point2.x - point0.x))
        result = (backfacingResult < 0)
        return result
    
# not using
#procedure KfObject3D.insertPoint(newPointIndex: smallint; newPoint: KfPoint3d);
#  var
#    i: smallint;
#  begin
#  inc(pointsInUse);
#  if newPointIndex <= pointsInUse - 1 then for i := newPointIndex to pointsInUse - 1 do
#    begin
#    self.changePointIndexInTriangles(i+1, i);
#    points[i+1] := points[i];
#    end;
#  points[newPointIndex] := newPoint;
#  end;
#
#
#    writeln(outputFile, '#declare camera_' + nameString + '= camera {');
#    writeln(outputFile, chr(9) + 'location  <0, 0, ' + intToStr(round(lowestZ)) + '>');
#    writeln(outputFile, chr(9) + 'look_at <'
#      + intToStr(round(totalX / (triangles.count * 3)))
#      + ', ' + intToStr(round(totalY / (triangles.count * 3)))
#      + ', ' + intToStr(round(totalZ / (triangles.count * 3))) + '>');
#    writeln(outputFile, chr(9) + 'angle 90');
#    writeln(outputFile, '}');
#    
