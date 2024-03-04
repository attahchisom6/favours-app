#!/usr/bin/env python3
"""
inirialize session variables
"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

from Authentication_microservice.api.v1.views.index import *
