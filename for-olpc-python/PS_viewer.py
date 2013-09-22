#!/usr/bin/env python



import pygtk
pygtk.require('2.0')
import gtk
from gtk_helpers import *

import math
from PS_constants import *

import uturtle
import gtkdrawingsurface
#import PS_tdo

#example_tdo = utdo.KfObject3D()
#example_tdo.readFromFile("./3dobject/l_carrot.tdo")
#example_tdo.readFromFile("./3dobject/l_squash.tdo")

import PS_plant
import PS_cursor

import hotshot
prof = None

class PlantDrawingArea(gtk.DrawingArea):
    def __init__(self):
        gtk.DrawingArea.__init__(self)
        self.connect("expose_event", self.expose)
        self.xr = 0
        self.yr = 0
        self.zr = 0
        self.plant = None

    def expose(self, widget, event):
        gc = widget.window.new_gc()
        context = (widget.window, gc)
        width = widget.get_allocation().width
        height = widget.get_allocation().height
        self.draw(context, width, height)

        """
        width = 10
        gc.set_line_attributes(width, gtk.gdk.LINE_SOLID, gtk.gdk.CAP_BUTT, gtk.gdk.JOIN_MITER)
        gc.set_fill(gtk.gdk.SOLID)
        gtkColor = gtk.gdk.color_parse("blue")
        #gtkColor = gtk.gdk.Color(65000, 0, 0, 2)
        print gtkColor
        map = widget.window.get_colormap()
        gtkColor = map.alloc_color("red") # light red
        gc.set_foreground(gtkColor)
        gc.set_background(gtkColor)
        widget.window.draw_line(gc, 0, 0, 100, 100)
        gtkColor = gtk.gdk.color_parse("red")
        widget.window.draw_line(gc, 100, 100, 200, 200)
        """

    def draw(self, context, width, height):
        turtle = uturtle.KfTurtle()
        turtle.drawingSurface = gtkdrawingsurface.GTKDrawingSurface()
        turtle.drawingSurface.setDrawingContext(context)
        turtle.drawOptions.drawStems = True
        turtle.drawOptions.draw3DObjects = True
        #self.testSimple(turtle)
        #self.testPolygon(turtle)
        #self.testTDO(turtle)
        #prof.runcall(self.testPlant, turtle, width, height)
        self.testPlant(turtle, width, height)

    def testPlant(self, turtle, width, height):
        turtle.reset()
        turtle.xyz(width / 2, height - 50, 100)
        turtle.setScale_pixelsPerMm(1.0)
        self.plant.turtle = turtle
        turtle.rotateX(self.xr)
        turtle.rotateY(self.yr)
        turtle.rotateZ(self.zr)
        #self.xr += 4
        #self.yr += 4
        #self.zr += 4
        if self.plant:
            self.plant.draw()
        #self.plant.nextDay()

##    def testTDO(self, turtle):
##        # try to draw polygon
##        turtle.reset()
##        turtle.xyz(50, 100, 100)
##        turtle.rotateX(self.xr)
##        turtle.rotateY(self.yr)
##        turtle.rotateZ(self.zr)
##        #self.xr += 4
##        self.yr += 4
##        self.zr += 4
##        turtle.drawingSurface.foreColor = clGreen
##        turtle.drawingSurface.backColor = clLime
##        turtle.drawingSurface.lineColor = clBlack
##        example_tdo.draw(turtle, 1.0, "", "", 0, 0)

    def testPolygon(self, turtle):
        turtle.reset()
        turtle.xyz(100, 100, 100)
        turtle.startRecording()
        turtle.setLineWidth(5)
        turtle.setLineColor(clRed)
        turtle.moveInPixels(30)
        turtle.recordPosition()
        turtle.rotateZ(32)
        turtle.setLineColor(clBlue)
        turtle.moveInPixels(30)
        turtle.recordPosition()
        turtle.setForeColorBackColor(clGreen, clYellow)
        turtle.drawTriangle()

    def testSimple(self, turtle):
        turtle.reset()
        turtle.xyz(100, 100, 100)
        turtle.setLineWidth(5)
        turtle.setLineColor(clRed)
        turtle.drawInPixels(30)
        turtle.rotateZ(32)
        turtle.setLineColor(clBlue)
        turtle.drawInPixels(30)

