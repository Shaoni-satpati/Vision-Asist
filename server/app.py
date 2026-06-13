from flask import Flask
from flask_sock import Sock

def create_app() -> Flask:
    app = Flask(
        __name__,
        static_folder="../frontend",
        static_url_path="",
        template_folder="../frontend",
    )
    sock = Sock(app)

    from server.routes import routes_bp
    from server.stream import register_stream
    app.register_blueprint(routes_bp)
    register_stream(app, sock)
    return app
