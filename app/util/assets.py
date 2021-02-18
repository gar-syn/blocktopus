from flask_assets import Bundle

bundles = {
    'main_css': Bundle(
        'css/dashboard.css',
        'css/style.css',
        'css/lib/all.css',
        filters='cssmin',
        output='gen/css/style.min.css',
        extra={'rel': 'stylesheet/css'}),

    'main_js': Bundle(
        'js/lib/jquery.js',
        'js/lib/jquery.easing.js',
        'js/lib/bootstrap.js',
        'js/lib/bootstrap.bundle.js',
        'js/lib/all.js',
        'js/dashboard.js',
        filters='jsmin',
        output='gen/js/main.min.js')
}