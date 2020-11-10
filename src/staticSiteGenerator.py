#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import logging
import chromalog
import argparse
import sys
import os
import datetime
import pytz
import json
from stdnum import isbn, issn
from jinja2 import Environment, FileSystemLoader
from locale import strxfrm
from pathlib import Path

def formatIdentifier(stringToFormat, type):
    if type.lower() == "isbn":
        if isbn.is_valid(stringToFormat):
            return isbn.format(stringToFormat)
            logger.debug("OK ISBN: {0}".format(tmp))
        else:
            logger.error("Malformed ISBN: {0}".format(stringToFormat))
            return stringToFormat

    elif type.lower() == "issn":
        if issn.is_valid(stringToFormat):
            return issn.format(stringToFormat)
            logger.debug("OK ISSN: {0}".format(tmp))
        else:
            logger.error("Malformed ISSN: {0}".format(stringToFormat))
            return stringToFormat

def generateLogoUrl(locationForLogoCheck):
    tmp = locationForLogoCheck.replace(" ", "")

    if os.path.isfile("static/img/locations/{0}.png".format(tmp)):
        return "img/locations/{0}.png".format(tmp)
    else:
        logger.error("No Logo for {0}!".format(locationForLogoCheck))
        return "img/locations/nologo.png"

# CLI Parameter
parser = argparse.ArgumentParser("staticSiteGenerator.py")
parser.add_argument("--loglevel", help="DEBUG, INFO, ERROR, CRITICAL")
parser.add_argument("--source", help="Path to inventory.csv. Default /tmp/library-media-inventory/inventory.csv")
parser.add_argument("--name", help="Library Name. Defaults to 'Metalab Library'")

args = vars(parser.parse_args())

# Logging stuff
loglevel = getattr(sys.modules["logging"], args["loglevel"].upper() if args["loglevel"] else "INFO")
chromalog.basicConfig(format="%(message)s", level=loglevel)
logger = logging.getLogger()

logger.debug(args)

# Defaults
sourceFile = args["source"] if args["source"] else "/tmp/library-media-inventory/inventory.csv"
libraryName = args["name"] if args["name"] else "Metalab Library"

logger.info("Library Name: {0}".format(libraryName))

# Current folder
workDir = os.path.dirname(os.path.realpath(__file__))

logger.info("Source file {0}".format(sourceFile))

jinja2Env = Environment(loader=FileSystemLoader('templates'), autoescape=True)

#### End of config stuff ####

try:
    with open(sourceFile, newline='') as csvFileReader:
        readFile = csv.DictReader(csvFileReader)
        media = sorted(readFile, key = lambda tup: (strxfrm(tup["location"].lower()), strxfrm(tup["category"].lower()), strxfrm(tup["name"].lower())))
except FileNotFoundError:
    logger.critical("Can't read library.csv!")
    exit(1)

logger.debug("Media: {0}".format(media))

# Here we build a nested dictionary in the form
# -> location 1
#   -> category 1
#   -> category 2
# -> location 2
#   -> category 1
#   -> category 2

locationsAndCategories = {}
for record in media: # Loop through all records
    if not record["location"] in locationsAndCategories: # ... if we don't have the location (branch offices)
        locationsAndCategories[record["location"]] = {} # ... add it do the dict

    if not record["category"] in locationsAndCategories[record["location"]]: # now we do the same with the categories
        locationsAndCategories[record["location"]][record["category"]] = []

logger.debug("Records: {0}".format(locationsAndCategories))

# Reverse Locations as a quick fix for issue #1
reversedLocations = sorted(locationsAndCategories, reverse=True)

# Generation Time
generationTime = datetime.datetime.now().astimezone(pytz.timezone("Europe/Vienna")).replace(microsecond=0).isoformat()

# Shared Template vars
sharedTemplateVars = {
    "locations": reversedLocations,
    "logoUrl": generateLogoUrl,
    "generationTime": generationTime,
    "locationsAndCategories": locationsAndCategories,
    "libraryName": libraryName
}

# Write the templates
for templateFile in [x for x in os.listdir(workDir + "/templates") if (os.path.splitext(x)[1] == ".html.j2" and x[0] != "_")]:
    logger.info("Writing Page: {0}".format(templateFile))

    template = jinja2Env.get_template(templateFile)
    with open("{0}/upload/{1}".format(workDir, templateFile), "w") as templateWriter:
        templateWriter.write(template.render(sharedTemplateVars))

# Write the locations
locationTemplate = jinja2Env.get_template("_location_boilerplate.html.j2")
for location in reversedLocations:
    logger.info("Writing location: {0}".format(location))
    destFile = "upload/location_{0}.html".format(location.replace(" ", ""))

    templateVars = {
        "location": location,
        "media": media,
        "categories": locationsAndCategories[location],
        "formatIdentifier": formatIdentifier
    }

    with open("{0}/{1}".format(workDir, destFile), "w") as locationWriter:
        locationWriter.write(locationTemplate.render({**sharedTemplateVars, **templateVars}))

# Write media json
with open("upload/media.json", "w") as mediaJsonWriter:
    json.dump(media, mediaJsonWriter)
