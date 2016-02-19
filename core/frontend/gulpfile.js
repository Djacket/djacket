var gulp = require('gulp');
var sass = require('gulp-sass');
var uglify = require('gulp-uglify');
var minifyHtml = require('gulp-minify-html');

var dev_folder = "./public/dev/";
var build_folder = "./public/build/";

var paths = {
    "dev": {
        "styles": [
            dev_folder + "static/styles/**/*.css",
            dev_folder + "static/styles/**/*.scss",
        ],
        "scripts": [
            dev_folder + "static/scripts/**/*.js",
        ],
        "views": [
            dev_folder + "views/**/*.html",
        ]
    },
    "build": {
        "styles": build_folder + "static/styles",
        "scripts": build_folder + "static/scripts",
        "views": build_folder + "views",
    }
};


gulp.task('styles', function () {
    gulp
        .src(paths.dev.styles)
        .pipe(sass({
            outputStyle: 'compressed'
        }).on('error', sass.logError))
        .pipe(gulp.dest(paths.build.styles));
});

gulp.task('scripts', function () {
    gulp
        .src(paths.dev.scripts)
        .pipe(uglify())
        .pipe(gulp.dest(paths.build.scripts));
});

gulp.task('views', function () {
    gulp
        .src(paths.dev.views)
        .pipe(minifyHtml({empty: true}))
        .pipe(gulp.dest(paths.build.views));
});

gulp.task('watch', function () {
    gulp.watch([paths.dev.styles, paths.dev.scripts, paths.dev.views], ['styles', 'scripts', 'views']);
});

gulp.task('default', ['watch']);    // Default task is for watching development folder for any changes.

gulp.task('compile', ['styles', 'scripts', 'views']);   // Compile task will run all necessary tasks for frontend.
