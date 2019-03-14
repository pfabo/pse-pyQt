import wx
import os
import pipes
import json
from src.component import *
from src.terminal import *


class UdpRead(Component):

    def __init__(self, name, x, y, editor):
        '''

        '''

        Component.__init__(self, name, x, y, editor)

        self.properties['desc'] = "UDP read block"
        self.properties['shapeImage'] = 'udp_globe.svg'
        self.properties['type'] = TYPE_SIM_DISCRETE
        self.properties['shapeColor'] = wx.BLACK
        self.properties['origin'] = (-10, 50)
        self.properties['refOffset'] = (0, -20)
        self.properties['paramOffset'] = (-10, 50)

        self.addTerminal('OUT', 1, TERM.OUT, (50, 20),  TERM.DIR_EAST,
                         TERM.OUT_ARROW_SMALL_FILL,  TERM.OUT_ARROW_SMALL)

        self.parameters['External clock'] = False
        self.parameters['UDP IP'] = '127.0.0.1'
        self.parameters['UDP Port'] = '5005'
        self.parameters['Show name'] = True

        self.pipe = None

    def drawShape(self, gc):
        '''
        '''
        super(UdpRead, self).update()

        gc.SetPen(wx.Pen(self.properties.get('shapeColor')))
        brush = gc.CreateLinearGradientBrush(
            0, -5, 0, 50, 'MEDIUM AQUAMARINE', 'WHITE')
        gc.SetBrush(brush)
        gc.DrawRoundedRectangle(-5, -5, 50, 50, 5)

        self.shapeSVG.render(gc)
        self.properties['box'] = (-10, -10, 60, 60)

        if self.properties['paramShow'] == False:
            if self.parameters['Show name'] == True:

                (dx, dy) = self.properties['paramOffset']
                font = self.properties['paramFont']
                gc.SetFont(font, self.properties['paramColor'])
                s = self.parameters[
                    'UDP IP'] + ':' + self.parameters['UDP Port']
                gc.DrawText(s, dx, dy)

    #
    def update(self):

        if self.parameters['External clock'] == True:
            if self.terminal.has_key(2):
                pass
            else:
                term = self.addTerminal('CLOCK', 2, TERM.IN, (
                    20, -10),  TERM.DIR_SOUTH, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)
                term.properties['termDiscColor'] = wx.RED
                term.properties['termConnColor'] = wx.RED
                term.properties['termConnFill'] = wx.RED
        else:
            if self.terminal.has_key(2):
                if self.terminal[2].connect != []:
                    print '>>> WARNING <<<'
                    print '    UdpRead : remove clock terminal'
                    print '    Clock terminal is connected'
                    self.parameters['External clock'] = True
                else:
                    del self.terminal[2]
            else:
                pass

    def sim(self, flag, value, time, step):
        '''
        '''

        pPath = self.parameters['Pipe name']
        ext = self.parameters['External clock']

        if flag == SIM_INIT:
            pass

        elif flag == SIM_OUTPUT:
            #---------------------------------------------------------------
            # syncronizacia na externe hodiny
            #---------------------------------------------------------------
            if ext == True:
                if self.getTermValue(2) < 1:
                    return

            pass

        elif flag == SIM_FINISH:
            pass

        return 0.0

    #
    def readImport(self, obj):
        '''
        Konverzia numpy.ndarray na list pre export v JSON.
        '''
        # if isinstance(obj, numpy.ndarray):
        #	d=obj.tolist()
        return obj

#=======================================================================
# END OF FILE
#=======================================================================
