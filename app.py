import os
from flask import Flask, jsonify
from flask_smorest import Api
# REMOVED: from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from db import db
# REMOVED: from blocklist import BLOCKLIST

from resources.user import blp as UserBlueprint
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint

# Ensure models are imported at top-level for migrations
import models.user
import models.item
import models.store
import models.tag

import logging

def create_app(db_url=None):
    app = Flask(__name__)
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    
    db.init_app(app)
    api = Api(app)

    # REMOVED: JWT Configuration and initialization
    # app.config["JWT_SECRET_KEY"] = "982e04f86f5b9b7754d58a032997193a027c44d7a8d0526e0e620d4f215d263a"
    # jwt = JWTManager(app)
    #
    # REMOVED: All JWT callback functions (token_in_blocklist_loader, expired_token_loader, etc.)
    
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)

    return app

# Migration support for flask db commands
def make_migrations_app():
    app = create_app()
    Migrate(app, db)
    return app

# Local development only
if __name__ == "__main__":
    app = create_app()
    from os import environ
    app.run(host="0.0.0.0", port=int(environ.get("PORT", 10000)))