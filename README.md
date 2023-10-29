# terminal-drawing
A simple CLI tool drawing to a terminal.  This was made as part of a coding test.

The work here represents two evenings of work.  I have expanded on the origonal prompt and incorporated a save functionality that allows me to export the drawing and use it to draw a game level from a tilesheet using pygame.

## Requirements

Python 3.9


## Quick Start

```bash
python3 cli
```

Make a drawing and save it.

```bash
python3 game $PATH_TO_SAVED_DRAWING
```

## Origonal prompt

### Instructions

You are free to use any programming language you like but we prefer to see Python, JavaScript,
TypeScript or Java. We do not expect you to spend more than an evening or two on this. If you get stuck,
feel free to reach out or make an explicit assumption. We are focusing on your choices and approaches
rather than exact implementation.

### The task

Write a small application (e.g., for the terminal) that can draw shapes using ASCII characters.

The following commands should be supported:

- NEW <w> <h> Create a new drawing area with dimensions w*h.
- CHA <c> Change drawing character to <c>.
- LIN <x1> <y1> <x2> <y2> Draw a line from point (x1,y1) to (x2,y2).
- REC <x1> <y1> <x2> <y2> Draw a rectangle with the left upper corner in (x1,y1) and the lower right corner in (x2, y2).
- FILL <x> <y> Fill the entire area connected to (x,y). I.e., all connected spaces with the same character as (x, y).
