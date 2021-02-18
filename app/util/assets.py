from flask_assets import Bundle

bundles = {
    'main_css': Bundle(
        'css/dashboard.css',
        'css/style.css',
        'fontawesome-free/css/all.css',
        filters='cssmin',
        output='dist/css/style.min.css',
        extra={'rel': 'stylesheet/css'}),

    'main_js': Bundle(
        'js/vendor/jquery/jquery.js',
        'js/vendor/jquery-easing/jquery.easing.js',
        'js/vendor/bootstrap/js/bootstrap.js',
        'js/vendor/bootstrap/js/bootstrap.bundle.js',
        'fontawesome-free/js/all.js',
        'js/dashboard.js',
        filters='jsmin',
        output='dist/js/main.min.js')
}