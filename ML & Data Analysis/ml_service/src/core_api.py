from flask import Flask, Blueprint
'''
Flask API core endpoints
'''

bp_core = Blueprint("core", __name__)

@bp_core.get("/models")
def models_list():
    return

@bp_core.post("/models/activate")
def models_activate():
    return

@bp_core.post("/train")
def train():
    return

@bp_core.post("/forecast")
def forecast():
    return
