class Screen:
    def __init__(self, w: int, h: int):
        self.w = w
        self.h = h
        self.buffer: list[list[str]] = [list(((" " * w))) for _ in range(h)]

    def put_char(self, c: str, x: int, y: int):
        try:
            self.buffer[y][x] = c
        except IndexError:
            # Ignore drawing off screen
            ...
