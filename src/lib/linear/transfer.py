# -*- coding: utf-8 -*-
from color import Color
from component import AgregateComponent
from lib.pseqt import *  # @UnusedWildImport
from lib.signal.port import VirtProxyOutIn, VirtProxyInOut
from terminal import TERM

from .gain import VirtSumGain, VirtGain
from .integ import VirtInteg


class TrFunc2(AgregateComponent):
    '''
    Integracia prenosovej funkcie 2. radu.

    Staticky vytvoreny virtulny diagram pre implementaciu prenosovej
    funkcie 2. radu.
    '''

    def __init__(self, name, pos):
        AgregateComponent.__init__(self, name, pos)

        #self.png = QPixmap('./src/lib/linear/img/tr_func2.png')
        self.shapeImage = 'tr_func2.png'
        self.box = QRectF(-70, -30, 140, 60)
        self.shapeColor = Color.red

        self.addTerminal('IN', 1, TERM.IN, QPointF(-70, 0), TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)
        self.addTerminal('OUT', 2, TERM.OUT, QPointF(70, 0), TERM.DIR_EAST, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)

        self.addParameter('Num', "[1.0, 1.0]", False, QPointF(0, 40), Color.black, True)
        self.addParameter('Den', "[1.0, 1.0, 1.0]", False, QPointF(0, 55), Color.black, True)

        self.num = [1.0, 1.0]		# koeficienty citatela   [b1, b0]
        self.den = [1.0, 1.0, 1.0]		# koeficienty menovatela [a2, a1, a0]

        # virtualny diagram komponentu
        # prepojenie na terminaly objektu
        prp1 = self.addComponent(VirtProxyOutIn(self.terminal[1]))
        prp2 = self.addComponent(VirtProxyInOut(self.terminal[2]))

        self.s1 = self.addComponent(VirtSumGain(3))
        self.s2 = self.addComponent(VirtSumGain(2))

        int1 = self.addComponent(VirtInteg())
        int2 = self.addComponent(VirtInteg())

        self.addNet(prp1, 1, self.s1, 1)  # n1
        self.addNet(self.s1, 4, int1, 1)  # n2
        self.addNet(int1, 2, int2, 1)     # n3
        self.addNet(int2, 2, self.s2, 1)  # n4
        self.addNet(self.s2, 3, prp2, 1)  # n5

        self.addNet(int1, 2, self.s1, 3)  # n6
        self.addNet(int2, 2, self.s1, 2)  # n7

        self.addNet(int1, 2, self.s2, 2)  # n8

    def updateShape(self):
        super(TrFunc2, self).updateShape()
        try:
            s = self.parameter['Num'].value
            s = s.replace('[', '')  # uprava retazca
            s = s.replace(']', '')
            q = s.split(',')
            self.num[0] = float(q[0])
            self.num[1] = float(q[1])
        except:
            print('>>> Parameter error in TrFunc2, Ref ', self.parameter['Ref'].value)
            print('    Wrong numerator value ', self.parameter['Num'].value)
            self.num = [1.0, 1.0]

        try:
            s = self.parameter['Den'].value
            s = s.replace('[', '')  # uprava retazca
            s = s.replace(']', '')
            q = s.split(',')
            self.den[0] = float(q[0])
            self.den[1] = float(q[1])
            self.den[2] = float(q[2])
        except:
            print('>>> Parameter error in TrFunc2, Ref ', self.parameter['Ref'].value)
            print('    Wrong denominator value ', self.parameter['Den'].value)
            self.den = [1.0, 1.0, 1.0]

        # nastavenie koeficientov - parametrov sumacnych komponentov
        # [1.0, -a0/a2, -a1/a2]
        self.s1.gain = [1.0, -self.den[2] / self.den[0], -self.den[1] / self.den[0]]

        # [b0/a2, b1/a2]
        self.s2.gain = [self.num[1] / self.den[0], self.num[0] / self.den[0]]

    def drawShape(self, gc):

        gc.setPen(QPen(self.shapeColor, 0.6))
        grad = QLinearGradient(0, -25, 0, 50)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.yellow)
        gc.setBrush(QBrush(grad))

        gc.drawRoundedRect(-65, -25, 130, 50, 5, 5)

        self.drawIcon(gc, -55, -20)

    def loadDiagram(self):
        pass


class TrFunc1(AgregateComponent):
    '''
    Integracia prenosovej funkcie 1. radu.

    Staticky vytvoreny virtulny diagram pre implementaciu prenosovej
    funkcie 1. radu.
    '''

    def __init__(self, name, pos):
        AgregateComponent.__init__(self, name, pos)

        self.shapeImage = 'tr_func1.png'
        self.box = QRectF(-40, -30, 80, 60)
        self.shapeColor = Color.red

        self.addTerminal('IN', 1, TERM.IN, QPointF(-40, 0), TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)
        self.addTerminal('OUT', 2, TERM.OUT, QPointF(40, 0), TERM.DIR_EAST, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)

        self.addParameter('Num', "[1.0]", False, QPointF(0, 40), Color.black, True)
        self.addParameter('Den', "[1.0, 1.0]", False, QPointF(0, 55), Color.black, True)

        self.num = [1.0]			# koeficienty citatela
        self.den = [1.0, 1.0]		# koeficienty menovatela

        self.s1 = self.addComponent(VirtSumGain(2))

        prp1 = self.addComponent(VirtProxyOutIn(self.terminal[1]))
        prp2 = self.addComponent(VirtProxyInOut(self.terminal[2]))

        int1 = self.addComponent(VirtInteg())
        self.amp1 = self.addComponent(VirtGain())

        self.addNet(prp1, 1, self.s1, 1)
        self.addNet(self.s1, 3, int1, 1)
        self.addNet(int1, 2, self.amp1, 1)
        self.addNet(int1, 2, self.s1, 2)
        self.addNet(self.amp1, 2, prp2, 1)

    def updateShape(self):
        # nacitanie standardnych casti komponentu (ikony)
        super(TrFunc1, self).updateShape()

        # nastavenie parametrov komponentu
        try:
            s = self.parameter['Num'].value
            s = s.replace('[', '')  # uprava retazca
            s = s.replace(']', '')
            q = s.split(',')
            self.num[0] = float(q[0])
        except:
            print('>>> Parameter error in TrFunc1, Ref ', self.parameter['Ref'].value)
            print('    Wrong numerator value ', self.parameter['Num'].value)
            self.num = [1.0]

        try:
            s = self.parameter['Den'].value
            s = s.replace('[', '')  # uprava retazca
            s = s.replace(']', '')
            q = s.split(',')
            self.den[0] = float(q[0])
            self.den[1] = float(q[1])
        except:
            print('>>> Parameter error in TrFunc1, Ref ',
                  self.parameter['Ref'].value)
            print('    Wrong denominator value ', self.parameter['Den'].value)
            self.den = [1.0, 1.0]

        # nastavenie koeficientov - parametrov sumacnych komponentov
        #            [1.0, -a0/a2, -a1/a2]
        self.s1.gain = [1.0, -self.den[1] / self.den[0]]
        self.amp1.gain = self.num[0] / self.den[0]

    def drawShape(self, gc):

        gc.setPen(QPen(self.shapeColor, 0.6))
        grad = QLinearGradient(0, -25, 0, 50)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.yellow)
        gc.setBrush(QBrush(grad))
        gc.drawRoundedRect(-35, -25, 70, 50, 5, 5)
        self.drawIcon(gc, -30, -20)

    def loadDiagram(self):
        pass
