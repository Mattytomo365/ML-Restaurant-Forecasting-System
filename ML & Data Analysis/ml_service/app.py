'''
Flask web service
'''

# HTTP GET
@app.get("/models")
def models_list():
    return

@app.get("/eda/summary")
def eda_summary():
    return

# HTTP POST
@app.post("/models/activate")
def models_activate():
    return

@app.post("/train")
def train():
    return

@app.post("/forecast")
def forecast():
    return