from flask import Flask
from routing import Routing
from log import Log

app = Flask(__name__)
routing = Routing(app)
log = Log()


routing.serve()


if __name__ == '__main__':
    app.run(host="localhost", port=1000, debug=True)
