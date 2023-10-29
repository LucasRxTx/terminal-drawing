from screen import Screen
from application import Application

if __name__ == "__main__":
    app = Application(Screen(10, 10), "x")
    app.run()
