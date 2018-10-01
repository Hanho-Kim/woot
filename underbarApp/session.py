#-*- coding: utf-8 -*-

import pymysql.cursors
import json 
from django.template import RequestContext
from django.views.generic.base import RedirectView
from django.shortcuts import render, get_object_or_404,redirect,render_to_response
from django.http import HttpResponse, Http404
from .models import *

class Session(object):
	def __init__(self, connection, request):
		self.connection = connection
		if 'superbarID' in request.session:
			self.superbarID = request.session['superbarID']
			self.superbar = easyGetRecords('barInfo', self.connection, 'barID', self.superbarID, select="*")[0]
		if 'upperbarID' in request.session:
			self.upperbarID = request.session['upperbarID']
			self.upperbar = easyGetRecords('barInfo', self.connection, 'barID', self.upperbarID, select="*")[0]
		if 'superbarName' in request.session:
			self.superbarName = request.session['superbarName']
		else:
			self.superbarName = "underbar"

	def getSuperbar(self, request):
		self.superbarID = request.session['superbarID']
		self.superbarName = request.session['superbarName']
		self.superbar = easyGetRecords('barInfo', self.connection, 'barID', self.superbarID, select="*")[0]
		self.superbar = easyGetRecords('barInfo', self.connection, 'barID', self.superbarID, select="*")[0]

	def getUpperbar(self, request):
		self.upperbarID = request.session['upperbarID']
		self.upperbar = easyGetRecords('barInfo', self.connection, 'barID', self.upperbarID, select="*")[0]
		self.upperbar = easyGetRecords('barInfo', self.connection, 'barID', self.upperbarID, select="*")[0]

	def setSuperbar(self, request, superbarID):
		self.superbarID = superbarID
		self.superbar = easyGetRecords('barInfo', self.connection, 'barID', self.superbarID, select="*")[0]
		request.session["superbarID"] = superbarID

	def setUpperbar(self, request, upperbarID):
		self.upperbarID = upperbarID
		self.upperbar = easyGetRecords('barInfo', self.connection, 'barID', self.upperbarID, select="*")[0]
		request.session["upperbarID"] = upperbarID

	def enterDevbar(self, request):
		self.supperbarName = 'devbar'
		request.session['superbarName'] = 'swag'
		self.setSuperbar(request, 4)
		self.setUpperbar(request, 43)

	def enterUnderbar(self, request):
		self.supperbarName = 'underbar'
		request.session['superbarName'] = 'underbar'
		self.setSuperbar(request, 5)
		self.setUpperbar(request, 8)
