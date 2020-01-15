from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import TextOperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import TextRecognitionMode
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time
import pyodbc

class Azure:
	def __init__(self):
		# Azure SQL Authentication
		self.server = 'trashusers.database.windows.net'
		self.database = 'userData'
		self.username = 'rootAdmin'
		self.password = 'A!123456'
		self.driver= '{ODBC Driver 17 for SQL Server}'

		# Azure Custom Vision API Authentication
		self.subscription_key = '0f43b589cb784d5eb502ed57a47845df'
		self.endpoint = 'https://westus2.api.cognitive.microsoft.com/'

		# Search terms:
		self.terms = ["fruit", "food"]

	# changeUserScore(< user # >, < 1 or -1 >), no return
	def changeUserScore(self, user, change):
		cnxn = pyodbc.connect('DRIVER='+self.driver+';SERVER='+self.server+';PORT=1433;DATABASE='+self.database+';UID='+self.username+';PWD='+self.password)
		cursor = cnxn.cursor()

		if change == -1:
			cursor.execute("UPDATE [dbo].[Users] SET Wrong = Wrong + 1 WHERE ID = " + str(user))
		elif change == 1:
			cursor.execute("UPDATE [dbo].[Users] SET Correct = Correct + 1 WHERE ID = " + str(user))

		cnxn.commit()

	# isCompost(< file location >), returns True or False
	def isCompost(self, location):
		computervision_client = ComputerVisionClient(self.endpoint, CognitiveServicesCredentials(self.subscription_key))
		
		# Open local image file
		local_image = open(location, "rb")
		# Call API local image
		tags_result_local = computervision_client.tag_image_in_stream(local_image)
		
		# For debugging
		# for tag in tags_result_local.tags:
  		# print("'{}' with confidence {:.2f}%".format(tag.name, tag.confidence * 100))
		# print()

    	for tag in tags_result_local.tags:
    		if tag in self.terms:
   				return True

   		return False

