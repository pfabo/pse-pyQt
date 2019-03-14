# -*- coding: utf-8 -*-
'''
Save data to the HDF5 file

HDF5 is a high performace dataformat designed to store and organize
large amounts of numerical data.

This python module needs python liblary h5py installed in your system:
www.h5py.org
https://pypi.python.org/pypi/h5py


Current implementation use dialect, which is possible to open via graph viewer
from http://www.signalconstructor.com

Note: Output file is compressed to keep size on minimum level.

Data are accessible via above mentioned SW or python liblary,
or can be opened via hdfview: http://www.hdfgroup.org/products/java/hdfview
'''

import logging

from numpy import ndarray
import numpy

from color import Color
from component import Component, PARAM
from componenttypes import (TYPE_SIM_CONTINUOUS, SIM_UPDATE, SIM_INIT,
                            SIM_FINISH, SIM_RESET)
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM
from math import isnan


LOG = logging.getLogger(__name__)


class FileHDF5(Component):
    '''Write values from terminal to the file'''
    def __init__(self, name, pos):
        super(FileHDF5, self).__init__(name, pos)
        self.shapeImage = 'file_write_hdf5.svg'
        self.compType = TYPE_SIM_CONTINUOUS
        self.shapeColor = Color.blue
        self.box = QRectF(-30, -30, 60, 60)

        term_in = self.addTerminal('IN', 1, TERM.IN, QPointF(-30, 0),
                                   TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL,
                                   TERM.IN_ARROW_SMALL)
        term_in.termDiscColor = Color.black       # farby pre vstup - vektor
        term_in.termDiscFill = Color.white
        term_in.termConnColor = Color.black
        term_in.termConnFill = Color.black

        # TODO: minimum for this parameter is 1
        # TODO: add human readable parameter description
        # Parameter N:  remember only N-th step
        self.addParameter('N', 1, paramType=PARAM.INT)
        self.addParameter('File', 'data.hdf5', paramType=PARAM.FILE_HDF5_SAVE)

        self.__mem = None
        self.__append_fun = None
        self.__period = None
        self.__param_N = None
        self.__step = 0

    def drawShape(self, gc):
        grad = QLinearGradient(0, -25, 0, 50)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.mediumAquamarine)
        gc.setBrush(QBrush(grad))

        gc.setPen(QPen(self.shapeColor, 1))
        gc.drawRoundedRect(-25, -25, 50, 50, 5, 5)

        self.drawIcon(gc, -20, -20)

    def __init_memory(self, val):
        '''inicialization of memory'''
        if isinstance(val, ndarray):
            nb_sig = len(val)  # calculate number of inputs in first step
            # memory is list of lists
            self.__mem = [list() for _ in range(nb_sig)]
            # use append function instead of calling .append (faster)
            self.__append_fun = [obj.append for obj in self.__mem]
        else:
            data = list()  # there will be signal data
            self.__mem = [data]
            self.__append_fun = data.append

    def sim(self, flag, value, time, step):
        if flag == SIM_UPDATE:
            # store value to the internal lists
            val = self.terminal[1].value

            if self.__mem is None:
                self.__init_memory(val)  # called only at the first step

            self.__period = step

            # remember only N-th step
            if not self.__step % self.__param_N:
                if isinstance(val, ndarray):  # val is array
                    for i, append_fun in enumerate(self.__append_fun):
                        append_fun(val[i])  # optimized for speed
                else:
                    self.__append_fun(val)  # only one signal is recorded
            self.__step += 1

        elif flag in [SIM_INIT, SIM_RESET]:
            # init memory
            # unfortunatelly we do not know number of inputs at this point
            self.__mem = None  # so only set variable to None
            self.__param_N = self.parameter['N'].value
            self.__step = 0

        elif flag == SIM_FINISH:
            # save the data to the file
            filename = self.parameter['File'].value
            # period must be integer [ms]
            period = int(self.__param_N * self.__period * 1000)
            hdf5_save(self.__mem, filename, period)
            self.__mem = None  # release memory


def hdf5_save(mem, filename, period):
    '''Save mem to the hdf5 file

    :param mem: list of lists with data
    :param filename: filename to save
    :param opts: options dictionary
    '''
    # 0. try to import h5py, if not inform user via error message

    # reason to import h5py "in the middle of module" is that not every
    # user has h5py installed. In that case PSE can run without this component
    try:
        import h5py
    except ImportError as e:
        LOG.error('Cannot import h5py liblary: %s' % e)
        LOG.error('File %s is not created' % filename)
        return

    nbsteps = len(mem[0])

    # 1. open HDF5 file
    # f = h5py.File('%s' % filename, 'w')
    with h5py.File('%s' % filename, 'w') as f:
        # 3. create signal group
        gsig = f.create_group("signals")

        for i, data in enumerate(mem):
            if isdigital(data):
                # in binary save only transitions -> smaller dataset
                dset = gsig.create_dataset("%08d" % i,
                                           data=get_transitions(data))
                dset.attrs["digital"] = True
            else:
                ndata = numpy.array(data)
                opts = {'compression': 'gzip', 'compression_opts': 9}
                dset = gsig.create_dataset("%08d" % i, data=ndata, **opts)
                dset.attrs["digital"] = False

            name = 'sig%s' % i  # sig.info.name.encode("utf-8")
            dset.attrs["name"] = name.encode(encoding='utf_8', errors='strict')

        meta = f.create_group("meta")
        meta.attrs['period'] = period  # period in miliseconds
        meta.attrs['nbsteps'] = nbsteps  # number of steps


def isdigital(data):
    '''
    return True if numbers in list are binary (contains only 0 and 1)

    :param data: list or array
    '''
    # if first number is NaN consider data as a analog
    if isnan(data[0]):
        return False

    try:
        ifirst = int(data[0])
    except ValueError:
        return False

    if ifirst not in [0, 1]:
        return False  # Fast death

    return data.count(0) + data.count(1) == len(data)


def get_transitions(signal):
    '''get changes (edges) from binary signal list.'''
    out = []
    # example for 11100100001:
    # out = [(0,1),(3,0),(5,1),(6,0),(10,1)]
    out.append((0, signal[0]))  # first is always

    out_append = out.append
    oldvalue = signal[0]
    for i, value in enumerate(signal):
        if oldvalue != value:
            out_append((i, value))  # append change
            oldvalue = value
    return out
