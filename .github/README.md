# library-opac
[![Build Status](https://travis-ci.org/Metalab/library-opac.svg?branch=main)](https://travis-ci.org/Metalab/library-opac)

The Metalab has a library. And this library now has an OPAC! And this is the generator for it.

## What's an OPAC?

An Online Public Access Catalogue (OPAC) is an online accessible library catalog.

## How to use it?

### Requirements
If you want to use the Metalab Library Media Inventory, run src/update.sh. It will clone/pull the repo to your home folder, install some npm modules and validate the csv. Install the python dependencies in requirements.json and the node.js ones from the package.json. To do so run

```bash
pip install -r requirements.txt
npm install
```
in the src folder.

Edit the config.yml file to fit your needs.

#### Generate the pages

Have a look at what is done in the .travis.yml file, or run the following commands (also in the src folder):

```bash
rsync -aq --delete --exclude "js" --exclude "sass" ./static/ ./upload/
$(npm bin)/jsonlint -q locales.json
pybabel compile --directory=locale
$(npm bin)/gulp compile
./generator.py --loglevel INFO --source $HOME/library-media-inventory/inventory.csv
$(npm bin)/gulp subresource-integrity
```

This will generate a folder called "upload", which you can then serve with any web server of your like. Since the generated files are static html, and the search and other dynamic features are implemented in JavaScript, there is no need for PHP or any other server side language to serve the OPAC.

Note that this will not minify the generated html pages and is only wise to use for development! To minify the html pages, install the "minify" package and run
```bash
find upload/ -type f -name "*.html" -exec minify {} --type html -o {} \;
```

### A note on locales

The locale "ebu_KE" is used, but it's not actually the language "Embu" spoken in Kenya. In fact it's the "uwu-ified" version of de_AT, but Babel does not support using custom locales such es de_UWU.

#### Adding new messages

In the src folder, run the following command:

```bash
pybabel extract --mapping=babel-mapping.ini --output=locale/messages.pot --copyright-holder=Metalab --project=library-opac --version=1 ./
```
This will update the locale/messages.pot file with the messages found in the templates in templates/**.html.j2

After that run
```bash
pybabel update --input-file=locale/messages.pot --output-dir=locale
```
to update the files for each locale. Proceed to translate the new messages, then run
```bash
pybabel compile --directory=locale
```
to generate the .mo files used by the script later.

#### Adding a new translation

In the src folder, run the following command:
```bash
pybabel init --input-file=locale/messages.pot --output-dir=locale --locale=*localehere*
```
where localehere can be any locale shown by

```bash
pybabel --list-locales
```

After you have translated the new locale (See the "Adding new messages" section), add the new locale to the locales.json file. Add an image for the new language that will be shown in the language switcher to static/img/locales. You can now generate the pages by running the script.

## License

MIT License (c) 2020 Metalab

## Developed by

(in alphabetical order)
* anlumo
* coldice4
* deadda7a
* eest9
* joak

## 3rd Party / Media License information
https://github.com/Metalab/library-opac/blob/main/.github/3dparty.md
