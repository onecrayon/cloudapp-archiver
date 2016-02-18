#!/usr/bin/env python
'''
Downloads your entire history of files from CloudApp for archival purposes

USAGE:

    archive-cloudapp.py -u <username> -p <password> -o <pathToArchiveOutputFolder>
'''
helpstring = "archive-cloudapp.py -u <username> -p <password> -o <pathToArchiveOutputFolder>"

import os, sys, inspect
import getopt
import json

# Add third-party modules to the search path for modules
externalRoot = os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0], "External")
externalDirectories = [os.path.join(externalRoot, name) for name in os.listdir(externalRoot) if os.path.isdir(os.path.join(externalRoot, name))]
for directory in externalDirectories:
	cmd_subfolder = os.path.realpath(os.path.abspath(directory))
	if cmd_subfolder not in sys.path:
		sys.path.insert(0, cmd_subfolder)
# And import third-party modules
import requests
from requests.auth import HTTPDigestAuth

# Grab the username and password
try:
	opts, extraArgs = getopt.getopt(sys.argv[1:], "hu:p:o:", ["help", "user=", "password=", "output="])
except getopt.GetoptError:
	print(helpstring)
	sys.exit(2)

username = None
password = None
rootPath = None
for opt, arg in opts:
	if opt in ("-h", "--help"):
		print(helpstring)
		sys.exit()
	elif opt in ("-u", "--user"):
		username = arg
	elif opt in ("-p", "--password"):
		password = arg
	elif opt in ("-o", "--output"):
		rootPath = os.path.abspath(arg)

if username is None or password is None or rootPath is None:
	print("Error: all arguments are required\n" + helpstring)
	sys.exit(2)
if not os.path.exists(rootPath):
	print("Error: output folder does not exist; please check your path")
	sys.exit(2)

# Time to recurse through the list and download everything!
url = 'http://my.cl.ly/v3/items?per_page=50'
response = requests.get(url, auth=HTTPDigestAuth(username, password), headers={'Accept': 'application/json'})
while response is not None and response.status_code == requests.codes.ok:
	json = response.json()
	for item in json["data"]:
		localFolder = os.path.join(item["created_at"][0:10], item["slug"])
		folderPath = os.path.join(rootPath, localFolder)
		try:
			os.makedirs(folderPath)
		except:
			# Skip items that already exist, since we presumably downloaded them in the past
			print("Skipping " + localFolder + " (already exists)")
			continue
		# Secondary request to download the file itself
		if item["remote_url"] is not None:
			r = requests.get(item["remote_url"], stream=True)
			name = item["name"]
			# Make sure the name doesn't include colons or slashes
			name = name.replace(':', '-')
			name = name.replace('/', '-')
			name = name.replace('\\', '-')
			filePath = os.path.join(folderPath, name)
			# Ensure we have a file extension
			ext = os.path.splitext(filePath)[-1]
			if ext is "":
				ext = os.path.splitext(item["remote_url"])[-1]
				if ext is not "":
					filePath += ext
			if r.status_code == requests.codes.ok:
				print("Downloading " + os.path.join(localFolder, name) + ' ...')
				with open(filePath, 'wb') as f:
					for chunk in r.iter_content(1024):
						f.write(chunk)
			else:
				# Failed to download for some reason, so delete the folder so we can try again in the future
				print("Error: failed to download " + os.path.join(localFolder, name))
				os.rmdir(folderPath)
		elif item["redirect_url"] is not None:
			# We have a URL; create an IE-style .url file (which also works in Safari)
			print("Writing shortcut <" + item["redirect_url"] + "> ...")
			filePath = os.path.join(folderPath, 'shortcut.url')
			f = open(filePath, 'w')
			f.write("[InternetShortcut]\nURL=" + item["redirect_url"] + "\n")
			f.close()
		else:
			print("Error: failed to process item: " + json.dumps(item))
			os.rmdir(folderPath)
	# Now that we've downloaded all the files, check for our next URL
	if "links" in json and "next_url" in json["links"]:
		url = json["links"]["next_url"]["href"]
		response = requests.get(url, auth=HTTPDigestAuth(username, password), headers={'Accept': 'application/json'})
	else:
		response = None

print("All done!")
