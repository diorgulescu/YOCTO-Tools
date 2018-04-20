import sys
import os
sys.path.insert(1,os.path.dirname(os.path.abspath(__file__)))
from mods.Common import findFile
from mods import PackageInfo
from optparse import OptionParser

def main(argv):
	parser = OptionParser()
	parser.add_option("-d", "--work-dir", dest="workdir",
			action="store", type="string",
			help="Specify where license.manifest will be looked for", metavar="workdir")
	parser.add_option("-j", "--json-export", dest="json", default="",
			action="store", type="string",
			help="Give the absolute path of the JSON file that will be created", metavar="json")
	parser.add_option("-x", "--xml-export", dest="xml", default="",
			help="Export to the specified XML file (the absolute path is required)", metavar="xml")
	parser.add_option("-c", "--csv", dest="csv", default="",
			help="The absolute path of the CSV file that will be created", metavar="csv")
	parser.add_option("-r", "--release-id", dest="releaseID", default="Q",
			help="Pass the release ID (\"Q\" by default)")

	(options, args) = parser.parse_args()
	
	if not options.workdir:  
		parser.error('You didn\'t specify the path where we should look for license.manifest. Use -h for more instructions')
		sys.exit(2)
	
	# Find the license manifest file	
	manifestFile = findFile("license.manifest", options.workdir)

	# Initialize the PackageInfo object
	pkgInfo = PackageInfo.PackageInfo(manifestFile, options.releaseID, options.xml, options.json, options.csv)	

	# Process Package Info
	pkgInfo.extractPackageInfo()

if __name__ == "__main__":
	main(sys.argv[1:])

	
