import pygame
from emotion_ai import detect_emotion
from game import FallingEmoji, WIDTH, HEIGHT

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Emotion Game")

background = pygame.image.load("bg.jpg")
background = pygame.transform.scale(background,(WIDTH,HEIGHT))

font = pygame.font.SysFont(None,36)

clock = pygame.time.Clock()

score = 0
misses = 0

WIN_SCORE = 3
MAX_MISSES = 3

emotions = ['angry','disgust','fear','happy','neutral','sad','surprise']

emoji_images = {
    "angry": pygame.image.load("angry.png"),
    "disgust": pygame.image.load("disgusted.jpg"),
    "fear": pygame.image.load("fear.png"),
    "happy": pygame.image.load("happy.png"),
    "neutral": pygame.image.load("neutral.png"),
    "sad": pygame.image.load("sad.png"),
    "surprise": pygame.image.load("surprise.png")
}

for key in emoji_images:
    emoji_images[key] = pygame.transform.scale(emoji_images[key],(100,100))

emojis = []
spawn_timer = 0

running = True

while running:

    screen.blit(background,(0,0))

    # Green check line
    pygame.draw.line(screen, (0,255,0), (0, HEIGHT-100), (WIDTH, HEIGHT-100), 3)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    user_emotion = detect_emotion()

    # Spawn emojis
    spawn_timer += 1

    if spawn_timer > 50 and score < WIN_SCORE and misses < MAX_MISSES:
        emojis.append(FallingEmoji(emotions))
        spawn_timer = 0

    # Update emojis
    for emoji in emojis[:]:

        emoji.update()
        emoji.draw(screen, emoji_images)

        if emoji.y > HEIGHT - 100:

            if emoji.emotion == user_emotion:
                score += 1
            else:
                misses += 1

            emojis.remove(emoji)

    # Display UI
    score_text = font.render(f"Score: {score}", True, (255,255,255))
    screen.blit(score_text,(20,20))

    emotion_text = font.render(f"Emotion: {user_emotion}", True, (255,255,255))
    screen.blit(emotion_text,(20,60))

    miss_text = font.render(f"Misses: {misses}", True, (255,0,0))
    screen.blit(miss_text,(20,100))

    # Win condition
    if score >= WIN_SCORE:

        win_text = font.render("YOU WIN!", True, (0,255,0))
        screen.blit(win_text,(WIDTH//2 - 80, HEIGHT//2))

        pygame.display.update()
        pygame.time.delay(3000)
        running = False

    # Lose condition
    if misses >= MAX_MISSES:

        lose_text = font.render("GAME OVER", True, (255,0,0))
        screen.blit(lose_text,(WIDTH//2 - 100, HEIGHT//2))

        pygame.display.update()
        pygame.time.delay(3000)
        running = False

    pygame.display.update()
    clock.tick(30)

pygame.quit()