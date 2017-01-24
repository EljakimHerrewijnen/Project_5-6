activate_this = '/home/flaskvenv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

import sys
sys.path.insert(0, '/home/Project_5-6')

from app import app as application

