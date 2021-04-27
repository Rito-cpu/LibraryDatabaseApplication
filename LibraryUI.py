import threading

import kivy
from kivy.app import App
from kivy.properties import ListProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
import mysql.connector
from mysql.connector import Error
from urllib.parse import urlparse


class LoginMenu(Screen):
    # Process to connect to Database
    jdbc = "jdbcmysql://library-app-instance-1.ckyrcuyndxij.us-east-2.rds.amazonaws.com:3306"
    parseResult = urlparse(jdbc)
    dbConnection = None
    try:
        dbConnection = mysql.connector.connect(host=parseResult.hostname,
                                               user="admin",
                                               password="password",
                                               database="libraryapp")
    except Error as e:
        print(e)

    # Prepare variables to issue SQL commands
    credQuery = ""
    cursor = dbConnection.cursor()
    records = ""
    tupleHolder = ""

    # Made this for easy login
    testUser = "a"
    testPassword = "a"

    # Function that logs in a user through checking database for their credentials and moves to main menu
    def onLogin(self):
        self.credQuery = "select username, password from member\nwhere username=%s"
        self.tupleExample = (self.ids.textinput_username.text,)
        self.cursor.execute(self.credQuery, self.tupleExample)
        if (self.ids.textinput_username.text == self.testUser and
                self.ids.textinput_password.text == self.testPassword):
            self.manager.current = "mainmenu"
            self.ids.textinput_username.text = ""
            self.ids.textinput_password.text = ""
        elif (self.cursor.fetchone()):
            self.manager.current = "mainmenu"
            self.ids.textinput_username.text = ""
            self.ids.textinput_password.text = ""


class SignupMenu(Screen):
    jdbc = "jdbcmysql://library-app-instance-1.ckyrcuyndxij.us-east-2.rds.amazonaws.com:3306"
    parseResult = urlparse(jdbc)
    dbConnection = None
    try:
        dbConnection = mysql.connector.connect(host=parseResult.hostname,
                                               user="admin",
                                               password="password",
                                               database="libraryapp")
    except Error as e:
        print(e)

    addQuery = ""
    cursor = dbConnection.cursor()
    records = ""
    tupleHolder = ""

    def submit(self):
        # insert into member (username, password)\nvalues ()
        if (self.ids.signup_username.text != "" and self.ids.signup_password.text != ""):
            self.addQuery = "insert into member (username, password)\nvalues (%s, %s)"
            self.tupleHolder = (self.ids.signup_username.text, self.ids.signup_password.text,)
            # self.cursor.execute(self.addQuery, (self.ids.signup_username.text, self.ids.signup_password.text))
            self.cursor.execute(self.addQuery, self.tupleHolder)


class MainMenu(Screen):
    pass


class LibraryMenu(Screen):
    books = ["test", 'test2', 'test4']
    bad_chars = ['{', '}', "'"]

    def getbooksthread(self):
        threading.Thread(target=self.getbooks).start()

    def getbooks(self):
        self.books = []
        # connectDB()
        jdbc = "jdbcmysql://library-app-instance-1.ckyrcuyndxij.us-east-2.rds.amazonaws.com:3306"
        parseResult = urlparse(jdbc)
        dbConnection = None
        try:
            dbConnection = mysql.connector.connect(host=parseResult.hostname,
                                                   user="admin",
                                                   password="password",
                                                   database="libraryapp")
        except Error as e:
            print(e)

        self.getQuery = ""
        self.cursor = dbConnection.cursor()
        # cursor.execute(getQuery)
        # records = cursor.fetchall()
        self.records = ""
        if (self.ids.userSearch.text == ""):
            self.getQuery = "select name, author_fname, author_lname, ISBN, genre, stock from books"
            self.cursor.execute(self.getQuery)
            self.records = self.cursor.fetchall()
        else:
            self.getQuery = "select name, author_fname, author_lname, ISBN, genre, stock from books\nwhere name like '%" + self.ids.userSearch.text + "%'"
            self.cursor.execute(self.getQuery)
            self.records = self.cursor.fetchall()

        # create data_items
        for row in self.records:
            for col in row:
                if col is row[4]:
                    col = ' '.join(i for i in col if not i in self.bad_chars)
                self.books.append(col)

        self.ids.bookstable.data = [{'text': str(x)} for x in self.books]
        self.ids.bookstable.refresh_from_viewport()

    def clearSearch(self):
        self.ids.userSearch.text = ""
        self.ids.dbentry.text = ""


class SelectableRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior, RecycleGridLayout):
    pass


class Book(RecycleDataViewBehavior, Label):
    pass


class Hlabel(Label):
    pass


class CheckoutMenu(Screen):
    pass


class MyBooksMenu(Screen):
    pass


class LibraryInterfaceApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LibraryMenu(name='librarymenu'))
        sm.add_widget(LoginMenu(name='loginmenu'))
        sm.add_widget(SignupMenu(name='signupmenu'))
        sm.add_widget(MainMenu(name='mainmenu'))

        sm.add_widget(CheckoutMenu(name='checkoutmenu'))
        sm.add_widget(MyBooksMenu(name='mybooksmenu'))
        return sm


if __name__ == "__main__":
    LibraryInterfaceApp().run()
