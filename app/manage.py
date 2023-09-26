# used to run our application
# from app import app
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)