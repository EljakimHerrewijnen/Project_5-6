
activate_this = '/home/flaskvenv/bin/activate_this.py'
with open(activate_this) as file_:
    print("Trying to open file")
    exec(file_.read(), dict(__file__=activate_this))
    print("Success")

import sys
sys.path.insert(0, '/var/www/Project56/Project_5-6/Website')

from website.app import app
application = app

