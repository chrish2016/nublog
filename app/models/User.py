from system.core.model import Model
import re

EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')

class User(Model):
    def __init__(self):
        super(User, self).__init__()
        self.validation_errors = {
            'first_name_exist' : "Name can't be blank.",
            'last_name_exist' : "Name can't be blank.",
            'alias_exist' : "Alias can't be blank.",
            'email_exist' : "Email can't be blank.",
            'email_valid' : "Email must be valid.",
            'password_exist' : "Password can't be blank.",
            'password_match' : "Passwords must match.",
            'email_taken' : "Email already in use.",
            'alias_taken' : "Alias already taken.",
            'login_fail' : "Email/password don't match."
        }
        self.queries = {
            'create_user' : "INSERT INTO users (first_name, last_name, alias, email, pw_hash, created_at, updated_at) VALUES( :first_name, :last_name, :alias, :email, :password, NOW(), NOW())",
            'get_user' : "SELECT id, first_name, last_email, alias, email, friends, admin, created_at, updated_at FROM users WHERE id = :id",
            'get_user_by_email' : "SELECT * FROM users WHERE email = :email LIMIT 1",
            'fetch_all_users' : "SELECT id, first_name, last_name, alias, email, friends, admin, created_at, updated_at FROM users WHERE id != :id",
            'fetch_user_by_id' : "SELECT id, first_name, last_name, alias, email, friends, admin, created_at, updated_at FROM users WHERE id = :id"
        }

    def login(self, form_data):
        result = self.get_user_by_email(form_data['email'])

        if not result:
            return [self.validation_errors['login_fail']]

        password = form_data['password']
        pw_hash = result[0]['pw_hash']

        test_password_result = self.bcrypt.check_password_hash(pw_hash, password)

        if test_password_result == False:
            return [self.validation_errors['login_fail']]
        else:
            return {
                'id' : result[0]['id'],
                'first_name' : result[0]['first_name'],
                'last_name' : result[0]['last_name'],
                'alias' : result[0]['alias'],
                'email' : result[0]['email'],
                'friends' : result[0]['friends'],
                'admin' : result[0]['admin']
            }

    def get_user_by_email(self, email):
        query = self.queries['get_user_by_email']
        data = { 'email' : email }
        return self.db.query_db(query, data)


    def validate_reg_info(self, form_data):
        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        errors = []

        if len(form_data['first_name']) < 1:
            errors.append(self.validation_errors['first_name_exist'])
        if len(form_data['last_name']) < 1:
            errors.append(self.validation_errors['last_name_exist'])
        if len(form_data['alias']) < 1:
            errors.append(self.validation_errors['alias_exist'])
        if len(form_data['email']) < 1:
            errors.append(self.validation_errors['email_exist'])
        if not EMAIL_REGEX.match(form_data['email']):
            errors.append(self.validation_errors['email_valid'])
        if len(form_data['password']) < 1:
            errors.append(self.validation_errors['password_exist'])
        if form_data['password'] != form_data['password_confirm']:
            errors.append(self.validation_errors['password_match'])

        if len(errors) > 0:
            return errors

        result = self.get_user_by_email(form_data['email'])

        if len(result) > 0:
            errors.append(self.validation_errors['email_taken'])
            return errors

        return self.register(form_data)


    def register(self, form_data):
        pw_hash = self.bcrypt.generate_password_hash(form_data['password'])
        query = self.queries['create_user']
        data = {
            'first_name' : form_data['first_name'],
            'last_name' : form_data['last_name'],
            'alias' : form_data['alias'],
            'email' : form_data['email'],
            'password' : pw_hash
        }

        result = self.db.query_db(query, data)
        return self.fetch_user_by_id(result)

    def fetch_user_by_id(self, id):
        query = self.queries['fetch_user_by_id']
        data = { 'id' : id }
        result = self.db.query_db(query, data)
        return result[0]

    def fetch_all_users(self, id):
        query = self.queries['fetch_all_users']
        data = { 'id' : id }
        result = self.db.query_db(query, data)
        return result

    def get_user_by_email(self, email):
        query = self.queries['get_user_by_email']
        data = { 'email' : email }
        return self.db.query_db(query, data)
