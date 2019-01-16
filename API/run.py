from flask import Flask
from app.api.v2.models.database import PostgresDatabase
database = PostgresDatabase()
def create_app():
    app = Flask(__name__)
    return app
app = create_app()
if __name__ == "__main__":
    app.run()