import pygame
import math

WIDTH, HEIGHT = 1000, 800
FPS = 60
CENTER = [WIDTH // 2, HEIGHT // 2]

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SUN_COLOR = (255, 255, 0)
GRAY = (100, 100, 100)
BTN_COLOR = (50, 50, 50)


class Planet:
    def __init__(self, name, orbit_radius, speed, size, color, start_angle):
        self.name = name
        self.base_orbit = orbit_radius * 80
        self.speed = speed
        self.size = size
        self.color = color
        self.angle = math.radians(start_angle)

    def update(self, speed_multiplier, is_paused):
        if not is_paused:
            self.angle += self.speed * speed_multiplier

    def draw(self, surface, zoom, font):
        x = CENTER[0] + math.cos(self.angle) * self.base_orbit * zoom
        y = CENTER[1] + math.sin(self.angle) * self.base_orbit * zoom

        current_size = max(4, min(40, self.size * zoom))

        pygame.draw.circle(
            surface, (40, 40, 40), CENTER, int(self.base_orbit * zoom), 1
        )
        pygame.draw.circle(surface, self.color, (int(x), int(y)), int(current_size))

        text = font.render(self.name, True, WHITE)
        surface.blit(text, (x - text.get_width() // 2, y - current_size - 20))


def draw_button(screen, rect, text, font):
    pygame.draw.rect(screen, BTN_COLOR, rect)
    pygame.draw.rect(screen, WHITE, rect, 1)
    txt_surf = font.render(text, True, WHITE)
    screen.blit(
        txt_surf, (rect.x + (rect.width - txt_surf.get_width()) // 2, rect.y + 10)
    )


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Солнечная система")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 14)
    btn_font = pygame.font.SysFont("Arial", 16)

    planets = [
        Planet("Меркурий", 1.0, 0.05, 5, (169, 169, 169), 0),
        Planet("Венера", 1.5, 0.03, 8, (255, 165, 0), 30),
        Planet("Земля", 2.0, 0.02, 9, (0, 0, 255), 60),
        Planet("Марс", 2.5, 0.015, 7, (255, 0, 0), 90),
        Planet("Юпитер", 3.5, 0.01, 15, (210, 180, 140), 120),
        Planet("Сатурн", 4.5, 0.008, 13, (238, 232, 170), 150),
        Planet("Уран", 5.5, 0.006, 11, (175, 238, 238), 180),
        Planet("Нептун", 6.5, 0.005, 11, (65, 105, 225), 210),
    ]

    zoom = 1.0
    speed_multiplier = 1.0
    is_paused = False

    btn_pause = pygame.Rect(20, 20, 100, 40)
    btn_fast = pygame.Rect(130, 20, 100, 40)
    btn_slow = pygame.Rect(240, 20, 100, 40)
    btn_plus = pygame.Rect(350, 20, 40, 40)
    btn_minus = pygame.Rect(400, 20, 40, 40)

    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_pause.collidepoint(event.pos):
                    is_paused = not is_paused
                if btn_fast.collidepoint(event.pos):
                    speed_multiplier *= 1.5
                if btn_slow.collidepoint(event.pos):
                    speed_multiplier /= 1.5
                if btn_plus.collidepoint(event.pos):
                    zoom *= 1.2
                if btn_minus.collidepoint(event.pos):
                    zoom /= 1.2
            if event.type == pygame.MOUSEWHEEL:
                zoom += event.y * 0.1
                zoom = max(0.1, min(5.0, zoom))

        pygame.draw.circle(screen, SUN_COLOR, CENTER, int(30 * zoom))
        sun_text = font.render("СОЛНЦЕ", True, SUN_COLOR)
        screen.blit(
            sun_text, (CENTER[0] - sun_text.get_width() // 2, CENTER[1] - 50 * zoom)
        )

        for planet in planets:
            planet.update(speed_multiplier, is_paused)
            planet.draw(screen, zoom, font)

        draw_button(screen, btn_pause, "Пауза" if not is_paused else "Пуск", btn_font)
        draw_button(screen, btn_fast, "Быстрее", btn_font)
        draw_button(screen, btn_slow, "Медленнее", btn_font)
        draw_button(screen, btn_plus, "+", btn_font)
        draw_button(screen, btn_minus, "-", btn_font)

        info_text = font.render(
            f"Скорость: {speed_multiplier:.1f}x  Масштаб: {int(zoom*100)}%", True, WHITE
        )
        screen.blit(info_text, (460, 30))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
