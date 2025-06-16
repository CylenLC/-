import pygame

WIDTH, HEIGHT = 600, 600
BG_COLOR = (30, 30, 30)
PLAYER1_COLOR = (0, 200, 0)
PLAYER2_COLOR = (200, 0, 0)
BULLET_COLOR = (250, 250, 0)
WALL_COLOR = (80, 80, 80)

P1_CONTROLS = {
    "up": pygame.K_UP,
    "down": pygame.K_DOWN,
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT,
    "fire": pygame.K_RETURN,
}

P2_CONTROLS = {
    "up": pygame.K_w,
    "down": pygame.K_s,
    "left": pygame.K_a,
    "right": pygame.K_d,
    "fire": pygame.K_SPACE,
}

WALL_RECTS = [
    pygame.Rect(250, 100, 100, 20),
    pygame.Rect(250, 480, 100, 20),
    pygame.Rect(100, 250, 20, 100),
    pygame.Rect(480, 250, 20, 100),
    pygame.Rect(250, 250, 100, 100),
]


class Wall(pygame.sprite.Sprite):
    def __init__(self, rect):
        super().__init__()
        self.image = pygame.Surface(rect.size)
        self.image.fill(WALL_COLOR)
        self.rect = rect

walls = None
screen_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction, owner):
        super().__init__()
        self.image = pygame.Surface((6, 6))
        self.image.fill(BULLET_COLOR)
        self.rect = self.image.get_rect(center=pos)
        self.direction = pygame.Vector2(direction).normalize()
        self.speed = 8
        self.owner = owner

    def update(self):
        self.rect.move_ip(self.direction * self.speed)
        if (
            not screen_rect.contains(self.rect)
            or pygame.sprite.spritecollideany(self, walls)
        ):
            self.kill()

class Tank(pygame.sprite.Sprite):
    def __init__(self, color, pos, controls):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=pos)
        self.direction = pygame.Vector2(0, -1)
        self.speed = 4
        self.color = color
        self.controls = controls

    def handle_keys(self, keys):
        move = pygame.Vector2(0, 0)
        if keys[self.controls['left']]:
            move.x = -self.speed
            self.direction = pygame.Vector2(-1, 0)
        elif keys[self.controls['right']]:
            move.x = self.speed
            self.direction = pygame.Vector2(1, 0)
        elif keys[self.controls['up']]:
            move.y = -self.speed
            self.direction = pygame.Vector2(0, -1)
        elif keys[self.controls['down']]:
            move.y = self.speed
            self.direction = pygame.Vector2(0, 1)

        old_rect = self.rect.copy()
        self.rect.move_ip(move)
        self.rect.clamp_ip(screen_rect)
        if pygame.sprite.spritecollideany(self, walls):
            self.rect = old_rect

    def update(self, keys=None):
        if keys:
            self.handle_keys(keys)

def main():
    global walls, screen_rect
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tank Battle")
    clock = pygame.time.Clock()

    screen_rect = screen.get_rect()
    walls = pygame.sprite.Group(Wall(r) for r in WALL_RECTS)

    player1 = Tank(PLAYER1_COLOR, (WIDTH // 2, HEIGHT - 50), P1_CONTROLS)
    player2 = Tank(PLAYER2_COLOR, (WIDTH // 2, 50), P2_CONTROLS)

    tanks = pygame.sprite.Group(player1, player2)
    bullets = pygame.sprite.Group()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == player1.controls['fire']:
                    bullets.add(Bullet(player1.rect.center, player1.direction, player1))
                elif event.key == player2.controls['fire']:
                    bullets.add(Bullet(player2.rect.center, player2.direction, player2))

        keys = pygame.key.get_pressed()
        player1.update(keys)
        player2.update(keys)
        for bullet in bullets.sprites():
            bullet.update()

        # Collision detection
        for bullet in bullets.sprites():
            hit_tanks = pygame.sprite.spritecollide(bullet, tanks, False)
            for tank in hit_tanks:
                if tank is not bullet.owner:
                    tank.kill()
                    bullet.kill()

        screen.fill(BG_COLOR)
        walls.draw(screen)
        tanks.draw(screen)
        bullets.draw(screen)
        pygame.display.flip()
        clock.tick(60)

        if len(tanks) < 2:
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()
