from flask_assets import Bundle

bundles = {
    'main_css': Bundle(
        'css/dashboard.css',
        'css/style.css',
        'css/libraries/all.css',
        filters='cssmin',
        output='gen/css/style.min.css',
        extra={'rel': 'stylesheet/css'}),

    'main_js': Bundle(
        'js/libraries/jquery.js',
        'js/libraries/jquery.easing.js',
        'js/libraries/bootstrap.js',
        'js/libraries/bootstrap.bundle.js',
        'js/libraries/all.js',
        'js/dashboard.js',
        filters='jsmin',
        output='gen/js/main.min.js')
}