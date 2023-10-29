from application import Application
from screen import Screen

if __name__ == "__main__":
    app = Application(Screen(10, 10), "x")
    app.run()
