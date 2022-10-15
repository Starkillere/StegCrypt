from .views import app, db, t_init_db


db.init_app(app)

@app.cli.command()
def init_db():
    t_init_db()
