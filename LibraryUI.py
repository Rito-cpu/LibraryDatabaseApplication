import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget 
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
import mysql.connector


class LibraryInterfaceApp(App):
    def build(self):
        sm = ScreenManager()
        return sm

if __name__ == "__main__":
    LibraryInterfaceApp().run()