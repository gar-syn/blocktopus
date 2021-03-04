from flask_assets import Bundle

bundles = {
    'main_css': Bundle(
        'css/dashboard.css',
        'css/style.css',
        'css/libraries/all.css',
        'css/libraries/dataTables.bootstrap4.css',
        'css/libraries/buttons.dataTables.css',
        filters='cssmin',
        output='gen/css/style.min.css',
        extra={'rel': 'stylesheet/css'}),

    'main_js': Bundle(
        'js/libraries/jquery.js',
        'js/libraries/jquery.easing.js',
        'js/libraries/jquery.dataTables.js',
        'js/libraries/bootstrap.js',
        'js/libraries/bootstrap.bundle.js',
        'js/libraries/popper.min.js',        
        'js/libraries/dataTables.bootstrap4.js',
        'js/libraries/dataTables.buttons.js',
        'js/libraries/jszip.js',
        'js/libraries/pdfmake.js',
        'js/libraries/vfs_fonts.js',
        'js/libraries/buttons.print.js',
        'js/libraries/buttons.html5.js',
        'js/libraries/all.js',
        'js/datatables.js',
        'js/dashboard.js',
        filters='jsmin',
        output='gen/js/main.min.js')
}