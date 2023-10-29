import math
import sys
from collections import defaultdict
from pathlib import Path

import pygame


class LevelNotFound(Exception):
    ...


class LevelIsEmpty(Exception):
    ...


char_to_tile_index_map = defaultdict(
    lambda: 31,  # dirt
    dict(
        # brick
        a=0,
        b=1,
        c=1,
        d=2,
        e=3,
        f=4,
        g=5,
        h=6,
        i=7,
        j=8,
        k=9,
        # desert
        l=10,
        m=11,
        n=12,
        o=13,
        p=14,
        q=15,
        r=16,
        s=17,
        t=18,
        u=19,
        # Grass
        v=20,
        w=21,
        x=22,
        y=23,
        z=24,
        A=25,
        B=26,
        C=27,
        D=28,
        E=29,
        # Mud
        F=30,
        G=31,
        H=32,
        I=33,
        J=34,
        K=35,
        L=36,
        M=37,
        N=38,
        O=39,
        # Sand stone
        P=40,
        Q=41,
        R=42,
        S=43,
        T=44,
        U=45,
        V=46,
        W=47,
        X=48,
        Y=49,
        Z=50,
    ),
)


if __name__ == "__main__":
    argc = len(sys.argv)
    filename = sys.argv[1] if argc > 1 else "./resources/demo_lvl.txt"

    path = Path(filename)
    if not path.is_file():
        raise LevelNotFound(f"{path} not found.")

    level_data = []
    with path.open("r") as f:
        for line in f.readlines():
            level_data.append([c for c in line.rstrip("\n")])

    if not level_data:
        raise LevelIsEmpty(f"Level file {path} did not contain data.")

    pygame.init()
    screen = pygame.display.set_mode([500, 500])
    screen.convert()

    tile_set = pygame.image.load("./resources/map_tileset.png").convert()
    tile_count_width = 10
    tile_count_height = 5
    tile_width = math.ceil(tile_set.get_width() / tile_count_width)
    tile_height = math.ceil(tile_set.get_height() / tile_count_height)
    tiles: list[pygame.Surface] = []
    for y in range(tile_count_height):
        for x in range(tile_count_width):
            rect = pygame.Rect(
                x * tile_width,
                y * tile_height,
                tile_width,
                tile_height,
            )
            image = pygame.Surface(rect.size).convert()
            image.blit(tile_set, (0, 0), rect)
            tiles.append(image)

    level_tile_count_height = len(level_data)
    level_tile_count_width = len(level_data[0])

    screen_width = tile_width * level_tile_count_width
    screen_height = tile_height * level_tile_count_height
    screen = pygame.display.set_mode([screen_width, screen_height])
    screen.convert()

    # Run until the user asks to quit
    running = True
    while running:
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the background with white
        screen.fill((255, 255, 255))
        for y, line in enumerate(level_data):
            for x, c in enumerate(line):
                tile = tiles[char_to_tile_index_map[c]]
                screen.blit(
                    tile,
                    (x * tile_width, y * tile_height),
                    (0, 0, tile_width, tile_height),
                )

        # Flip the display
        pygame.display.flip()

    # Done! Time to quit.
    pygame.quit()
