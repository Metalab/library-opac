#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import logging
import chromalog
import argparse
import sys
import os

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

#### End of config stuff ####

with open(sourceFile, newline='') as csvFileReader:
    readFile = csv.DictReader(csvFileReader)
    sortedRecords = sorted(readFile, key = lambda tup: (tup["location"], tup["category"], tup["name"]))

logger.debug(sortedRecords)
