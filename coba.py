"""
DAFTAR PERUBAHAN (MODIFIKASI) DARI KODE ASLI GEEKSFORGEEKS:
1. Arsitektur OOP: Membungkus fungsi main() yang prosedural menjadi class `GameManager` untuk enkapsulasi penuh.
2. Polimorfisme Class Block: Menambahkan parameter `block_type` (normal, hard, indestructible, bonus) dengan health dan skor berbeda.
3. Level Progression: Menambahkan logika naik level (kecepatan bola bertambah) jika semua balok yang bisa dihancurkan habis.
4. Fisika Pantulan Striker: Pantulan sumbu X bola sekarang merespons dan mengikuti arah pergerakan striker.
5. Visual & Performa: Mengubah resolusi menjadi 800x600, menaikkan FPS menjadi 60, menggunakan tema Dark/Cyberpunk, dan menambahkan garis luar (border) pada objek.
6. Bug Fix Font: Mengganti pemanggilan font eksternal 'freesansbold.ttf' menjadi font bawaan (None) agar tidak error saat dieksekusi.
"""

import pygame
import random

pygame.init()

# MODIFIKASI: Mengubah resolusi layar dan skema warna menjadi "Dark/Cyberpunk Theme".
WIDTH, HEIGHT = 800, 600
BG_COLOR = (15, 15, 20)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)       # Warna Striker (Paddle)
GREEN = (57, 255, 20)      # Normal Block
PURPLE = (191, 0, 255)     # Hard Block (Butuh 2 hit)
RED = (255, 50, 50)        # Indestructible Block (Tidak bisa hancur)
GOLD = (255, 215, 0)       # Bonus Block (Skor tinggi)

# MODIFIKASI: Menggunakan font default bawaan Pygame agar tidak error "FileNotFoundError"
font = pygame.font.Font(None, 18)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cyber Brick Breaker - OOP Mod")
clock = pygame.time.Clock()

# MODIFIKASI: Mengubah FPS dari 30 ke 60 agar pergerakan gameplay jauh lebih mulus.
FPS = 60 

# Helper Function
def collisionChecker(rect, ball_rect):
    if pygame.Rect.colliderect(rect, ball_rect):
        return True
    return False

# MODIFIKASI: Meng-upgrade class Block agar mendukung berbagai tipe (Polimorfisme sederhana).
class Block:
    def __init__(self, posx, posy, width, height, block_type):
        self.posx, self.posy = posx, posy
        self.width, self.height = width, height
        self.block_type = block_type
        
        # Inisialisasi atribut berdasarkan tipe block
        if block_type == "normal":
            self.color = GREEN
            self.health = 100
            self.score_value = 5
        elif block_type == "hard":
            self.color = PURPLE
            self.health = 200
            self.score_value = 15
        elif block_type == "bonus":
            self.color = GOLD
            self.health = 100
            self.score_value = 50
        elif block_type == "indestructible":
            self.color = RED
            self.health = -1 # health -1 menandakan block abadi
            self.score_value = 0
            
        self.damage = 100
        self.blockRect = pygame.Rect(self.posx, self.posy, self.width, self.height)
        
    def display(self):
        # Tampilkan block jika health > 0 atau jika tipe indestructible (-1)
        if self.health > 0 or self.health == -1:
            pygame.draw.rect(screen, self.color, self.blockRect)
            # MODIFIKASI: Memberikan efek garis luar (border) putih pada blok
            pygame.draw.rect(screen, WHITE, self.blockRect, 1)

    def hit(self):
        if self.health > 0:
            self.health -= self.damage
            # Jika "hard" block terkena 1x hit, ubah warnanya menjadi hijau (normal)
            if self.health == 100:
                self.color = GREEN

    def getRect(self):
        return self.blockRect

    def getHealth(self):
        return self.health

class Striker:
    def __init__(self, posx, posy, width, height, speed, color):
        self.posx, self.posy = posx, posy
        self.width, self.height = width, height
        self.speed = speed
        self.color = color
        self.strikerRect = pygame.Rect(self.posx, self.posy, self.width, self.height)

    def display(self):
        pygame.draw.rect(screen, self.color, self.strikerRect)
        # MODIFIKASI: Tambahan efek border putih pada paddle/striker
        pygame.draw.rect(screen, WHITE, self.strikerRect, 2)

    def update(self, xFac):
        self.posx += self.speed * xFac
        # Mencegah paddle keluar dari layar
        if self.posx <= 0:
            self.posx = 0
        elif self.posx + self.width >= WIDTH:
            self.posx = WIDTH - self.width
        self.strikerRect = pygame.Rect(self.posx, self.posy, self.width, self.height)

    def getRect(self):
        return self.strikerRect

