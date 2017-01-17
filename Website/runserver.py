

from os import environ
from website import app

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', '95.85.13.5')
    try:
        PORT = int(environ.get('SERVER_PORT', '80'))
    except ValueError:
        PORT = 80
    app.run(HOST, PORT)
