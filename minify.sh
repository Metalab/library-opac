#!/usr/bin/env bash
# Sebastian Elisa Pfeifer <sebastian@sebastian-elisa-pfeifer.eu>

find upload/js/ -type f \
    -name "*.js" ! -name "*.min.*" ! -name "vfs_fonts*" \
    -exec uglifyjs {} --comments -c -m -o {} \;

find upload/css/ -type f \
    -name "*.css" ! -name "*.min.*" \
    -exec uglifycss {} --output {} \;

find upload/ -type f \
    -name "*.html" ! -name "*.html.*" \
    -exec minify {} --type html -o {} \;
