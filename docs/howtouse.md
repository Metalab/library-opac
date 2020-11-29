# How to use it?

## Requirements
If you want to use the Metalab Library Media Inventory[^1], run src/update.sh. It will clone/pull the repo to your home folder, install some npm modules and validate the csv. Install the python dependencies in requirements.json and the node.js ones from the package.json. To do so run

``` bash
pip install -r requirements.txt
npm install
```
in the src folder.

Edit the config.yml file to fit your needs.

``` yaml
--8<-- "src/config.yml"
```

### Generate the pages

Have a look at what is done in the .travis.yml file, or run the following commands (also in the src folder):

``` bash
rsync -aP --delete --exclude "js" --exclude "sass" ./static/ ./upload/
pybabel compile --directory=locale
$(npm bin)/gulp compile
./generator.py --loglevel INFO --source $HOME/library-media-inventory/inventory.csv
$(npm bin)/gulp subresource-integrity
```

This will generate a folder called "upload", which you can then serve with any web server of your like. Since the generated files are static html, and the search and other dynamic features are implemented in JavaScript, there is no need for PHP or any other server side language to serve the OPAC.

Note that this will not minify the generated html pages and is only wise to use for development! To minify the html pages, install the `minify` package and run
``` bash
find upload/ -type f -name "*.html" -exec minify {} --type html -o {} \;
```

[^1]: <https://github.com/Metalab/library-media-inventory>
