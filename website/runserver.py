from os import environ
from website import app



def DataToJSON():
    print("testing")
    res = Database.get_all('coffee')
    print(res)



if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
 
    