############################################################

class MainWindow(object):
    def __init__(self):
        self.plants = None

        self.window = MakeWindow("PlantStudio(TM) for OLPC", 750, 500)

        hbox = MakeHorizontalBox(self.window)
        self.plantList = MakeList(hbox, "Plant name", self.selectionChanged)

        vbox = MakeVerticalBox(hbox)

        self.drawingArea = PlantDrawingArea()
        PackBox(vbox, self.drawingArea)


        hbox = MakeHorizontalBox(vbox)
        MakeButton(hbox, "=0", self.grow, -1)
        MakeButton(hbox, "+1", self.grow, 1)
        MakeButton(hbox, "+5", self.grow, 5)
        MakeButton(hbox, "+10", self.grow, 10)
        MakeButton(hbox, "+30", self.grow, 30)
        MakeButton(hbox, "+100", self.grow, 100)

        hbox = MakeHorizontalBox(vbox)
        MakeButton(hbox, "<<", self.turn, -8)
        MakeButton(hbox, ">>", self.turn, 8)

        MakeButton(vbox, "Open library...", self.openLibrary)

        self.fileName = "test.pla"
        #self.fileName = "test tree.pla"
        #self.fileName = "Garden flowers.pla"
        #self.fileName = "Garden flowers.pla"
        plants = PS_plant.PlantLoader().loadPlantsFromFile(self.fileName, inPlantMover=1, justLoad=1)
        self.setPlantListContents(plants)

        ShowWindow(self.window)
        PS_cursor.windowsToWaitWith.append(self.window.window)

    def setPlantListContents(self, plants):
        self.plants = plants
        plantListContents = []
        for plant in self.plants:
            pair = (plant.name, plant)
            plantListContents.append(pair)
        FillList(self.plantList, plantListContents)
        if self.plants:
            self.drawingArea.plant = self.plants[0]
        else:
             self.drawingArea.plant = None

    def grow(self, widget, days):
        prof.runcall(self._grow, widget, days)
        #self.drawingArea.plant.report()


    def _grow(self, widget, days):
        if not self.drawingArea.plant:
            return
        PS_cursor.cursor_startWait()
        try:
            if days == -1:
                self.drawingArea.plant.reset()
            else:
                for day in range(days):
                    self.drawingArea.plant.nextDay()
        finally:
            PS_cursor.cursor_stopWait()
        InvalidateWidget(self.drawingArea)

    def turn(self, widget, amount):
        self.drawingArea.yr += amount
        InvalidateWidget(self.drawingArea)

    def selectionChanged(self, widget):
        plant = GetListSelection(self.plantList, 1)
        self.drawingArea.plant = plant
        InvalidateWidget(self.drawingArea)

    def openLibrary(self, widget):
        fileName = ChooseFile(self.window, "Plant files", ["*.pla"])
        if fileName == None:
            return
        print "Opening", fileName
        PS_cursor.cursor_startWait()
        try:
            plants = uplant.PlantLoader().loadPlantsFromFile(fileName, inPlantMover=1, justLoad=1)
            self.fileName = fileName
            self.setPlantListContents(plants)
        finally:
            PS_cursor.cursor_stopWait()
        InvalidateWidget(self.drawingArea)

def main():
    #import udomain
    #import uparams
    #for param in udomain.domain.parameterManager.parameters:
    #    if param.fieldType == uparams.kFieldHeader:
    #        print "======== HEADER", param.name
    #    else:
    #        print "                        ", param.name
    #return

    global prof
    prof = hotshot.Profile("hotshot_stats")
    application = MainWindow()
    gtk.main()
    prof.close()

if __name__ == "__main__":
    main()





