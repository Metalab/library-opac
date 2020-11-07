"use strict";

var gulp = require("gulp");
var sass = require("gulp-sass");
var sourcemaps = require("gulp-sourcemaps");
var autoprefixer = require("gulp-autoprefixer");
var minifycss = require("gulp-minify-css");
var sriHash = require("gulp-sri-hash");

sass.compiler = require("node-sass");

gulp.task("sass", function(){
  return gulp.src(["static/sass/all.scss"])
    .pipe(sourcemaps.init())
    .pipe(sass.sync({
      outputStyle: "compressed"
    }).on("error", sass.logError))
    .pipe(autoprefixer("last 2 versions"))
    .pipe(minifycss())
    .pipe(sourcemaps.write("."))
    .pipe(gulp.dest("upload/"))
});

gulp.task("sri", () => {
  return gulp.src("upload/*.html")
    .pipe(sriHash({
      algo: "sha512"
    }))
    .pipe(gulp.dest("upload/"));
});

gulp.task("compile", gulp.series("sass"));
gulp.task("subresource-integrity", gulp.series("sri"));
