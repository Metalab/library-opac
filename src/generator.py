#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import argparse
import sys
import os
import datetime
import pytz
import json
import logzero
from logzero import logger as log
from stdnum import isbn, issn
from jinja2 import Environment, FileSystemLoader
from locale import strxfrm

def formatIdentifier(stringToFormat, type):
    if type.lower() == "isbn":
        if isbn.is_valid(stringToFormat):
            return isbn.format(stringToFormat)
            log.debug("OK ISBN: {0}".format(tmp))
        else:
            log.error("Malformed ISBN: {0}".format(stringToFormat))
            return stringToFormat

    elif type.lower() == "issn":
        if issn.is_valid(stringToFormat):
            return issn.format(stringToFormat)
            log.debug("OK ISSN: {0}".format(tmp))
        else:
            log.error("Malformed ISSN: {0}".format(stringToFormat))
            return stringToFormat

def generateLogoUrl(locationForLogoCheck):
    tmp = locationForLogoCheck.replace(" ", "")

    if os.path.isfile("static/img/locations/{0}.png".format(tmp)):
        return "img/locations/{0}.png".format(tmp)
    else:
        log.error("No Logo for {0}!".format(locationForLogoCheck))
        return "img/locations/nologo.png"

# CLI Parameter
parser = argparse.ArgumentParser("generator.py")
parser.add_argument("--loglevel", help="DEBUG, INFO, ERROR, CRITICAL")
parser.add_argument("--jsonlog", help="Log output as JSON")
parser.add_argument("--source", help="Path to inventory.csv. Default /tmp/library-media-inventory/inventory.csv")
parser.add_argument("--name", help="Library Name. Defaults to 'Metalab Library'")

args = vars(parser.parse_args())

# Logging stuff
loglevelFromCli = getattr(sys.modules["logging"], args["loglevel"].upper() if args["loglevel"] else "INFO")
jsonLogFromCli = args["jsonlog"].upper() if args["jsonlog"] else "N"
logzero.loglevel(loglevelFromCli)

if (jsonLogFromCli == "Y" or jsonLogFromCli == "YES"):
    logzero.json()

log.debug("Command Line Parameters: {0}".format(args))

# Defaults
sourceFile = args["source"] if args["source"] else "/tmp/library-media-inventory/inventory.csv"
libraryName = args["name"] if args["name"] else "Metalab Library"

log.info("Library Name: {0}".format(libraryName))

# Current folder
workDir = os.path.dirname(os.path.realpath(__file__))

log.info("Source file: {0}".format(sourceFile))

jinja2Env = Environment(loader=FileSystemLoader('templates'), autoescape=True)

#### End of config stuff ####

try:
    with open(sourceFile, newline='') as csvFileReader:
        readFile = csv.DictReader(csvFileReader)
        media = sorted(readFile, key = lambda tup: (strxfrm(tup["location"].lower()), strxfrm(tup["category"].lower()), strxfrm(tup["name"].lower())))
except FileNotFoundError:
    log.critical("Can't read library.csv!")
    exit(1)

log.debug("Media: {0}".format(media))

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

log.debug("Records: {0}".format(locationsAndCategories))

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
for templateFile in [x for x in os.listdir(workDir + "/templates") if (os.path.splitext(x)[1] == ".j2" and x[0] != "_")]:
    log.info("Reading Page Template: {0}".format(templateFile))
    targetFilename = os.path.splitext(templateFile)[0]
    log.info("Writing Page: {0}".format(targetFilename))

    template = jinja2Env.get_template(templateFile)
    with open("{0}/upload/{1}".format(workDir, targetFilename), "w") as templateWriter:
        templateWriter.write(template.render(sharedTemplateVars))

# Write the locations
locationTemplate = jinja2Env.get_template("_location_boilerplate.html.j2")
for location in reversedLocations:
    log.info("Writing location: {0}".format(location))
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
    log.info("Writing Media Information as JSON...")
    json.dump(media, mediaJsonWriter)
