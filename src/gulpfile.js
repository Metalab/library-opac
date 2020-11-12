"use strict";

var gulp = require("gulp");
var sass = require("gulp-sass");
var sourcemaps = require("gulp-sourcemaps");
var autoprefixer = require("gulp-autoprefixer");
var cleancss = require("gulp-clean-css");
var sriHash = require("gulp-sri-hash");
var terser = require("gulp-terser");

sass.compiler = require("node-sass");

gulp.task("sass", function() {
  return gulp.src(["static/sass/all.scss"])
    .pipe(sourcemaps.init())
    .pipe(sass.sync({
      outputStyle: "compressed"
    }).on("error", sass.logError))
    .pipe(autoprefixer("last 2 versions"))
    .pipe(cleancss())
    .pipe(sourcemaps.write("."))
    .pipe(gulp.dest("upload/"))
});

gulp.task("js", function() {
  return gulp.src("static/js/**/*.js")
    .pipe(sourcemaps.init())
    .pipe(terser({
      mangle: true,
      compress: true
    }))
    .pipe(sourcemaps.write("."))
    .pipe(gulp.dest("upload/js"))
});

gulp.task("sri", () => {
  return gulp.src("upload/*.html")
    .pipe(sriHash({
      algo: "sha512"
    }))
    .pipe(gulp.dest("upload/"));
});

gulp.task("compile", gulp.series("sass", "js"));
gulp.task("subresource-integrity", gulp.series("sri"));
