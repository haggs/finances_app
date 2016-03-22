var gulp = require('gulp');
var concat = require('gulp-concat');
var print = require('gulp-print');
var sass = require('gulp-sass');
var filter = require('gulp-filter');
var util = require('gulp-util');
var minifycss = require('gulp-minify-css');
var uglify = require('gulp-uglify');
var del = require('del');
var gulpif = require('gulp-if');


var static_dir = "static/";
var css_dir = static_dir + "css/";
var js_dir = static_dir + "js/";
var css_build_dir = css_dir + "build/";
var js_build_dir = js_dir + "build/";
var node_modules_dir = "node_modules/";


gulp.task('build_vendor_js', function(){
    gulp.src([ node_modules_dir + "jquery/dist/jquery.js",
               node_modules_dir + "bootstrap/dist/js/bootstrap.js",
               node_modules_dir + "datatables/media/js/jquery.dataTables.js",
               node_modules_dir + "toastr/build/toastr.min.js"
      ]).pipe(print())
        .pipe(concat('vendor.js'))
        .pipe(gulp.dest(js_build_dir));
});


gulp.task('build_vendor_css', function(){
    gulp.src([ node_modules_dir + "bootstrap/dist/css/bootstrap.css",
               node_modules_dir + "datatables/media/css/jquery.dataTables.css",
               node_modules_dir + "font-awesome/css/font-awesome.css",
               node_modules_dir + "toastr/build/toastr.css"
      ]).pipe(print())
        .pipe(concat('vendor.css'))
        .pipe(gulp.dest(css_build_dir));
});


gulp.task('clean', function(cb){
    del([css_build_dir + "*"], cb);
    del([js_build_dir + "*"], cb);
});


gulp.task('build', ['clean', 'build_vendor_js', 'build_vendor_css']);