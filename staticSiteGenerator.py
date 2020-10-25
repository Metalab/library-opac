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
from stdnum import isbn, issn
from jinja2 import Environment, FileSystemLoader
from locale import strxfrm
from pathlib import Path

def isbnFormatFunction(isbnToFormat):
    if isbn.is_valid(isbnToFormat):
        tmp = isbn.format(isbnToFormat)
    else:
        logger.error("Malformed ISBN: {0}".format(isbnToFormat))
        tmp = isbnToFormat

    return tmp

def issnFormatFunction(issnToFormat):
    if issn.is_valid(issnToFormat):
        tmp = issn.format(issnToFormat)
    else:
        logger.error("Malformed ISSN: {0}".format(issnToFormat))
        tmp = issnToFormat

    return tmp

def generateLogoUrl(locationForLogoCheck):
    tmp = locationForLogoCheck.replace(" ", "")

    if os.path.isfile("static/img/aussenstellen/{0}.png".format(tmp)):
        return "img/aussenstellen/{0}.png".format(tmp)
    else:
        logger.error("No Logo for {0}!".format(locationForLogoCheck))
        return "img/aussenstellen/nologo.png"

# CLI Parameter
parser = argparse.ArgumentParser("staticSiteGenerator.py")
parser.add_argument("--loglevel", help="DEBUG, INFO, ERROR, CRITICAL")
parser.add_argument("--source", help="Path to inventory.csv. Default /tmp/library-media-inventory/inventory.csv")

args = vars(parser.parse_args())

# Logging stuff
loglevel = getattr(sys.modules["logging"], args["loglevel"].upper() if args["loglevel"] else "INFO")
chromalog.basicConfig(format="%(message)s", level=loglevel)
logger = logging.getLogger()

logger.debug(args)

# Source file
sourceFile = args["source"] if args["source"] else "/tmp/library-media-inventory/inventory.csv"

# Current folder
workDir = os.path.dirname(os.path.realpath(__file__))

logger.info("Source file {0}".format(sourceFile))

jinja2Env = Environment(loader=FileSystemLoader('templates'), autoescape=True)

#### End of config stuff ####

try:
    with open(sourceFile, newline='') as csvFileReader:
        readFile = csv.DictReader(csvFileReader)
        media = sorted(readFile, key = lambda tup: (strxfrm(tup["location"]), strxfrm(tup["category"]), strxfrm(tup["name"])))
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
        locationsAndCategories[record["location"]][record["category"]] = {}

logger.debug("Records: {0}".format(locationsAndCategories))

# Reverse Locations as a quick fix for issue #1
reversedLocations = sorted(locationsAndCategories.keys(), reverse=True)

# Generation Time
generationTime = datetime.datetime.now().astimezone(pytz.timezone("Europe/Vienna")).replace(microsecond=0).isoformat()

# Write the Index Page
indexTemplate = jinja2Env.get_template("index.html")
with open("{0}/upload/index.html".format(workDir), "w") as indexWriter:
    indexWriter.write(indexTemplate.render({
        "locations": reversedLocations,
        "logoUrl": generateLogoUrl,
        "generationTime": generationTime,
    }))

# Write the locations
locationTemplate = jinja2Env.get_template("_location_boilerplate.html")
for location in reversedLocations:
    logger.info("Writing location: {0}".format(location))
    destFile = "upload/location_{0}.html".format(location.replace(" ", ""))

    with open("{0}/{1}".format(workDir, destFile), "w") as locationWriter:
        locationWriter.write(locationTemplate.render({
            "locations": reversedLocations,
            "logoUrl": generateLogoUrl,
            "location": location,
            "media": media,
            "categories": locationsAndCategories[location],
            "isbnFormatFunction": isbnFormatFunction,
            "issnFormatFunction": issnFormatFunction,
            "generationTime": generationTime
        }))
