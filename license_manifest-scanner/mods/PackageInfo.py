import os
import sys
import json
import xml.dom.minidom
import xml.etree.cElementTree as ET
import csv

class PackageInfo:
	"""A class that gives one the option to easily extract information from the license.manifest
	file (generated by YOCTO) - attributes like version, recipe name and license - and export it
	into various easily parsable formats: JSON, XML and CSV."""

	def __init__(self, licenseManifestFile, release_id="Q", xmlout="", jsonout="", csvout=""):
		"""Object constructor. The absolute path to the license.manifest file is mandatory, while the
	others are entirely optional. Setting the other parameters determines whether or not that 
	type of export will be performed."""
		self.manifestFile = licenseManifestFile
		self.jsonOutputFile = jsonout
		self.xmlOutputFile = xmlout
		self.csvOutputFile = csvout
		self.releaseID = release_id

	# GETTERS & SETTERS
	def setJSONOutputFile(self, outputFilePath):
		"""Sets the JSON output file path to the supplied value. As a direct effect, JSON processing will be performed."""
		self.jsonOutputFile = outputFilePath

	def setXMLOutputFile(self, outputFilePath):
		"""Sets the XML output file path to the supplied value. As a direct effect, XML processing will be performed."""
		self.xmlOutputFile = outputFilePath

	def setCSVOutputFIle(self, outputFilePath):
		"""Sets the CSV output file path to the supplied value. As a direct effect, CSV processing will be performed."""
		self.csvOutputFile = outputFilePath

	def getJSONOutputFile(self):
		"""Returns the current value of jsonOutputFile"""
		return self.jsonOutputFile

	def getXMLOutputFile(self):
        	"""Returns the current value of xmlOutputFile"""
                return self.xmlOutputFile

	def getCSVOutputFile(self):
        	"""Returns the current value of csvOutputFile"""
                return self.csvOutputFile

	# --------END #

	def gatherPackageInfo(self):
		"""Parses the license.manifest file and extracts all available information about each and
	every listed package, building a dictionary based on this info, which is returned."""
		# The dictionary that will be used to store the extracted information
        	packageInfo = {}
	        with open(self.manifestFile) as file:
        	        contents = file.read()
			
			# Split the file contents into "chunks", each chunk being associated with
			# a single package. A chunk contains the package name, it's version, the
			# name of the recipe that was used and 
                	for entry in contents.split('\n\n'):
                        	pkgName=pkgVer=pkgRecipe=pkgLicense=""
	                        entryAttributes = {}
                	        entryContents = entry.split('\n')
                        	for line in entryContents:
	                                if "PACKAGE VERSION" in line:
        	                                pkgVer = line.rsplit(':', 1)[1].strip()
                	                if "PACKAGE NAME" in line:
                        	                pkgName = line.rsplit(':', 1)[1].strip()
					if "RECIPE NAME" in line:
                                                pkgRecipe = line.rsplit(':', 1)[1].strip()
					if "LICENSE" in line:
                                                pkgLicense = line.rsplit(':', 1)[1].strip()

	                        entryAttributes.update({'version' : pkgVer})
				entryAttributes.update({'recipe' : pkgRecipe})
				entryAttributes.update({'license' : pkgLicense})

        	                packageInfo.update({pkgName : entryAttributes})
		
		# Clean the dictionary by removing any blank keys and values
		packageInfo.pop('""', None)
		packageInfo.pop('', None)
	        return packageInfo

	def buildPKGInfoJSON(self, packageInfoDict):
		"""This builds a JSON file that contains only a list of packages and their
		   version. It's functionality should be extended only if this requirement is
		agreed with the stakeholders."""
		returnStatus = False
		# If the output file is not set (for some reason), return an error and quit.
		if self.jsonOutputFile != "":
			# The dict object that will eventually be used for writing out the JSON file
			jsonInfo = {}

			# A list of tuples consisting of package names and their versions
			packageList = []
	
			# Build the prerequisite for the JSON dictionary
			for pkgName, pkgAttributes in packageInfoDict.iteritems():
				packageList.append([pkgName, pkgAttributes['version']])

			# Update the dictionary
			jsonInfo.update({"release_id" : self.releaseID})
			jsonInfo.update({"packages" : packageList})
	
			# Export it to a file - a try catch must be added here
			with open(self.jsonOutputFile, 'w') as outfile:
				json.dump(jsonInfo, outfile, indent=4, sort_keys=True) 
			print "INFO: JSON file successfully created."
		return returnStatus

	def buildPKGInfoXML(self, packageInfoDict):
		"""Builds an XML that contains only a list of the packages and their
                   attributes."""
               	if self.xmlOutputFile == "":
                       	print "ERROR: XML Output file is not set!"
                        sys.exit(1)

		# +BUILD THE XML+ #
		# Release ID must be a parameter!
		root = ET.Element("packages", release_id="Q")
		
		for pkgName, pkgAttributes in packageInfoDict.iteritems():
			if "+" in pkgName:
				pkgName.replace("+", "_plus")
			pkg = ET.SubElement(root, pkgName)

			ET.SubElement(pkg, "version").text = pkgAttributes['version']
			ET.SubElement(pkg, "license").text = pkgAttributes['license'] 
			ET.SubElement(pkg, "recipe").text = pkgAttributes['recipe']
		tree = ET.ElementTree(root)

		# TODO: Dynamically locate the file and finish XML pretty printing 
		tree.write("tempFile.xml") # Here we must randomly generate a filename

		# +PRETTY PRINT+ #
		xmlParser = xml.dom.minidom.parse("tempFile.xml")
		formattedXMLAsString = xml.toprettyxml()
		
		# print - for now
		#print pretty_xml_as_string

		# Write out the file
		with open(self.xmlOutputFile, 'w') as outfile:
			outfile.write(formattedXMLAsString)
	
		return True

	def buildPKGInfoCSV(self, packageInfoDict):
		"""Build a CSV file that contains all packages and their versions"""

		csvData = []

		for pkgName, pkgAttributes in packageInfoDict.iteritems():
			csvData.append((pkgName, pkgAttributes['version']))

		with open(self.csvOutputFile, 'w') as csvWriteHandle:
			writer = csv.writer(csvWriteHandle, delimiter=',')
			writer.writerows(csvData)
	
		print "INFO: XML file successfully created."	
		return True

	def extractPackageInfo(self):
		"""This is the main method that triggers package info processing. No arguments are passed, while the method itself prints out the files that were generated after the run."""	
		if self.jsonOutputFile:
			self.buildPKGInfoJSON(self.gatherPackageInfo())
		
		if self.xmlOutputFile:
			print "WARNING: XML export is not currently available! Skipping..."
			#self.buildPKGInfoXML()

		if self.csvOutputFile:
			self.buildPKGInfoCSV(self.gatherPackageInfo())
