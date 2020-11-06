# library-opac
[![Build Status](https://travis-ci.org/Metalab/library-opac.svg?branch=main)](https://travis-ci.org/Metalab/library-opac)

The Metalab has a library. And this library now has an OPAC! And this is the generator for it.

## What's an OPAC?

An Online Public Access Catalogue (OPAC) is an online accessible library catalog.

## How to use?

If you want to use the Metalab Library Media Inventory, run update.sh. It will clone/pull the repo to the location where the script will look for it by default. Then replace the logos in static/img. Install the python dependencies in requirements.json and the node.js ones from the package.json. Have a look at what is done in the .travis.yml file, otherwise run the following commands in the root folder of this repo:

```bash
$(npm bin)/node-sass --source-map true --source-map-contents --output-style expanded static/sass/all.scss static/style.css
rsync -av --info=progress2 --delete ./static/ ./upload/
./staticSiteGenerator.py
```

Note that this will not minify any of the generated content and is only wise to use for development!
