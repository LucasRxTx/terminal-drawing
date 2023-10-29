from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol

from exceptions import InvalidCommandException


class CommandOptions(StrEnum):
    NEW = "NEW"
    CHA = "CHA"
    LIN = "LIN"
    REC = "REC"
    FILL = "FILL"
    HELP = "HELP"
    SAVE = "SAVE"
    LOAD = "LOAD"
    EXIT = "EXIT"


@dataclass(frozen=True)
class RawCommand:
    kind: CommandOptions
    params: list[str]

    @classmethod
    def from_str(
        cls: type[RawCommand],
        string: str,
    ) -> RawCommand:
        parts = string.split(" ")
        parts = [p for p in parts if p != ""]  # drop empty strings
        kind, *params = parts

        try:
            kind = CommandOptions(kind.upper())
        except ValueError as e:
            raise InvalidCommandException("Invalid command name.") from e

        return cls(
            kind=kind,
            params=params,
        )


@dataclass
class CommandProtocol(Protocol):
    def from_raw_command(
        cls: type[CommandProtocol],
        raw_command: RawCommand,
    ) -> CommandProtocol:
        ...


@dataclass
class NewCommand:
    w: int
    h: int

    @classmethod
    def from_raw_command(
        cls: type[NewCommand],
        raw_command: RawCommand,
    ) -> NewCommand:
        try:
            w, h = raw_command.params
        except ValueError as e:
            raise InvalidCommandException("Missing parameters for NEW command.") from e

        return cls(
            w=int(w),
            h=int(h),
        )


@dataclass
class ChangeCharCommand:
    c: str

    @classmethod
    def from_raw_command(
        cls: type[ChangeCharCommand],
        raw_command: RawCommand,
    ) -> ChangeCharCommand:
        try:
            c = raw_command.params[0][0]
        except IndexError as e:
            raise InvalidCommandException("Missing parameters for CHA command.") from e

        return cls(c=c)


@dataclass
class LineCommand:
    x1: int
    y1: int
    x2: int
    y2: int

    @classmethod
    def from_raw_command(
        cls: type[LineCommand],
        raw_command: RawCommand,
    ) -> LineCommand:
        try:
            x1, y1, x2, y2 = raw_command.params
        except ValueError as e:
            raise InvalidCommandException("Missing parameters for LIN command.") from e

        try:
            x1, y1, x2, y2 = [int(value) for value in [x1, y1, x2, y2]]
        except ValueError as e:
            raise InvalidCommandException(
                "Parameters for LIN command must be integers."
            ) from e

        return cls(
            x1=x1,
            y1=y1,
            x2=x2,
            y2=y2,
        )


@dataclass
class RectangleCommand:
    x1: int
    y1: int
    x2: int
    y2: int

    @classmethod
    def from_raw_command(
        cls: type[RectangleCommand],
        raw_command: RawCommand,
    ) -> RectangleCommand:
        try:
            x1, y1, x2, y2 = raw_command.params
        except ValueError as e:
            raise InvalidCommandException("Missing parameters for REC command.") from e

        try:
            x1, y1, x2, y2 = [int(value) for value in [x1, y1, x2, y2]]
        except ValueError as e:
            raise InvalidCommandException(
                "Parameters for REC command must be integers."
            ) from e

        return cls(
            x1=x1,
            y1=y1,
            x2=x2,
            y2=y2,
        )


@dataclass
class FillCommand:
    x: int
    y: int

    @classmethod
    def from_raw_command(
        cls: type[FillCommand],
        raw_command: RawCommand,
    ) -> FillCommand:
        try:
            x, y = raw_command.params
        except ValueError as e:
            raise InvalidCommandException("Missing parameters for FILL command.") from e

        try:
            x, y = [int(value) for value in [x, y]]
        except ValueError as e:
            raise InvalidCommandException(
                "Parameters for FILL command must be integers."
            ) from e

        return cls(x=x, y=y)


@dataclass
class HelpCommand:
    @classmethod
    def from_raw_command(
        cls: type[HelpCommand],
        raw_command: RawCommand,
    ) -> HelpCommand:
        return cls()


@dataclass
class ExitCommand:
    @classmethod
    def from_raw_command(
        cls: type[ExitCommand],
        raw_command: RawCommand,
    ) -> ExitCommand:
        return cls()


@dataclass
class SaveCommand:
    filename: str

    @classmethod
    def from_raw_command(
        cls: type[SaveCommand],
        raw_command: RawCommand,
    ) -> SaveCommand:
        try:
            filename, *_ = raw_command.params
        except ValueError as e:
            raise InvalidCommandException("Missing parameters for SAVE command.") from e

        return cls(filename)


@dataclass
class LoadCommand:
    filename: str

    @classmethod
    def from_raw_command(
        cls: type[LoadCommand],
        raw_command: RawCommand,
    ) -> LoadCommand:
        try:
            filename, *_ = raw_command.params
        except ValueError as e:
            raise InvalidCommandException("Missing parameters for LOAD command.") from e

        return cls(filename)


command_registry = defaultdict(
    lambda: HelpCommand,
    {
        CommandOptions.CHA: ChangeCharCommand,
        CommandOptions.FILL: FillCommand,
        CommandOptions.HELP: HelpCommand,
        CommandOptions.LIN: LineCommand,
        CommandOptions.NEW: NewCommand,
        CommandOptions.REC: RectangleCommand,
        CommandOptions.SAVE: SaveCommand,
        CommandOptions.LOAD: LoadCommand,
        CommandOptions.EXIT: ExitCommand,
    },
)
