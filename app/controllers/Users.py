from system.core.controller import *

class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)

        self.load_model('User')
        self.db = self._app.db

    def index(self):
        return self.load_view('index.html')

    def register(self):
        validation_result = self.models['User'].validate_reg_info(request.form)
        print validation_result
        if type(validation_result) == list:
            session['val_errors'] = validation_result
        if 'val_errors' in session:
            for error in session['val_errors']:
                flash(error)
            session.pop('val_errors')# clears flash messages
            return redirect('/')
        self.set_user_session(validation_result)
        return redirect('/user')

    def login(self):
        login_result = self.models['User'].login(request.form)
        print login_result
        if type(login_result) == list:
            session['login_errors'] = login_result
        if 'login_errors' in session:
            for error in session['login_errors']:
                flash(error)
            session.pop('login_errors')# clears flash messages
            return redirect('/')
        self.set_user_session(login_result)
        return redirect('/user')


    def user(self):
        return self.load_view('user.html')


    def set_user_session(self, validation_result):
        session['user'] = validation_result
        return

    def logout(self):
        session.clear()
        return redirect('/')

    def admin(self):
        return self.load_view('admin.html')

    def display_login_reg(self):
        if 'val_errors' in session:
            for error in session['val_errors']:
                flash(error)
            session.pop('val_errors')# clears flash messages
        return self.load_view('index.html')


        """
    def index(self):
        return self.load_view('index.html')

        A loaded model is accessible through the models attribute
        self.models['WelcomeModel'].get_users()

        self.models['WelcomeModel'].add_message()
        # messages = self.models['WelcomeModel'].grab_messages()
        # user = self.models['WelcomeModel'].get_user()
        # to pass information on to a view it's the same as it was with Flask

        # return self.load_view('index.html', messages=messages, user=user)
        """
