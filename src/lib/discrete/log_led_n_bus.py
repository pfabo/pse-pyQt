import wx

from numpy import zeros

from component import Component
from componenttypes import TYPE_SIM_CONTINUOUS, SIM_UPDATE
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class BusLed(Component):
    '''     '''
    def __init__(self, name, x, y, editor):
        '''        '''
        Component.__init__(self, name, x, y, editor)

        self.numLed = 6

        self.properties['desc'] = "Variable bus led indicator"
        self.properties['type'] = TYPE_SIM_CONTINUOUS
        self.properties['shapeColor'] = wx.BLACK
        self.properties['origin'] = (-10, self.numLed * 10 * 2)
        self.properties['refOffset'] = (0, -20)
        self.properties['paramOffset'] = (-10, self.numLed * 10 * 2 + 10)
        self.properties['box'] = (-10, 0, 30, self.numLed * 10 * 2)

        self.parameters['Number of LEDs'] = self.numLed

        self.addTerminal(
            'IN', 1, TERM.IN, (-10, self.numLed * 10), TERM.DIR_EAST)

        self.value = zeros(self.numLed)

    def update(self):
        '''
        Uprava poctu LED a polohy terminalu
        '''

        if self.parameters['Number of LEDs'] != self.numLed:
            self.numLed = self.parameters['Number of LEDs']
            self.terminal[1].properties['position'] = (-10, self.numLed * 10)

            self.properties['origin'] = (-10, self.numLed * 10 * 2)
            self.properties['paramOffset'] = (-10, self.numLed * 10 * 2 + 10)
            self.properties['box'] = (
                -10, 0, 30, self.numLed * 10 * 2)

    #
    def drawShape(self, gc):
        '''
        '''

        gc.SetPen(wx.Pen(self.properties.get('shapeColor')))
        for i in range(self.numLed):
            gc.DrawRoundedRectangle(0, 0 + i * 20, 20, 20, 5)

        for i in range(self.numLed):
            path = gc.CreatePath()

            # osetrenie pretecenia indexu pri kratsom vstupnom vektore
            try:
                val = self.value[i]
            except:
                val = False

            if val is True:
                brush = gc.CreateBrush(wx.Brush('LIME GREEN'))
            else:
                brush = gc.CreateBrush(wx.Brush('RED'))
            gc.SetBrush(brush)
            path.AddCircle(10, 10 + i * 20, 7)
            gc.FillPath(path)
            gc.StrokePath(path)

        gc.SetPen(wx.Pen(self.properties.get('shapeColor'), 3))
        path = gc.CreatePath()
        path.MoveToPoint(-10, self.numLed * 10)
        path.AddLineToPoint(0, self.numLed * 10)
        gc.StrokePath(path)

    def sim(self, flag, value, time, step):
        '''
        '''
        if flag == SIM_UPDATE:
            self.value = self.terminal[1].value

        return 0.0
