import unittest

from command import NewCommand, RawCommand
from exceptions import InvalidCommandException


class TestNewCommand(unittest.TestCase):
    def test_given_valid_new_command_then_a_new_command_is_returned(self):
        commands = [
            (RawCommand.from_str("NEW 200 200"), [200, 200]),
            (RawCommand.from_str("NEW 10 10"), [10, 10]),
            (RawCommand.from_str("NEW 1 1"), [1, 1]),
            (RawCommand.from_str("NEW 12 30"), [12, 30]),
            (RawCommand.from_str("NEW 1080 720"), [1080, 720]),
        ]

        for command, expected_dimensions in commands:
            with self.subTest(command=command):
                try:
                    new_command = NewCommand.from_raw_command(command)
                except Exception as e:
                    self.fail(f"Unable to parse new command `{command}`. {e}")

                self.assertEqual(
                    new_command.w,
                    expected_dimensions[0],
                    f"Expected width to be `{expected_dimensions[0]}`.  Found `{new_command.w}`.",
                )

                self.assertEqual(
                    new_command.h,
                    expected_dimensions[1],
                )

    def test_given_an_invalid_command_when_parsed_then_an_invalid_command_exception_is_raised(
        self,
    ):
        invalid_commands = [
            "CREATE 300 300",
            "LINE 100",
            "RC 0 20 30 30",
            "FIL 5",
            "this is some bad text",
            "BAD",
        ]

        for command in invalid_commands:
            with self.subTest(command=command):
                with self.assertRaises(InvalidCommandException):
                    RawCommand.from_str(command)
