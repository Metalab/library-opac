# library-opac
[![Build Status](https://travis-ci.org/Metalab/library-opac.svg?branch=main)](https://travis-ci.org/Metalab/library-opac)

The Metalab has a library. And this library now has an OPAC! And this is the generator for it.

## What's an OPAC?

An Online Public Access Catalogue (OPAC) is an online accessible library catalog.

## How to use it?

If you want to use the Metalab Library Media Inventory, run update.sh. It will clone/pull the repo to your home folder. Then replace the logos in static/img. Install the python dependencies in requirements.json and the node.js ones from the package.json. To do so run
```bash
pip install -r requirements.txt
npm install
```

Have a look at what is done in the .travis.yml file, otherwise run the following commands in the root folder of this repo:

```bash
rsync -aP --delete ./static/ ./upload/
$(npm bin)/gulp compile
./staticSiteGenerator.py --loglevel INFO --source $HOME/library-media-inventory/inventory.csv --name "Metalab Library"
$(npm bin)/gulp subresource-integrity
```

Note that this will not minify the generated html pages and is only wise to use for development! To minify the html pages, install the "minify" package and run
```bash
find upload/ -type f -name "*.html" -exec minify {} --type html -o {} \;
```

You can then serve the upload folder in an web server of your like.
