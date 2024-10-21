import pygame
import random

# Pygame-ni boshlash
pygame.init()

# Ekran o'lchami
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Ranglar
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)  # Tangalar rangi

# O'yin tezligi va vaqt
clock = pygame.time.Clock()

# Personaj classi
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))  # 30x30 piksel o'lchamida
        self.image.fill(GREEN)  # Oq yashil rangdagi kvadrat
        self.rect = self.image.get_rect()
        self.rect.center = (100, SCREEN_HEIGHT // 2)
        self.speed_y = 0
        self.jump_count = 0  # Sakrashlar sonini kuzatish

    def update(self):
        self.speed_y += 1  # Gravitatsiya
        self.rect.y += self.speed_y

        # Yerga tushish
        if self.rect.bottom > SCREEN_HEIGHT - 10:
            self.rect.bottom = SCREEN_HEIGHT - 10
            self.speed_y = 0
            self.jump_count = 0  # Yerga tushganda sakrashlar soni tiklanadi

    def jump(self):
        if self.jump_count < 10000:  # Faqat 2 marta sakrash imkoniyati
            self.speed_y = -20  # Sakrash kuchi
            self.jump_count += 1  # Sakrashlar sonini oshiramiz

# To'siqlar classi
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x -= 5  # To'siqlar harakatlanishi
        if self.rect.right < 0:
            self.kill()  # Ekrandan chiqib ketgan to'siqlarni o'chirib tashlash

# Tanga classi
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x -= 5  # Tangalar harakatlanishi
        if self.rect.right < 0:
            self.kill()  # Ekrandan chiqib ketgan tangalarni o'chirish

# Funksiya: To'siqlar yaratish
def spawn_obstacle():
    obstacle_height = random.randint(50, 200)  # To'siq balandligi oshirildi
    obstacle = Obstacle(SCREEN_WIDTH, SCREEN_HEIGHT - obstacle_height - 10, 20, obstacle_height)
    all_sprites.add(obstacle)
    obstacles.add(obstacle)


# Funksiya: Tangalar yaratish
def spawn_coin():
    coin_y = random.randint(50, SCREEN_HEIGHT - 50)  # Tangalar ekrandagi tasodifiy joylarda paydo bo'ladi
    coin = Coin(SCREEN_WIDTH, coin_y)
    all_sprites.add(coin)
    coins.add(coin)

# Sprite to'plamlari
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
coins = pygame.sprite.Group()

# O'yinchini yaratish
player = Player()
all_sprites.add(player)

# O'yin sanagichlari
obstacle_passed = 0
coins_collected = 0
game_over = False
won = False

# O'yinni qayta boshlash funksiyasi
def reset_game():
    global obstacle_passed, coins_collected, game_over, won
    obstacle_passed = 0
    coins_collected = 0
    game_over = False
    won = False
    all_sprites.empty()
    obstacles.empty()
    coins.empty()
    all_sprites.add(player)
    player.rect.center = (100, SCREEN_HEIGHT // 2)

# O'yin sikli
running = True
while running:
    clock.tick(60)  # O'yin tezligi

    # Eventlarni qayta ishlash
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == 1073741906:  # Bu PgUp tugmasining kodi
                player.jump()
            if event.key == pygame.K_r and game_over:  # O'yin tugagach qayta boshlash tugmasi
                reset_game()

    # O'yin mexanikasi
    if not game_over:
        all_sprites.update()

        # O'yinchi to'siqlarga urildimi?
        if pygame.sprite.spritecollideany(player, obstacles):
            game_over = True

        # O'yinchi tangalarni yutsami?
        coins_hit = pygame.sprite.spritecollide(player, coins, True)  # O'yinchi tangaga urilsa, tanga o'chiriladi
        coins_collected += len(coins_hit)  # Har safar yutgan tanga sonini qo'shamiz

        # To'siqlarni sanash
        for obstacle in obstacles:
            if obstacle.rect.right < player.rect.left and not obstacle.rect.right < 0:
                obstacle_passed += 1
                obstacle.kill()  # O'tilgan to'siqni o'chiramiz

        # O'yinchi 10 ta to'siqdan o'tganini tekshirish
        if obstacle_passed >= 50:
            won = True
            game_over = True

        # To'siqlarni va tangalarni tasodifiy yaratish
        if random.randint(1, 100) < 3:
            spawn_obstacle()
        if random.randint(1, 100) < 3:  # Tangalar ham tasodifiy paydo bo'ladi
            spawn_coin()

    # Ekranni yangilash
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # O'yin tugaganini va g'olib bo'lganini ko'rsatish
    font = pygame.font.SysFont(None, 36)
    if game_over:
        if won:
            text = font.render(f'G\'olib bo\'ldingiz! Yig\'ilgan tangalar: {coins_collected} | Yana o\'ynash uchun R bosing', True, BLACK)
        else:
            text = font.render(f'O\'yin tugadi! Yig\'ilgan tangalar: {coins_collected} | Yana o\'ynash uchun R bosing', True, BLACK)
        screen.blit(text, (100, SCREEN_HEIGHT // 2))
    else:
        # To'siqdan o'tganlar va yig'ilgan tangalar sonini ko'rsatish
        text = font.render(f'To\'siqlardan o\'tdingiz: {obstacle_passed} | Tangalar: {coins_collected}', True, BLACK)
        screen.blit(text, (10, 10))

    pygame.display.flip()

pygame.quit()
