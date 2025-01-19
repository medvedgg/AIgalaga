
import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galaga")

# Define a Font for displaying the score
font = pygame.font.Font(None, 36)


class Player:
    def __init__(self):
        self.image = pygame.Surface((50, 30))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        self.speed = 5

    def move(self, dx):
        self.rect.x += dx
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > WIDTH - self.rect.width:
            self.rect.x = WIDTH - self.rect.width

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Enemy:
    def __init__(self):
        self.image = pygame.Surface((50, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(random.randint(0, WIDTH), random.randint(-100, -40)))
        self.speed = random.randint(4, 6)

    def move(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.rect.y = random.randint(-100, -40)
            self.rect.x = random.randint(0, WIDTH - self.rect.width)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Bullet:
    def __init__(self, x, y):
        self.image = pygame.Surface((5, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = -10

    def move(self):
        self.rect.y += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)


def game_over_screen(surface, score):
    font = pygame.font.Font(None, 74)
    text = font.render("GAME OVER", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)

    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))
    
    surface.blit(text, text_rect)
    surface.blit(score_text, score_rect)
    pygame.display.flip()
    pygame.time.wait(3000)


def game():
    clock = pygame.time.Clock()
    player = Player()
    enemies = [Enemy() for _ in range(5)]
    bullets = []
    score = 0  # Initialize score
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Indicate the game loop should break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(-player.speed)
        if keys[pygame.K_RIGHT]:
            player.move(player.speed)
        if keys[pygame.K_SPACE]:
            if len(bullets) < 5:
                bullets.append(Bullet(player.rect.centerx, player.rect.top))

        for enemy in enemies:
            enemy.move()

        for bullet in bullets[:]:
            bullet.move()
            if bullet.rect.bottom < 0:
                bullets.remove(bullet)

        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if bullet.rect.colliderect(enemy.rect):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    enemies.append(Enemy())
                    score += 5  # Increment score on hit

        for enemy in enemies:
            if player.rect.colliderect(enemy.rect):
                game_over_screen(screen, score)
                return True  # Indicate restart

        screen.fill(BLACK)
        player.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)

        # Display the score on top left of the screen
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        pygame.display.flip()
        clock.tick(FPS)

    return False


def main():
    restart = True
    while restart:
        restart = game()  # Run the game and check the return value for restart
    pygame.quit()


if __name__ == "__main__":
    main()
