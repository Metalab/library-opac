# library-opac
[![Build Status](https://travis-ci.org/Metalab/library-opac.svg?branch=main)](https://travis-ci.org/Metalab/library-opac)

The Metalab has a library. And this library now has an OPAC! And this is the generator for it.

## What's an OPAC?

An Online Public Access Catalogue (OPAC) is an online accessible library catalog.

## How to use it?

If you want to use the Metalab Library Media Inventory, run update.sh. It will clone/pull the repo to your home folder. Then replace the logos in src/static/img. Install the python dependencies in requirements.json and the node.js ones from the package.json. To do so run
```bash
pip install -r requirements.txt
npm install
```

Have a look at what is done in the .travis.yml file, or run the following commands in the src folder of this repo:

```bash
rsync -aP --delete ./static/ ./upload/
$(npm bin)/gulp compile
./staticSiteGenerator.py --loglevel INFO --source $HOME/library-media-inventory/inventory.csv --name "Metalab Library"
$(npm bin)/gulp subresource-integrity
```

This will generate a folder called "upload", which you can then serve with any web server of your like. Since the generated files are static html, and the search and other dynamic features are implemented in JavaScript, there is no need for PHP or any other server side language to serve the OPAC.

Note that this will not minify the generated html pages and is only wise to use for development! To minify the html pages, install the "minify" package and run
```bash
find upload/ -type f -name "*.html" -exec minify {} --type html -o {} \;
```

## License
MIT License (c) 2020 Metalab

## 3rd Party License
https://github.com/Metalab/library-opac/blob/main/.github/3dparty.md
