import random
import pygame as pg
import pygame.locals as keys

from pathlib import Path

DIR = Path(__file__).parent.absolute()
ASSETS = DIR / "assets/game/"
SOUNDS = ASSETS / "sound"
PLAYER = ASSETS / "player"
BEERS = ASSETS / "beers"


class Size:
    BASE = WIDTH, HEIGHT = (800, 800)
    ROAD = int(WIDTH / 1.6)
    SEP = int(WIDTH / 200)


class Point:
    CENTER_RIGHT = Size.WIDTH / 2 + Size.ROAD / 4
    CENTER_LEFT = Size.WIDTH / 2 - Size.ROAD / 4
    BORDER_RIGHT = Size.WIDTH / 2 + Size.ROAD / 2
    BORDER_LEFT = Size.WIDTH / 2 - Size.ROAD / 2
    MIDDLE = Size.WIDTH / 2 - Size.SEP / 2


class Position:
    TOP_RIGHT = (Point.CENTER_RIGHT, Size.HEIGHT * 0.2)
    TOP_LEFT = (Point.CENTER_LEFT, Size.HEIGHT * 0.2)
    BOTTOM_RIGHT = (Point.CENTER_RIGHT, Size.HEIGHT * 0.8)
    BOTTOM_LEFT = (Point.CENTER_LEFT, Size.HEIGHT * 0.8)


class Color:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (60, 220, 0)
    YELLOW = (255, 240, 60)
    GRAY = (50, 50, 50)


class FontProperties:
    FAMILY = "Comic Sans MS"
    NORMAL = FAMILY, 30
    BIG = FAMILY, 90


class Game:
    rounds: int = 0
    gains: int = 0
    losses: int = 0
    running: bool = True
    paused: bool = True
    speed: int = 1


def load_random_beer() -> tuple[pg.Surface, tuple[float, float]]:
    """Returns a tuple containing a random asset surface."""
    i = random.randint(1, 5)
    beer = pg.image.load(BEERS / f"{i}.png")
    beer = pg.transform.scale(beer, (100, 100))
    beer_position = beer.get_rect()
    beer_position.center = Position.TOP_RIGHT if random.randint(0, 1) == 0 else Position.TOP_LEFT
    return beer, beer_position


def main():
    # Setup gaming window
    pg.init()
    window = pg.display.set_mode(Size.BASE)
    window.fill(Color.GREEN)
    pg.display.update()
    normal_font = pg.font.SysFont(*FontProperties.NORMAL)
    big_font = pg.font.SysFont(*FontProperties.BIG)

    beer, beer_position = load_random_beer()
    player = pg.image.load(PLAYER / "player.png")
    player = pg.transform.scale(player, (150, 150))
    player_position = player.get_rect()
    player_position.center = Position.BOTTOM_RIGHT

    # Event loop
    while Game.running:
        Game.rounds += 1

        # Increase speed
        if Game.rounds == 500:
            Game.speed += 0.30
            Game.rounds = 0
            print("Level UP", Game.speed)

        # Colision detection
        if (
            10 < (player_position[1] - beer_position[1]) < 30
            and player_position[0] == beer_position[0] - 25
        ):
            Game.gains += 1
            beer, beer_position = load_random_beer()
            sound = random.choice(["sensacional.mp3", "olha_so.mp3"])
            pg.mixer.music.load(SOUNDS / sound)
            pg.mixer.music.play(0)

        beer_position[1] += Game.speed

        # Capture keys pressed
        for event in pg.event.get(keys.KEYDOWN):
            match event.key:
                case keys.K_ESCAPE:
                    Game.running = False
                case keys.K_LEFT:
                    player_position.center = Position.BOTTOM_LEFT
                case keys.K_RIGHT:
                    player_position.center = Position.BOTTOM_RIGHT

        # Draw the road in the middle
        pg.draw.rect(window, Color.GRAY, (Point.BORDER_LEFT, 0, Size.ROAD, Size.HEIGHT))
        # Draw Separator
        pg.draw.rect(window, Color.YELLOW, (Point.MIDDLE, 0, Size.SEP, Size.HEIGHT))
        # Draw borders
        pg.draw.rect(
            window, Color.WHITE, (Point.BORDER_LEFT + Size.SEP * 2, 0, Size.SEP, Size.HEIGHT)
        )
        pg.draw.rect(
            window, Color.WHITE, (Point.BORDER_RIGHT - Size.SEP * 3, 0, Size.SEP, Size.HEIGHT)
        )
        # Game title
        title = normal_font.render(
            f"Catch a beer! bebeu: {Game.gains} vacilou: {Game.losses}", 1, Color.WHITE, Color.BLACK
        )
        window.blit(title, (Size.WIDTH / 5, 0))

        # Wait keypress to start the game
        while Game.paused:
            msg = normal_font.render("Press any key to start", 1, Color.YELLOW, Color.BLACK)
            window.blit(msg, (Size.WIDTH / 4, 100))
            pg.display.update()
            if pg.event.get(keys.KEYDOWN):
                pg.mixer.music.load(SOUNDS / "vai.mp3")
                pg.mixer.music.play(0)
                Game.paused = False

        # Game over screen
        if Game.losses > 3:
            msg = big_font.render("GAME OVER", 1, Color.YELLOW, Color.BLACK)
            window.blit(msg, (Size.WIDTH / 4, 100))
            pg.display.update()
            pg.mixer.music.load(SOUNDS / "zika.mp3")
            pg.mixer.music.play(0)
            wait_key = True
            while wait_key:
                if pg.event.get(keys.KEYDOWN):
                    wait_key = Game.running = False
                    continue

        # Position Beer
        window.blit(beer, beer_position)
        # Position player
        window.blit(player, player_position)

        # Always update the window at the end of the loop
        pg.display.update()

        # Load another beer if any beer reaches the bottom
        if beer_position[1] > Size.HEIGHT:
            Game.losses += 1
            beer, beer_position = load_random_beer()
