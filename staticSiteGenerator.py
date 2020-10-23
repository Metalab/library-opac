#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import logging
import chromalog
import argparse
import sys
import os
import datetime
from stdnum import isbn
from jinja2 import Environment, FileSystemLoader
from locale import strxfrm

def isbnFormatFunction(isbnToFormat):
    if isbn.is_valid(isbnToFormat):
        tmp = isbn.format(isbnToFormat)
    else:
        logger.error("Malformed ISBN: {0}".format(isbnToFormat))
        tmp = isbnToFormat

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

jinja2Env = Environment(loader=FileSystemLoader('templates'))

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
    if not record["location"] in recordsToWrite: # ... if we don't have the location (branch office)
        recordsToWrite[record["location"]] = {} # ... add it do the dict

    if not record["category"] in recordsToWrite[record["location"]]: # now we do the same with the categories
        recordsToWrite[record["location"]][record["category"]] = {}

logger.debug("Records: {0}".format(recordsToWrite))
logger.info("Locations: {0}".format(recordsToWrite.keys()))

templateVars = {
  "locations": sorted(recordsToWrite.keys(), reverse=True),
  "firstLocation": list(sorted(recordsToWrite.keys(), reverse=True))[0],
  "generationTime": datetime.datetime.now().astimezone().replace(microsecond=0).isoformat(),
  "records": recordsToWrite,
  "media": media,
  "isbnFormatFunction": isbnFormatFunction
}

# Write the OPAC itself
indexTemplate = jinja2Env.get_template("index.html")
with open(workDir + "/upload/index.html", "w") as indexWriter:
    indexWriter.write(indexTemplate.render(templateVars))

# We also need to have filter.js in a template because it uses variables from the csv
filterTemplate = jinja2Env.get_template("js/filter.js")
with open(workDir + "/upload/js/filter.js", "w") as filterWriter:
    filterWriter.write(filterTemplate.render(templateVars))
