import wx
import os
import pipes
import json
from src.component import *
from src.terminal import *


class PipeWrite(Component):

    def __init__(self, name, x, y, editor):
        '''

        '''

        Component.__init__(self, name, x, y, editor)

        self.properties['desc'] = "Pipe write block"
        self.properties['shapeImage'] = 'pp_write.svg'
        self.properties['type'] = TYPE_SIM_DISCRETE
        self.properties['shapeColor'] = wx.BLACK
        self.properties['origin'] = (-10, 50)
        self.properties['refOffset'] = (0, -20)
        self.properties['paramOffset'] = (-10, 50)

        self.addTerminal('IN', 1, TERM.IN, (-10, 20),  TERM.DIR_EAST,
                         TERM.IN_ARROW_SMALL_FILL,  TERM.IN_ARROW_SMALL)

        self.parameters['External clock'] = False
        self.parameters['Pipe name'] = '/tmp/pipe'
        self.parameters['Show name'] = True

        self.pipe = None

    def drawShape(self, gc):
        '''
        '''
        super(PipeWrite, self).update()

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
                gc.DrawText(self.parameters['Pipe name'], dx, dy)

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
                    print '    PipeWrite : remove clock terminal'
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
            # kontrola existencie adresarov a vytvorenia pipe
            if not os.path.exists(pPath):
                try:
                    os.mkfifo(pPath, 0777)
                except:
                    print '>>> WARNING <<<'
                    print '    Cannot create fifo at ', pPath

            # otvorenie pipe a priradenie deskriptora
            try:
                self.pipe = os.open(pPath, os.O_WRONLY | os.O_NONBLOCK)
                self.properties['shapeImage'] = 'pp_write_g.svg'
            except:
                self.pipe = None
                self.properties['shapeImage'] = 'pp_write_r.svg'

        # zapis do pipe, v pripede neexistujucej pipe pokus o jej otvorenie
        elif flag == SIM_OUTPUT:
            #---------------------------------------------------------------
            # syncronizacia na externe hodiny
            #---------------------------------------------------------------
            if ext == True:
                if self.getTermValue(2) < 1:
                    return

            value = self.getTermValue(1)
            try:
                s = json.dumps(value, default=self.writeExport)
                os.write(self.pipe, s + '\n')
            except:
                try:
                    self.pipe = os.open(pPath, os.O_WRONLY | os.O_NONBLOCK)
                    self.properties['shapeImage'] = 'pp_write_g.svg'
                except:
                    self.pipe = None
                    self.properties['shapeImage'] = 'pp_write_r.svg'

        elif flag == SIM_FINISH:
            self.properties['shapeImage'] = 'pp_write_r.svg'

        return 0.0

    #
    def writeExport(self, obj):
        '''
        Konverzia numpy.ndarray na list pre export v JSON.
        '''
        if isinstance(obj, numpy.ndarray):
            d = obj.tolist()
            return d
#=======================================================================
# END OF FILE
#=======================================================================
