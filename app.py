from BackEnd import create_app
from flask_cors import CORS
from flask_session import Session

app=create_app()
CORS(app)
Session(app)
@app.route('/')
def hello():
    return "Hello, World!"

if __name__=='__main__':
    app.run(debug=False)