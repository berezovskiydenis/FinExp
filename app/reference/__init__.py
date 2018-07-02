from flask import Blueprint

bp = Blueprint('reference', __name__)

from app.reference import views
