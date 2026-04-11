from flask import Blueprint, render_template

web_bp = Blueprint("web", __name__)


@web_bp.route("/")
def home():
    return render_template(
        "home.html",
        title="Home",
        message="This page is rendered by Flask + Jinja.",
    )


@web_bp.route("/about")
def about():
    return render_template(
        "home.html",
        title="About",
        message="This route is also served by Flask.",
    )