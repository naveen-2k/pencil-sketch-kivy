from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
import mysql.connector

class SignupScreen(Screen):
    def __init__(self, **kwargs):
        super(SignupScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        self.username_input = TextInput(hint_text='Username', multiline=False)
        self.password_input = TextInput(hint_text='Password', multiline=False, password=True)
        self.signup_button = Button(text='Sign Up', on_press=self.signup)

        self.layout.add_widget(Label(text='Signup Page', font_size='20sp'))
        self.layout.add_widget(self.username_input)
        self.layout.add_widget(self.password_input)
        self.layout.add_widget(self.signup_button)

        self.add_widget(self.layout)

    def signup(self, instance):
        # Get user input
        username = self.username_input.text
        password = self.password_input.text

        # Connect to the database
        db_connection = mysql.connector.connect(
            host='your_host',
            user='your_user',
            password='your_password',
            database='your_database'
        )

        # Create a cursor
        cursor = db_connection.cursor()

        # Execute the SQL query to insert the user into the 'users' table
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))

        # Commit the changes and close the connection
        db_connection.commit()
        cursor.close()
        db_connection.close()

        print(f"Signup: Username: {username}, Password: {password}")

        # Transition to the Signin screen
        self.manager.current = 'signin'


class SigninScreen(Screen):
    def __init__(self, **kwargs):
        super(SigninScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        self.username_input = TextInput(hint_text='Username', multiline=False)
        self.password_input = TextInput(hint_text='Password', multiline=False, password=True)
        self.signin_button = Button(text='Sign In', on_press=self.signin)

        self.layout.add_widget(Label(text='Signin Page', font_size='20sp'))
        self.layout.add_widget(self.username_input)
        self.layout.add_widget(self.password_input)
        self.layout.add_widget(self.signin_button)

        self.add_widget(self.layout)

    def signin(self, instance):
        # Get user input
        username = self.username_input.text
        password = self.password_input.text

        # Connect to the database
        db_connection = mysql.connector.connect(
            host='your_host',
            user='your_user',
            password='your_password',
            database='your_database'
        )

        # Create a cursor
        cursor = db_connection.cursor()

        # Execute the SQL query to check if the user exists in the 'users' table
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))

        # Fetch the result
        result = cursor.fetchone()

        # Close the cursor and connection
        cursor.close()
        db_connection.close()

        if result:
            print(f"Signin Successful: Username: {username}")
            # Transition to the Home screen
            self.manager.current = 'home'
        else:
            print("Signin Failed: Invalid username or password")


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        self.layout.add_widget(Label(text='Home Page', font_size='20sp'))
        self.add_widget(self.layout)


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(SignupScreen(name='signup'))
        sm.add_widget(SigninScreen(name='signin'))
        sm.add_widget(HomeScreen(name='home'))
        return sm


# if __name__ == '__main__':
#     MyApp().run()
