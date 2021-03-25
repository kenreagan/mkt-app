from src import create_app, db, app
import os
import click


def create_db():
    with app.app_context():
        db.create_all()

def destroy_db():
    with app.app_context():
        db.drop_all()
        os.unlink('app.sqlite')


app = create_app()


if __name__ == '__main__':
    app.run(port=8000)
