from system.core.controller import *

class Welcome(Controller):
    def __init__(self, action):
        super(Welcome, self).__init__(action)

    def index(self):
        return self.load_view('index.html')

    def display_login_reg(self):
        if 'val_errors' in session:
            for error in session['val_errors']:
                flash(error)
            session.pop('val_errors')# clears flash messages
        return self.load_view('loginreg.html')
