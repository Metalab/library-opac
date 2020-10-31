#!/usr/bin/env bash
# Sebastian Elisa Pfeifer <sebastian@sebastian-elisa-pfeifer.eu>

find upload/js/ -type f \
    -name "*.js" ! -name "*.min.*" ! -name "vfs_fonts*" \
    -exec terser {} --comments --compress --mangle --comments --source-map --output {} \;

find upload/ -type f \
    -name "*.html" ! -name "*.html.*" \
    -exec minify {} --type html -o {} \;

uglifycss upload/style.css --output upload/style.css
echo -e "\n*# sourceMappingURL=style.css.map */" >> upload/style.css
