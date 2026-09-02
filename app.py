from flask import Flask, jsonify, redirect, url_for, request
from werkzeug.exceptions import HTTPException
from config.database import init_db, db
from controller import v1_controller, v2_controller
from models.roles import Roles

app = Flask(__name__)

init_db(app)

app.register_blueprint(v1_controller)
app.register_blueprint(v2_controller)

@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        if request.path.startswith("/api"):
            return {"error": e.description}, e.code
        return redirect(url_for("controller.login"))
    print(f"Unhandled exception: {e}")
    if request.path.startswith("/api"):
        return {"error": "Something went wrong. Please try again later."}, 500
    return redirect(url_for("controller.login"))

@app.route("/health",methods=["GET"])
def health():
    try:
        return "OK", 200
    except Exception:
        return "Unhealthy", 503

if __name__ == "__main__":
    with app.app_context():
        try:
            db.create_all()
            if not Roles.query.filter_by(name="admin").first():
                db.session.add(Roles(name="admin"))
            if not Roles.query.filter_by(name="user").first():
                db.session.add(Roles(name="user"))
            db.session.commit()
        except Exception as e:
            print(f"Database setup failed: {e}")
    app.run(host="0.0.0.0", port=5000,debug=True)
