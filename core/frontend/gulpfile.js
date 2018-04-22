var gulp = require('gulp');
var sass = require('gulp-sass');
var concat = require('gulp-concat');
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
        ],
        "ext": [
            dev_folder + "ext/**/*.*",
        ]
    },
    "build": {
        "styles": build_folder + "static/styles",
        "scripts": build_folder + "static/scripts",
        "fonts": build_folder + "static/fonts",
        "libs": build_folder + "static/libs",
        "views": build_folder + "views",
        "ext": build_folder + "static"
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

gulp.task('libs', function () {
    gulp
        .src([
            '../../node_modules/jquery/dist/jquery.min.js',
            '../../node_modules/jquery-pjax/jquery.pjax.js',
            '../../node_modules/highlightjs/highlight.pack.min.js',
            '../../node_modules/nprogress/nprogress.js',
            '../../node_modules/moment/min/moment.min.js',
            '../../node_modules/marked/marked.min.js',
            '../../node_modules/chart.js/Chart.min.js'
        ])
        .pipe(concat('djacket-libs.js'))
        .pipe(uglify())
        .pipe(gulp.dest(paths.build.libs));

    gulp
        .src([
            '../../node_modules/font-awesome/css/font-awesome.min.css',
            '../../node_modules/devicons/css/devicons.min.css',
            '../../node_modules/nprogress/nprogress.css',
            '../../node_modules/highlightjs/styles/monokai-sublime.css'
        ])
        .pipe(concat('djacket-libs.css'))
        .pipe(sass({
            outputStyle: 'compressed'
        }).on('error', sass.logError))
        .pipe(gulp.dest(paths.build.libs));
    
    gulp
        .src([
            '../../node_modules/font-awesome/fonts/*',
            '../../node_modules/devicons/fonts/*',
        ])
        .pipe(gulp.dest(paths.build.fonts));
});

gulp.task('views', function () {
    gulp
        .src(paths.dev.views)
        .pipe(minifyHtml({empty: true}))
        .pipe(gulp.dest(paths.build.views));
});

gulp.task('ext', function () {
    gulp
        .src(paths.dev.ext)
        .pipe(gulp.dest(paths.build.ext))
})

gulp.task('watch', function () {
    gulp.watch([paths.dev.styles, paths.dev.scripts, paths.dev.views], ['styles', 'scripts', 'views']);
});

gulp.task('default', ['compile', 'watch']);    // Default task is for watching development folder for any changes.

gulp.task('compile', ['styles', 'scripts', 'libs', 'views', 'ext']);   // Compile task will run all necessary tasks for frontend.