class Ball:
    def __init__(self, posx, posy, radius, speed, color):
        self.posx, self.posy = posx, posy
        self.radius = radius
        self.speed = speed
        self.color = color
        self.xFac, self.yFac = 1, -1
        # Collision presisi menggunakan radius bola
        self.ballRect = pygame.Rect(self.posx - self.radius, self.posy - self.radius, self.radius*2, self.radius*2)

    def display(self):
        pygame.draw.circle(screen, self.color, (self.posx, self.posy), self.radius)

    def update(self):
        self.posx += self.xFac * self.speed
        self.posy += self.yFac * self.speed

        # Pantulan dari dinding vertikal
        if self.posx - self.radius <= 0 or self.posx + self.radius >= WIDTH:
            self.xFac *= -1
        # Pantulan dari atap
        if self.posy - self.radius <= 0:
            self.yFac *= -1

        self.ballRect = pygame.Rect(self.posx - self.radius, self.posy - self.radius, self.radius*2, self.radius*2)

        # Jika bola menyentuh dasar layar
        if self.posy >= HEIGHT:
            return True # life lost
        return False

    def reset(self):
        # Kembalikan bola ke posisi aman
        self.posx = WIDTH // 2
        self.posy = HEIGHT - 150
        self.xFac, self.yFac = random.choice([1, -1]), -1

    def hit(self):
        self.yFac *= -1
        
    def getRect(self):
        return self.ballRect

# MODIFIKASI: Menerapkan class GameManager untuk membungkus fungsi main() yang sebelumnya berantakan.
class GameManager:
    def __init__(self):
        self.running = True
        self.lives = 3
        self.score = 0
        self.level = 1
        self.ball = Ball(WIDTH//2, HEIGHT - 150, 8, 6, WHITE)
        self.striker = Striker(
            WIDTH//2 - 50, HEIGHT - 50, 100, 15, self.ball.speed * 2, CYAN
        )
        self.strikerXFac = 0
        
        self.blockWidth, self.blockHeight = 60, 20
        self.horizontalGap, self.verticalGap = 15, 15
        self.listOfBlocks = self.populateBlocks()

    def populateBlocks(self):
        blocks = []
        # MODIFIKASI: Random generator dengan probabilitas agar level lebih variatif.
        types = ["normal", "hard", "indestructible", "bonus"]
        weights = [60, 25, 5, 10] # Persentase kemungkinan kemunculan tiap tipe blok
        
        for i in range(20, WIDTH - self.blockWidth, self.blockWidth + self.horizontalGap):
            for j in range(40, HEIGHT // 2, self.blockHeight + self.verticalGap):
                b_type = random.choices(types, weights=weights, k=1)[0]
                blocks.append(Block(i, j, self.blockWidth, self.blockHeight, b_type))
        return blocks

    def gameOverScreen(self):
        go = True
        while go:
            screen.fill(BG_COLOR)
            over_text = font.render(f"GAME OVER! Final Score: {self.score}", True, WHITE)
            restart_text = font.render("Press SPACE to Restart or ESC to Quit", True, CYAN)
            screen.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//2 - 20))
            screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 20))
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return True
                    if event.key == pygame.K_ESCAPE:
                        return False

    def run(self):
        while self.running:
            screen.fill(BG_COLOR)
            
            # UI
            score_text = font.render(f"Score : {self.score}", True, WHITE)
            lives_text = font.render(f"Lives : {self.lives}", True, WHITE)
            level_text = font.render(f"Level : {self.level}", True, CYAN)
            screen.blit(score_text, (20, 10))
            screen.blit(lives_text, (WIDTH - 100, 10))
            screen.blit(level_text, (WIDTH // 2 - 40, 10))

            # MODIFIKASI: Level Progression. Jika block selain "indestructible" habis, level naik.
            destructibles = [b for b in self.listOfBlocks if b.health > 0]
            if not destructibles:
                self.level += 1
                self.ball.speed += 1 # Bola semakin cepat setiap naik level
                self.listOfBlocks = self.populateBlocks()
                self.ball.reset()

            if self.lives <= 0:
                restart = self.gameOverScreen()
                if restart:
                    self.lives = 3
                    self.score = 0
                    self.level = 1
                    self.ball.speed = 6
                    self.listOfBlocks = self.populateBlocks()
                    self.ball.reset()
                else:
                    self.running = False
                continue

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.strikerXFac = -1
                    if event.key == pygame.K_RIGHT:
                        self.strikerXFac = 1
                if event.type == pygame.KEYUP:
                    if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                        self.strikerXFac = 0

            # Collision Striker dengan Bola
            if collisionChecker(self.striker.getRect(), self.ball.getRect()):
                self.ball.hit()
                # MODIFIKASI: Mengubah arah pantulan X bola mengikuti arah gerak Striker
                if self.strikerXFac != 0:
                    self.ball.xFac = self.strikerXFac

            # Collision Bola dengan Blocks
            for block in self.listOfBlocks[:]:
                if collisionChecker(block.getRect(), self.ball.getRect()):
                    self.ball.hit()
                    block.hit()
                    if block.getHealth() == 0:
                        self.score += block.score_value
                        self.listOfBlocks.remove(block)

            self.striker.speed = self.ball.speed * 2
            self.striker.update(self.strikerXFac)
            life_lost = self.ball.update()
            
            if life_lost:
                self.lives -= 1
                self.ball.reset()

            # Render semua object
            self.striker.display()
            self.ball.display()
            for block in self.listOfBlocks:
                block.display()

            pygame.display.update()
            clock.tick(FPS)

# Eksekusi Program (Titik mulai utama)
if __name__ == "__main__":
    game = GameManager()
    game.run()
    pygame.quit()