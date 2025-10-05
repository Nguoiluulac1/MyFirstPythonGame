import pygame
import sys
import random
import os

pygame.init()

# --- Cấu hình ---
WIDTH, HEIGHT = 800, 600
FPS = 60
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Human Dodge Game (Beginner)")

# Màu
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Font
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)

# --- Hàm tạo nhân vật nếu không có file ---
def make_default_player_surface(size=(64, 64)):
    surf = pygame.Surface(size, pygame.SRCALPHA)  # hỗ trợ alpha
    surf.fill((0,0,0,0))  # trong suốt
    w, h = size
    # Vẽ đầu
    pygame.draw.circle(surf, (255, 220, 170), (w//2, h//6), h//8)
    # Vẽ thân
    pygame.draw.rect(surf, (40, 110, 200), (w//2 - 10, h//4 + 6, 20, h//3))
    # Tay trái và phải
    pygame.draw.line(surf, (0,0,0), (w//2, h//3), (w//2 - 18, h//3 + 8), 4)
    pygame.draw.line(surf, (0,0,0), (w//2, h//3), (w//2 + 18, h//3 + 8), 4)
    # Chân
    pygame.draw.line(surf, (0,0,0), (w//2, h//4 + h//3 + 6), (w//2 - 12, h - 6), 4)
    pygame.draw.line(surf, (0,0,0), (w//2, h//4 + h//3 + 6), (w//2 + 12, h - 6), 4)
    return surf

# --- Tải ảnh nhân vật (nếu có), nếu không có -> tạo mặc định ---
PLAYER_SIZE = (64, 64)
player_image = None
if os.path.exists("player.png"):
    try:
        player_image = pygame.image.load("player.png").convert_alpha()
        player_image = pygame.transform.scale(player_image, PLAYER_SIZE)
    except Exception as e:
        print("Warning: couldn't load player.png:", e)
        player_image = make_default_player_surface(PLAYER_SIZE)
else:
    player_image = make_default_player_surface(PLAYER_SIZE)

player_rect = player_image.get_rect(midbottom=(WIDTH // 2, HEIGHT - 30))
PLAYER_SPEED = 7

# --- Kẻ rơi (enemy) ---
def make_enemy():
    w = 50
    x = random.randint(0, WIDTH - w)
    y = -random.randint(40, 150)
    rect = pygame.Rect(x, y, w, w)
    return rect

enemies = [make_enemy()]
enemy_speed = 5

# Điểm
score = 0

clock = pygame.time.Clock()
running = True
game_over = False

def reset_game():
    global enemies, enemy_speed, score, player_rect, game_over
    enemies = [make_enemy()]
    enemy_speed = 5
    score = 0
    player_rect.midbottom = (WIDTH // 2, HEIGHT - 30)
    game_over = False

# --- Vòng lặp chính ---
while running:
    dt = clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if game_over:
                if event.key == pygame.K_r:
                    reset_game()
                if event.key == pygame.K_q:
                    running = False

    keys = pygame.key.get_pressed()
    if not game_over:
        # di chuyển người chơi
        if keys[pygame.K_LEFT]:
            player_rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            player_rect.x += PLAYER_SPEED

        # giới hạn trong màn hình
        if player_rect.left < 0:
            player_rect.left = 0
        if player_rect.right > WIDTH:
            player_rect.right = WIDTH

        # di chuyển kẻ rơi
        for e in enemies:
            e.y += enemy_speed
            if e.top > HEIGHT:
                # reset vị trí kẻ rơi, tăng điểm
                e.x = random.randint(0, WIDTH - e.width)
                e.y = -random.randint(40, 120)
                score += 1
                # tăng độ khó theo điểm
                if score % 5 == 0:
                    enemy_speed += 1
                    # tạo thêm 1 enemy tối đa 5
                    if len(enemies) < 5:
                        enemies.append(make_enemy())

        # kiểm tra va chạm
        for e in enemies:
            if player_rect.colliderect(e):
                game_over = True

    # --- Vẽ ---
    SCREEN.fill(WHITE)
    # vẽ player
    SCREEN.blit(player_image, player_rect)
    # vẽ enemies
    for e in enemies:
        pygame.draw.rect(SCREEN, (20,20,20), e)

    # hiển thị điểm
    score_surf = font.render(f"Score: {score}", True, BLACK)
    SCREEN.blit(score_surf, (10, 10))

    if game_over:
        over_surf = big_font.render("GAME OVER", True, (180, 20, 20))
        over_rect = over_surf.get_rect(center=(WIDTH//2, HEIGHT//2 - 40))
        SCREEN.blit(over_surf, over_rect)
        hint = font.render("Press R to Restart or Q to Quit", True, BLACK)
        SCREEN.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT//2 + 20))

    pygame.display.flip()

pygame.quit()
sys.exit()
