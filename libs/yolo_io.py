#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
import os
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement
from lxml import etree
import codecs
from libs.constants import DEFAULT_ENCODING, baseServerUrl
import requests

TXT_EXT = '.txt'
ENCODE_METHOD = DEFAULT_ENCODING
defaultClassListPath = baseServerUrl + 'classes.txt'


class YOLOWriter:
    def __init__(self,
                 foldername,
                 filename,
                 imgSize,
                 databaseSrc='Unknown',
                 localImgPath=None):
        self.foldername = foldername
        self.filename = filename
        self.databaseSrc = databaseSrc
        self.imgSize = imgSize
        self.boxlist = []
        self.localImgPath = localImgPath
        self.verified = False

    def addBndBox(self, xmin, ymin, xmax, ymax, name, difficult):
        bndbox = {'xmin': xmin, 'ymin': ymin, 'xmax': xmax, 'ymax': ymax}
        bndbox['name'] = name
        bndbox['difficult'] = difficult
        self.boxlist.append(bndbox)

    def BndBox2YoloLine(self, box, classList=[]):
        xmin = box['xmin']
        xmax = box['xmax']
        ymin = box['ymin']
        ymax = box['ymax']

        xcen = float((xmin + xmax)) / 2 / self.imgSize[1]
        ycen = float((ymin + ymax)) / 2 / self.imgSize[0]

        w = float((xmax - xmin)) / self.imgSize[1]
        h = float((ymax - ymin)) / self.imgSize[0]

        # PR387
        boxName = box['name']
        if boxName not in classList:
            classList.append(boxName)

        classIndex = classList.index(boxName)

        return classIndex, xcen, ycen, w, h

    def save(self, targetFile, classList=[]):
        labels = ''
        for box in self.boxlist:
            classIndex, xcen, ycen, w, h = self.BndBox2YoloLine(box, classList)
            # print (classIndex, xcen, ycen, w, h)
            label = "%d %.6f %.6f %.6f %.6f\n" % (classIndex, xcen, ycen, w, h)
            labels += label
        data = {'bboxes': labels}

        # upload to server. any new uploads will override existing file.
        r = requests.put(targetFile, json=data)
        # check status code for response recieved
        # success code - 201: created
        print('r', r)
        # print text of request
        print('\ntext\n', r.text)
        print('\content\n', r.content)
        print('\nheaders\n', r.headers)


class YoloReader:
    def __init__(self, filepath, image, classListPath=defaultClassListPath):
        # shapes type:
        # [labbel, [(x1,y1), (x2,y2), (x3,y3), (x4,y4)], color, color, difficult]
        self.shapes = []
        self.filepath = filepath
        self.classListPath = classListPath

        try:
            classfilerequest = requests.get(self.classListPath)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        try:
            bboxrequest = requests.get(self.filepath)
            self.boxes = bboxrequest.content.decode().strip('\n').split('\n')
        except requests.exceptions.RequestException as e:
            if bboxrequest.status_code == 404:
                print('no existing labels')
                return False
            else:
                raise SystemExit(e)

        # self.classes is a list of classes
        self.classes = classfilerequest.content.decode().strip('\n').split(
            '\n')
        print('classes: ', self.classes)

        imgSize = [
            image.height(),
            image.width(), 1 if image.isGrayscale() else 3
        ]

        self.imgSize = imgSize

        self.verified = False
        # try:
        self.parseYoloFormat()
        # except:
        # pass

    def getShapes(self):
        return self.shapes

    def addShape(self, label, xmin, ymin, xmax, ymax, difficult):

        points = [(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)]
        self.shapes.append((label, points, None, None, difficult))

    def yoloLine2Shape(self, classIndex, xcen, ycen, w, h):
        label = self.classes[int(classIndex)]

        xmin = max(float(xcen) - float(w) / 2, 0)
        xmax = min(float(xcen) + float(w) / 2, 1)
        ymin = max(float(ycen) - float(h) / 2, 0)
        ymax = min(float(ycen) + float(h) / 2, 1)

        xmin = int(self.imgSize[1] * xmin)
        xmax = int(self.imgSize[1] * xmax)
        ymin = int(self.imgSize[0] * ymin)
        ymax = int(self.imgSize[0] * ymax)

        return label, xmin, ymin, xmax, ymax

    def parseYoloFormat(self):
        bndBoxFile = self.boxes
        for bndBox in bndBoxFile:
            if len(bndBox) == 0:
                print('no existing labels')
                return False
            classIndex, xcen, ycen, w, h = bndBox.split(' ')
            label, xmin, ymin, xmax, ymax = self.yoloLine2Shape(
                classIndex, xcen, ycen, w, h)

            # Caveat: difficult flag is discarded when saved as yolo format.
            self.addShape(label, xmin, ymin, xmax, ymax, False)
