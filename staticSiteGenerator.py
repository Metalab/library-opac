#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import logging
import chromalog
import argparse
import sys
import os
import datetime
from stdnum import isbn, issn
from jinja2 import Environment, FileSystemLoader
from locale import strxfrm

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

recordsToWrite = {}
for record in media: # Loop through all records
    if not record["location"] in recordsToWrite: # ... if we don't have the location (branch offices)
        recordsToWrite[record["location"]] = {} # ... add it do the dict

    if not record["category"] in recordsToWrite[record["location"]]: # now we do the same with the categories
        recordsToWrite[record["location"]][record["category"]] = {}

logger.debug("Records: {0}".format(recordsToWrite))

# Reverse Locations as a quick fix for issue #1
reversedLocations = sorted(recordsToWrite.keys(), reverse=True)

templateVars = {
  "locations": reversedLocations,
  "firstLocation": list(reversedLocations)[0],
  "generationTime": datetime.datetime.now().astimezone().replace(microsecond=0).isoformat(),
  "records": recordsToWrite,
  "media": media,
  "isbnFormatFunction": isbnFormatFunction,
  "issnFormatFunction": issnFormatFunction
}

# Write the Index Page
indexTemplate = jinja2Env.get_template("index.html")
with open(workDir + "/upload/index.html", "w") as indexWriter:
    indexWriter.write(indexTemplate.render({
        "locations": sorted(recordsToWrite.keys(), reverse=True),
    }))

# Write the locations
for location in reversedLocations:
    logger.info("Writing location: {0}".format(location))

    destFile = "upload/location_{0}.html".format(location.replace(" ", ""))
