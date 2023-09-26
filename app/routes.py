from app import app


@app.route('/', method=['GET'])
def index():
    return '<h1>This is Del Ruiz ordering app!</h1>'