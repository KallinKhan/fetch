from flask import Flask
from transactions.transactions import transactions
from settings import PORT


def initialize_app():
    app = Flask(__name__)
    app.register_blueprint(transactions)
    return app


def main():
    app = initialize_app()
    app.run(port=PORT)


if __name__ == '__main__':
    main()
