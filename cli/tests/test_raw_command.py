import unittest

from command import RawCommand
from exceptions import InvalidCommandException


class TestRawCommand(unittest.TestCase):
    def test_given_valid_command_string_then_a_raw_command_is_returned(self):
        commands = [
            # (Command, expected count)
            ("LIN 0 0 1 1", 4),
            ("NEW 100 300", 2),
            ("CHA x", 1),
            ("LIN 0 0 100 100", 4),
            ("REC 1 1 20 20", 4),
            ("FILL 5 5", 2),
        ]

        for command, expected_param_count in commands:
            with self.subTest(command=command):
                try:
                    raw_command = RawCommand.from_str(command)
                except Exception as e:
                    self.fail(f"Unable to parse command `{command}`, {e}")

                self.assertEqual(
                    len(raw_command.params),
                    expected_param_count,
                    "Number of parameters for command did not match number parsed.",
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
