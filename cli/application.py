from dataclasses import dataclass
from typing import Callable
from command import (
    NewCommand,
    LineCommand,
    ChangeCharCommand,
    RawCommand,
    RectangleCommand,
    FillCommand,
    HelpCommand,
    SaveCommand,
    LoadCommand,
    ExitCommand,
    command_registry,
)
from screen import Screen
from pathlib import Path
from shapes import Line, Point, Rectangle, ShapeProtocol
from exceptions import InvalidCommandException
import constants


@dataclass
class Application:
    """Application class for CLI.

    params:
        screen: The screen object we are drawing too.
        char: The character that will be drawn to the screen.
        error_message: An error message from the last tick.
        should_print_help: A flag to indicate if a help message should be displayed.
        output: A sink for program output.  Defaults to python's `print` function.
    """

    screen: Screen
    char: str = "x"
    running: bool = True
    error_message: str = ""
    should_print_help: bool = True
    output: Callable[[str], None] = print

    @staticmethod
    def parse_command(
        cmd: str,
    ):
        """Parse raw string input into a command object."""
        raw_command = RawCommand.from_str(cmd)
        return command_registry[raw_command.kind].from_raw_command(
            raw_command=raw_command
        )

    def print_help(self):
        """Print a help message."""
        self.output("=== Commands ===")
        self.output("HELP")
        self.output("NEW <w> <h>")
        self.output("CHA <c>")
        self.output("LIN <x1> <y1> <x2> <y2>")
        self.output("REC <x1> <y1> <x2> <y2>")
        self.output("FILL <x> <y>")
        self.output("SAVE <filename>")
        self.output("LOAD <filename>")
        self.output("")

    def handle_command(self, command):
        """Handle a command.

        params:
            command: A command object to execute.
        """
        match command:
            case NewCommand(w, h):
                self.new_screen(w=w, h=h)
            case ChangeCharCommand(c):
                self.set_draw_character(character=c)
            case LineCommand(x1, y1, x2, y2):
                self.draw_shape(
                    Line(
                        Point(x1, y1),
                        Point(x2, y2),
                    ),
                )
            case RectangleCommand(x1, y1, x2, y2):
                self.draw_shape(
                    Rectangle(
                        Point(x1, y1),
                        Point(x2, y2),
                    )
                )
            case FillCommand(x, y):
                self.fill_area(x, y)
            case HelpCommand():
                self.should_print_help = True
            case SaveCommand(filename):
                self.save(filename)
            case LoadCommand(filename):
                self.load(filename)
            case ExitCommand():
                self.running = False

    def save(self, filename: str):
        """Save a screen to a file.

        If file already exists, user will be prompted to overwrite.

        params:
            filename: Path to save file to.
        """
        path = Path(filename)
        if path.exists():
            answer = input(f"{path} already exists.  Overwrite? [y, n] > ")
            if answer.upper() not in ("Y", "YES"):
                self.output("Save aborted.")
                return

        with path.open("w") as f:
            f.writelines(("".join(line) + "\n" for line in self.screen.buffer))

        self.output("Save successfull.")

    def load(self, filename: str):
        """Load a screen from a file.

        params:
            filename: Path to file to load.
        """
        path = Path(filename)
        if not path.exists():
            self.output(f"{path} does not exist.")

        if not path.is_file():
            self.output(f"{path} is not a file.")

        raw_data: list[list[str]] = []
        with path.open("r") as f:
            for i, line in enumerate(f.readlines()):
                raw_data.append([c for c in line.rstrip("\n")])

        if not raw_data:
            self.output("File was empty.  Abort.")
            return

        h = len(raw_data)
        w = len(raw_data[0])
        self.new_screen(w=w, h=h)

        for y, line in enumerate(raw_data):
            for x, c in enumerate(line):
                self.screen.put_char(c, x, y)

        self.output("Load Successfull.")

    def print_screen(self):
        """Print screen with the application output function."""
        top_nums = "│".join(str(i % 10) for i in range(self.screen.w))
        header = "╤".join(c for c in "═" * self.screen.w)
        mid = "┼".join(c for c in "─" * self.screen.w)
        bottom = "╧".join(c for c in "═" * self.screen.w)

        self.output("│" + top_nums + "│")
        self.output("╔" + header + "╗")

        last_line = len(self.screen.buffer) - 1
        for i, line in enumerate(self.screen.buffer):
            self.output("║" + "│".join(line) + f"║ {i}")
            if i < last_line:
                self.output("╟" + mid + "╢")

        self.output("╚" + bottom + "╝")

    def handle_user_input(self):
        command_from_input = input("> ")
        try:
            command = self.parse_command(command_from_input)
            self.handle_command(command=command)
        except InvalidCommandException as e:
            self.error_message = str(e)

    def print_system_messages(self):
        if self.should_print_help:
            self.print_help()
            self.should_print_help = False

        if self.error_message:
            self.output("error: ", self.error_message)
            self.error_message = ""

    def run(self):
        """Run the CLI."""
        while self.running:
            try:
                self.output(constants.CLEAR_SCREEN)
                self.print_screen()
                self.print_system_messages()
                self.handle_user_input()
            except KeyboardInterrupt:
                self.running = False

    def new_screen(self, w: int, h: int):
        self.screen = Screen(w, h)

    def set_draw_character(self, character: str):
        self.char = character

    def draw_shape(self, shape: ShapeProtocol):
        for p in shape.points():
            self.screen.put_char(self.char, p.x, p.y)

    def __fill(self, x: int, y: int, c_to_replace: str):
        c = self.screen.buffer[y][x]
        if c != c_to_replace:
            return

        self.screen.put_char(c=self.char, x=x, y=y)
        if self.screen.w > x + 1:  # Right
            self.__fill(x=x + 1, y=y, c_to_replace=c_to_replace)

        if 0 <= x - 1:  # Left
            self.__fill(x=x - 1, y=y, c_to_replace=c_to_replace)

        if self.screen.h > y + 1:  # Below
            self.__fill(x=x, y=y + 1, c_to_replace=c_to_replace)

        if 0 <= y - 1:  # Above
            self.__fill(x=x, y=y - 1, c_to_replace=c_to_replace)

        return

    def fill_area(self, x: int, y: int):
        max_x = self.screen.w - 1  # zero indexed
        max_y = self.screen.h - 1  # zero indexed

        if max_x < x or max_y < y:
            raise InvalidCommandException("Fill position is off screen.")

        self.__fill(
            x=x,
            y=y,
            c_to_replace=self.screen.buffer[y][x],
        )
