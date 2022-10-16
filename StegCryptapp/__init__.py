from .views import app, db, t_init_db


db.init_app(app)

@app.cli.command("init_db")
def init_db():
    t_init_db()
