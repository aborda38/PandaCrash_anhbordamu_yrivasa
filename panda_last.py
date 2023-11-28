import arcade
import random
import pyglet

# Window
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
# CarSize
CAR_WIDTH = 80
CAR_HEIGHT = 70
# Obstacles
OBSTACLE_WIDTH = 90
OBSTACLE_HEIGHT = 65
# Speed
CAR_SPEED = 5
OBSTACLE_SPEED = 3.5

# MUSIC
MUSIC_FILE_PATH = "music/panda_crash_m.mp3"
background_music = None

# PathFolder
PLAYER_IMAGE_PATH = "images/Car.png"
OBSTACLE_IMAGE_PATHS = ["images/Police.png"]

# Lanes(Obstacles in one line)
LANE_WIDTH = 100
LANE_SPACING = 50
LEFT_LANE_X = SCREEN_WIDTH // 2 - LANE_WIDTH - LANE_SPACING // 2
RIGHT_LANE_X = SCREEN_WIDTH // 2 + LANE_SPACING // 2


class CarGame(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height, "Panda Crash")

        # MUSIC
        global background_music
        if not background_music:
            background_music = pyglet.media.load(MUSIC_FILE_PATH)
            background_music.play()

        # Position
        self.car_x = SCREEN_WIDTH / 2
        self.car_y = 100

        self.obstacles = []
        self.score = 0
        self.game_over = False
        self.held_keys = []

        # Timer obstacles
        self.obstacle_spawn_timer = 0.0

    def spawn_obstacle(self):
        x = random.choice([LEFT_LANE_X, RIGHT_LANE_X])
        y = SCREEN_HEIGHT

        # GenerateObstacles
        while any(
            self.check_collision(
                x,
                y,
                OBSTACLE_WIDTH,
                OBSTACLE_HEIGHT,
                obstacle[0],
                obstacle[1],
                OBSTACLE_WIDTH,
                OBSTACLE_HEIGHT,
            )
            for obstacle in self.obstacles
        ):
            x = random.choice([LEFT_LANE_X, RIGHT_LANE_X])

        self.obstacles.append((x, y))

    def on_draw(self):
        arcade.start_render()

        arcade.draw_rectangle_filled(
            SCREEN_WIDTH // 2,  # Centro X
            SCREEN_HEIGHT // 2,  # Centro Y
            SCREEN_WIDTH / 1.5,  # Ancho del rectángulo
            SCREEN_HEIGHT,  # Altura del rectángulo (mitad de la pantalla)
            arcade.color.GRAY,  # Color del rectángulo
        )

        # PlayerCar
        arcade.draw_texture_rectangle(
            self.car_x,
            self.car_y,
            CAR_WIDTH,
            CAR_HEIGHT,
            arcade.load_texture(PLAYER_IMAGE_PATH),
        )

        # Obstacles_truck
        for obstacle in self.obstacles:
            x, y = obstacle
            arcade.draw_texture_rectangle(
                x + OBSTACLE_WIDTH / 2,
                y - OBSTACLE_HEIGHT / 2,
                OBSTACLE_WIDTH,
                OBSTACLE_HEIGHT,
                arcade.load_texture(random.choice(OBSTACLE_IMAGE_PATHS)),
            )

        # Score
        arcade.draw_text(
            f"Score: {self.score}",
            10,
            SCREEN_HEIGHT - 20,
            arcade.color.WHITE,
            12,
            font_name="Kenney Future",
        )

        # GameOver
        if self.game_over:
            arcade.draw_text(
                f"Score: {self.score}",
                200,
                400,
                arcade.color.WHITE,
                20,
                font_name="Kenney Future",
                anchor_x="center",
            )

            arcade.draw_text(
                "GAME OVER",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2,
                arcade.color.WHITE,
                30,
                font_name="Kenney Blocks",
                anchor_x="center",
            )

    def on_update(self, delta_time):
        if not self.game_over:
            # MovePlayerCar
            if arcade.key.LEFT in self.held_keys and self.car_x > 90:
                self.car_x -= CAR_SPEED
            if arcade.key.RIGHT in self.held_keys and self.car_x < (SCREEN_WIDTH - 90):
                self.car_x += CAR_SPEED

            # MoveObstacles
            for i in range(len(self.obstacles)):
                x, y = self.obstacles[i]
                y -= OBSTACLE_SPEED
                self.obstacles[i] = (x, y)

            # MasterObstacles (Control)
            self.obstacle_spawn_timer += delta_time
            if self.obstacle_spawn_timer > 2.0:
                self.spawn_obstacle()
                self.obstacle_spawn_timer = 0.0

            # CrashCar --> Collision
            obstacles2 = 0
            for obstacle in self.obstacles:
                obstacles2 += 1
                if self.check_collision(
                    self.car_x,
                    self.car_y,
                    CAR_WIDTH,
                    CAR_HEIGHT,
                    obstacle[0],
                    obstacle[1],
                    OBSTACLE_WIDTH,
                    OBSTACLE_HEIGHT,
                ):
                    self.game_over = True

            # DeleteObstacles
            self.obstacles = [(x, y) for x, y in self.obstacles if y > 0]

            # Score
            self.score += obstacles2

    def check_collision(self, x1, y1, w1, h1, x2, y2, w2, h2):
        margin = 5
        center_x = x1 + w1 / 2
        center_y = y1 + h1 / 2
        return (
            center_x - margin < x2 + w2
            and center_x + margin > x2
            and center_y - margin < y2 + h2
            and center_y + margin > y2
        )

    # Key_action -->
    def on_key_press(self, key, modifiers):
        if key not in self.held_keys:
            self.held_keys.append(key)

    def on_key_release(self, key, modifiers):
        if key in self.held_keys:
            self.held_keys.remove(key)


def main():
    window = CarGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()


if __name__ == "__main__":
    main()
