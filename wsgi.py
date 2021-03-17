#Fask Entrypoint
from app import create_app
from app.util.extensions import db

app = create_app('dev')
app.app_context().push()
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()