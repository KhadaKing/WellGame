import pygame
import random
from pygame.locals import *

# --- INICIALIZAÇÃO E TELA ---
pygame.init()
LARGURA, ALTURA = 1600, 900
screen = pygame.display.set_mode((LARGURA, ALTURA), RESIZABLE)
pygame.display.set_caption("Jogo com animação completa")
clock = pygame.time.Clock()

# --- MUSICA E EFEITOS SONOROS ---
pygame.mixer.init()

# bg music
pygame.mixer.music.load("sounds/bg_music.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

# level pass
level_pass = pygame.mixer.Sound("sounds/level_pass.wav")
level_pass.set_volume(1.0)

# player
jump_sounds = [
    pygame.mixer.Sound("sounds/player/player_jump_1.wav"),
    pygame.mixer.Sound("sounds/player/player_jump_2.wav"),
    pygame.mixer.Sound("sounds/player/player_jump_3.wav")
]
for s in jump_sounds:
    s.set_volume(1.0)

fall_sounds = [
    pygame.mixer.Sound("sounds/player/player_fall_1.wav"),
    pygame.mixer.Sound("sounds/player/player_fall_2.wav"),
    pygame.mixer.Sound("sounds/player/player_fall_3.wav"),
    pygame.mixer.Sound("sounds/player/player_fall_4.wav")
]
for s in fall_sounds:
    s.set_volume(0.5)

player_death_sound = pygame.mixer.Sound("sounds/player/player_death.wav")
player_death_sound.set_volume(1.0)

# enemy
enemy_bump_sounds = [
    pygame.mixer.Sound("sounds/enemy/enemy_bump_1.wav"),
    pygame.mixer.Sound("sounds/enemy/enemy_bump_2.wav"),
    pygame.mixer.Sound("sounds/enemy/enemy_bump_3.wav"),
    pygame.mixer.Sound("sounds/enemy/enemy_bump_4.wav")
]

# --- TELA DE MORTE ---
death_overlay_surface = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
death_overlay_surface.fill((255, 0, 0, 100))  # Vermelho translúcido

# --- CONSTANTES FÍSICAS ---
VEL = 5
GRAVIDADE = 1
PULO = -20
level = 1
MAX_LEVELS = 4  # 3 níveis + “final”
GOAL_ANIM_INTERVAL = 500  # milissegundos entre trocas (0,5 s)

# --- CAMINHO BASE DAS SPRITES ---
CAMINHO_BASE = 'D:/Documentos & Arquivos/Downloads/Jogo/images'

# --- TELA DE FUNDO ---
background_img = pygame.image.load(f'{CAMINHO_BASE}/general/background_1.png').convert()

# --- SPRITES DO PLAYER ---
base_right = pygame.image.load(f'{CAMINHO_BASE}/player/player_base.png').convert_alpha()
base_left = pygame.transform.flip(base_right, True, False)

walk_right = [pygame.image.load(f'{CAMINHO_BASE}/player/player_walk_R/player_walk_R_{i}.png').convert_alpha() for i in
              range(1, 6)]
walk_left = [pygame.image.load(f'{CAMINHO_BASE}/player/player_walk_L/player_walk_L_{i}.png').convert_alpha() for i in
             range(1, 6)]

jump_neutral = [pygame.image.load(f'{CAMINHO_BASE}/player/player_jump_N/player_jump_N_{i}.png').convert_alpha() for i in
                range(1, 8)]
jump_right = [pygame.image.load(f'{CAMINHO_BASE}/player/player_jump_R/player_jump_R_{i}.png').convert_alpha() for i in
              range(1, 8)]
jump_left = [pygame.image.load(f'{CAMINHO_BASE}/player/player_jump_L/player_jump_L_{i}.png').convert_alpha() for i in
             range(1, 8)]

fall_neutral = [pygame.image.load(f'{CAMINHO_BASE}/player/player_fall_N/player_fall_N_{i}.png').convert_alpha() for i in
                range(1, 5)]
fall_right = [pygame.image.load(f'{CAMINHO_BASE}/player/player_fall_R/player_fall_R_{i}.png').convert_alpha() for i in
              range(1, 5)]
fall_left = [pygame.image.load(f'{CAMINHO_BASE}/player/player_fall_L/player_fall_L_{i}.png').convert_alpha() for i in
             range(1, 5)]

crash_neutral = [pygame.image.load(f'{CAMINHO_BASE}/player/player_crash_N/player_crash_N_{i}.png').convert_alpha() for i
                 in range(1, 6)]
crash_right = [pygame.image.load(f'{CAMINHO_BASE}/player/player_crash_R/player_crash_R_{i}.png').convert_alpha() for i
               in range(1, 6)]
crash_left = [pygame.image.load(f'{CAMINHO_BASE}/player/player_crash_L/player_crash_L_{i}.png').convert_alpha() for i in
              range(1, 6)]

player_death_img = pygame.image.load(f'{CAMINHO_BASE}/player/player_death.png').convert_alpha()

# --- SPRITES DAS PLATAFORMAS ---
wall_1 = pygame.image.load(f'{CAMINHO_BASE}/terrain/wall_1.png').convert_alpha()
wall_1_n = pygame.image.load(f'{CAMINHO_BASE}/terrain/wall_1_n.png').convert_alpha()
wall_2 = pygame.image.load(f'{CAMINHO_BASE}/terrain/wall_2.png').convert_alpha()
wall_2_n = pygame.image.load(f'{CAMINHO_BASE}/terrain/wall_2_n.png').convert_alpha()

# --- VERSÕES VERTICAIS DAS PAREDES ---
wall_1_v = pygame.transform.rotate(wall_1, 90)
wall_1_n_v = pygame.transform.rotate(wall_1_n, 90)
wall_2_v = pygame.transform.rotate(wall_2, 90)
wall_2_n_v = pygame.transform.rotate(wall_2_n, 90)

# --- SPRITES DA BARREIRA ---
barrier_img = pygame.image.load(f'{CAMINHO_BASE}/terrain/barrierNull.png').convert_alpha()

# --- SPRITE DE DEATH BARRIER ---
death_barrier_img = pygame.image.load(f'{CAMINHO_BASE}/terrain/death_barrierNull.png').convert_alpha()

# --- ANIMAÇÃO DE INIMIGOS ---
enemy_frames = [pygame.image.load(f'{CAMINHO_BASE}/enemy/enemy_{i}.png').convert_alpha() for i in range(1, 9)]
enemy_anim_speed = 6

# --- SPRITE OBJETIVO ---
goal_imgs = [
    pygame.image.load(f'{CAMINHO_BASE}/general/goal_1.png').convert_alpha(),
    pygame.image.load(f'{CAMINHO_BASE}/general/goal_2.png').convert_alpha()
]

# --- TELA DE MORTE ---
death_overlay_img = pygame.image.load(f'{CAMINHO_BASE}/general/death_screen.png').convert_alpha()

# --- LEVEL DATA ---

levels_data = {
    1: {
        'ground_offset': 60,
        'platform_pairs': [
            { # AZUIS
                'h': [
                    { #1
                    'rect': wall_1.get_rect(topleft=(1000, ALTURA - 260)),
                    'active_img': wall_1,
                    'inactive_img': wall_1_n
                },
                    { #4
                    'rect': wall_1.get_rect(topleft=(360, ALTURA - 320)),
                    'active_img': wall_1,
                    'inactive_img': wall_1_n
                },
                    { #10
                    'rect': wall_1.get_rect(topleft=(725, ALTURA - 680)),
                    'active_img': wall_1,
                    'inactive_img': wall_1_n
                },
                    { #12
                    'rect': wall_1.get_rect(topleft=(1070, ALTURA - 680)),
                    'active_img': wall_1,
                    'inactive_img': wall_1_n
                }
            ],
                'v': [
                    { #5
                    'rect': wall_1_v.get_rect(topleft=(280, ALTURA - 520)),
                    'active_img': wall_1_v,
                    'inactive_img': wall_1_n_v
                },
                    { #11
                    'rect': wall_1_v.get_rect(topleft=(990, ALTURA - 890)),
                    'active_img': wall_1_v,
                    'inactive_img': wall_1_n_v
                }
                ]
            },
            { # LARANJAS
                'h': [
                    { #2
                    'rect': wall_2.get_rect(topleft=(700, ALTURA - 300)),
                    'active_img': wall_2,
                    'inactive_img': wall_2_n
                },
                    { #6
                    'rect': wall_2.get_rect(topleft=(25, ALTURA - 350)),
                    'active_img': wall_2,
                    'inactive_img': wall_2_n
                },
                    { #7
                    'rect': wall_2.get_rect(topleft=(25, ALTURA - 520)),
                    'active_img': wall_2,
                    'inactive_img': wall_2_n
                },
                    { #8
                    'rect': wall_2.get_rect(topleft=(25, ALTURA - 680)),
                    'active_img': wall_2,
                    'inactive_img': wall_2_n
                },
                    { #9
                    'rect': wall_2.get_rect(topleft=(325, ALTURA - 700)),
                    'active_img': wall_2,
                    'inactive_img': wall_2_n
                }
                ],
                'v': [
                    { #3
                    'rect': wall_2_v.get_rect(topleft=(625, ALTURA - 550)),
                    'active_img': wall_2_v,
                    'inactive_img': wall_2_n_v
                }
                ]
            }
        ],
        'barriers': [
            pygame.Rect(1330, ALTURA - 175, 250, 75), # Low block
            pygame.Rect(1330, ALTURA - 715, 250, 75), # High block
            pygame.Rect(1500, ALTURA - 745, 250, 10) # High block 2
        ],
        'enemies_start_pos': [
            (25, ALTURA - 450, 3, False, 1),
            (1500, ALTURA - 850, 3, False, 1),
            (1250, ALTURA - 600, 2, True, 1)
        ],
        'goal_rect': pygame.Rect(1525, ALTURA - 820, 50, 50),
        'background_img_path': f'{CAMINHO_BASE}/general/background_1.png'
    },
    2: {
        'ground_offset': 0,
        'platform_pairs': [
            { # AZUIS
                'h': [
                    { #1
                    'rect': wall_1.get_rect(topleft=(250, ALTURA - 159)),
                    'active_img': wall_1,
                    'inactive_img': wall_1_n
                },
                    { #6
                    'rect': wall_1.get_rect(topleft=(640, ALTURA - 350)),
                    'active_img': wall_1,
                    'inactive_img': wall_1_n
                },
                    { #11
                    'rect': wall_1.get_rect(topleft=(1340, ALTURA - 160)),
                    'active_img': wall_1,
                    'inactive_img': wall_1_n
                },
                    { #13
                    'rect': wall_1.get_rect(topleft=(1340, ALTURA - 360)),
                    'active_img': wall_1,
                    'inactive_img': wall_1_n
                },
                    { #14
                    'rect': wall_1.get_rect(topleft=(1000, ALTURA - 500)),
                    'active_img': wall_1,
                    'inactive_img': wall_1_n
                }
            ],
                'v': [
                    { #2
                    'rect': wall_1_v.get_rect(topleft=(245, ALTURA - 340)),
                    'active_img': wall_1_v,
                    'inactive_img': wall_1_n_v
                },
                    { #4
                    'rect': wall_1_v.get_rect(topleft=(440, ALTURA - 645)),
                    'active_img': wall_1_v,
                    'inactive_img': wall_1_n_v
                },
                    { #15
                    'rect': wall_1_v.get_rect(topleft=(1200, ALTURA - 645)),
                    'active_img': wall_1_v,
                    'inactive_img': wall_1_n_v
                }
                ]
            },
            { # LARANJAS
                'h': [
                    { #3
                    'rect': wall_2.get_rect(topleft=(135, ALTURA - 585)),
                    'active_img': wall_2,
                    'inactive_img': wall_2_n
                },
                    { #5
                    'rect': wall_2.get_rect(topleft=(640, ALTURA - 700)),
                    'active_img': wall_2,
                    'inactive_img': wall_2_n
                },
                    { #7
                    'rect': wall_2.get_rect(topleft=(640, ALTURA - 30)),
                    'active_img': wall_2,
                    'inactive_img': wall_2_n
                },
                    { #9
                    'rect': wall_2.get_rect(topleft=(840, ALTURA - 30)),
                    'active_img': wall_2,
                    'inactive_img': wall_2_n
                },
                    { #10
                    'rect': wall_2.get_rect(topleft=(1040, ALTURA - 30)),
                    'active_img': wall_2,
                    'inactive_img': wall_2_n
                },
                    { #12
                    'rect': wall_2.get_rect(topleft=(1000, ALTURA - 300)),
                    'active_img': wall_2,
                    'inactive_img': wall_2_n
                }
                ],
                'v': [
                    { #8
                    'rect': wall_2_v.get_rect(topleft=(900, ALTURA - 230)),
                    'active_img': wall_2_v,
                    'inactive_img': wall_2_n_v
                }
                ]
            }
        ],
        'barriers': [
            pygame.Rect(0, ALTURA - 50, 230, 75), # Entrance
            pygame.Rect(460, ALTURA - 445, 155, 600), # Estalagmite
            pygame.Rect(537, ALTURA - 685, 57, 600), # Estalagmite2
            pygame.Rect(870, ALTURA - 900, 40, 650), # Estalactite
            pygame.Rect(875, ALTURA - 900, 60, 540), # Estalactite2
            pygame.Rect(930, ALTURA - 900, 80, 315), # Estalactite3
            pygame.Rect(1367, ALTURA - 665, 430, 235) # Exit
        ],
        'death_barriers': [
            pygame.Rect(0, ALTURA - 1, 1900, 1)
        ],
        'goal_rect': pygame.Rect(1525, ALTURA - 740, 50, 50),
        'enemies_start_pos': [
            (0, ALTURA - 830, 4, False, 1),
            (350, ALTURA - 830, 4, True, 1),
            (715, ALTURA - 100, 4, True, 1),
            (1270, ALTURA - 880, 4, True, 1)
        ],
        'background_img_path': f'{CAMINHO_BASE}/general/background_2.png'
    },
    3: {
        'ground_offset': 60,
        'platform_pairs': [
            { # AZUIS
                'h': [
                    { # 1
                    'rect': wall_1.get_rect(topleft=(1350, ALTURA - 350)),
                    'active_img': wall_1,
                    'inactive_img': wall_1_n
                },
                    { # 2
                    'rect': wall_1.get_rect(topleft=(50, ALTURA - 530)),
                    'active_img': wall_1,
                    'inactive_img': wall_1_n
                }
            ],
                'v': [

                ]
            },
            { # LARANJAS
                'h': [
                    { #3
                    'rect': wall_2.get_rect(topleft=(50, ALTURA - 700)),
                    'active_img': wall_2,
                    'inactive_img': wall_2_n
                }

                ],
                'v': [

                ]
            }
        ],
        'barriers': [
            pygame.Rect(1410, ALTURA - 200, 230, 260), # right
            pygame.Rect(0, ALTURA - 400, 1300, 120), # second level
            pygame.Rect(305, ALTURA - 720, 1400, 120), # third level
            pygame.Rect(1410, ALTURA - 790, 155, 50), # stair 1
            pygame.Rect(1520, ALTURA - 1100, 155, 300) # stair 2
        ],
        'death_barriers': [
        ],
        'goal_rect': pygame.Rect(1440, ALTURA - 865, 50, 50),
        'enemies_start_pos': [
            # first
            (100, ALTURA - 111, 3.1, True, 1),
            (160, ALTURA - 141, 3.1, True, 1),
            (220, ALTURA - 171, 3.1, True, 1),
            (280, ALTURA - 201, 3.1, True, 1),
            (340, ALTURA - 231, 3.1, True, 1),
            (400, ALTURA - 261, 3.1, True, 1),
            (460, ALTURA - 291, 3.1, True, -1),
            (520, ALTURA - 261, 3.1, True, -1),
            (580, ALTURA - 231, 3.1, True, -1),
            (640, ALTURA - 201, 3.1, True, -1),
            (700, ALTURA - 171, 3.1, True, -1),
            (760, ALTURA - 141, 3.1, True, -1),
            (820, ALTURA - 111, 3.1, True, -1),
            (880, ALTURA - 141, 3.1, True, 1),
            (940, ALTURA - 171, 3.1, True, 1),
            (1000, ALTURA - 201, 3.1, True, 1),
            (1060, ALTURA - 231, 3.1, True, 1),
            (1120, ALTURA - 261, 3.1, True, 1),
            (1180, ALTURA - 291, 3.1, True, 1),
            (1240, ALTURA - 261, 3.1, True, -1),
            # second
            (100, ALTURA - 480, 15, False, 1),
            (1540, ALTURA - 580, 15, False, 1),
            (1120, ALTURA - 580, 3, True, 1),
            (500, ALTURA - 580, 3, True, -1),
        ],
        'background_img_path': f'{CAMINHO_BASE}/general/background_3.png'
    },
    4: {
        'ground_offset': 2000,
        'platform_pairs': [
            { # AZUIS
                'h': [

            ],
                'v': [

                ]
            },
            { # LARANJAS
                'h': [

                ],
                'v': [

                ]
            }
        ],
        'barriers': [

        ],
        'death_barriers': [
        ],
        'goal_rect': pygame.Rect(2000, ALTURA - 865, 50, 50),
        'enemies_start_pos': [

        ],
        'background_img_path': f'{CAMINHO_BASE}/general/background_4.png'
    }
}


# --- CLASSE ENEMY ---
class Enemy:
    def __init__(self, x, y, speed, vertical=False, init_direction=1):
        self.frames = enemy_frames
        self.frame_counter = 0
        self.rect = self.frames[0].get_rect(topleft=(x, y))
        self.speed = speed
        self.direction = init_direction
        self.prev_direction = self.direction
        self.vertical = vertical
        self.image = self.frames[0]

    def update(self):
        # 1) Armazena direção anterior
        self.prev_direction = self.direction

        # 2) Atualiza frame de animação
        self.frame_counter += 1
        idx = (self.frame_counter // enemy_anim_speed) % len(self.frames)
        self.image = self.frames[idx]

        # 3) Move vertical ou horizontal
        if self.vertical:
            self.rect.y += self.speed * self.direction
            if self.rect.top <= 0 or self.rect.bottom >= ground_level:
                self.direction *= -1
        else:
            self.rect.x += self.speed * self.direction
            if self.rect.left <= 0 or self.rect.right >= LARGURA:
                self.direction *= -1

        # 4) Colisão com plataformas ativas (inverte direção)
        active_platforms = platform_pairs[active_pair]
        for key in ['h', 'v']:
            for plat in active_platforms[key]:
                plat_rect = plat['rect']
                if self.rect.colliderect(plat_rect):
                    self.direction *= -1
                    break  # já inverteu, pode sair do loop interno

        # 5) Colisão com barreiras (reposiciona e inverte direção)
        for barrier in barriers:
            if self.rect.colliderect(barrier):
                # Reposiciona o inimigo para fora da barreira
                if not self.vertical:
                    if self.rect.centerx < barrier.centerx:
                        self.rect.right = barrier.left
                    else:
                        self.rect.left = barrier.right
                else:
                    if self.rect.centery < barrier.centery:
                        self.rect.bottom = barrier.top
                    else:
                        self.rect.top = barrier.bottom
                self.direction *= -1

        # 6) Se a direção mudou em relação ao início deste update(), toca som
        if self.direction != self.prev_direction:
            random.choice(enemy_bump_sounds).play()

    def draw(self, surface):
        surface.blit(self.image, self.rect)



# --- ESTADO DO PLAYER ---
player_rect = base_right.get_rect(topleft=(0, 0))
vel_y = 0
no_chao = True
walk_counter = 0
walk_speed = 5
jump_counter = 0
jump_speed = 4
fall_counter = 0
fall_speed = 6
crash_counter = 0
crash_speed = 5
crashing = False
facing_right = True
morto = False


# --- FUNÇÃO PARA RESETAR O ESTADO DO JOGADOR E DOS INIMIGOS ---
def reset_player():
    global player_rect, vel_y, no_chao, walk_counter, jump_counter
    global fall_counter, crash_counter, crashing, facing_right, morto, enemies
    global current_level

    if current_level == 2:
        player_rect.topleft = (0, ALTURA - 100)
    else:
        player_rect.topleft = (0, ALTURA - base_right.get_height())
    vel_y = 0
    no_chao = True
    walk_counter = jump_counter = fall_counter = crash_counter = 0
    crashing = False
    facing_right = True
    morto = False

    enemies = [
        Enemy(x, y, s, v, init_dir)
        for (x, y, s, v, init_dir) in enemies_start_pos
    ]


# --- CRIAÇÕES DOS LEVELS ---
def load_level(n):
    global platform_pairs, barriers, death_barriers, goal_rect
    global enemies_start_pos, enemies, background_img
    global ground_offset_atual

    data = levels_data[n]

    ground_offset_atual = data.get('ground_offset', 60)

    # Plataformas, barreiras e objetivo
    platform_pairs = data['platform_pairs']
    barriers = data['barriers']
    death_barriers = data.get('death_barriers', [])
    goal_rect = data['goal_rect']

    # Fundo
    background_img = pygame.image.load(data['background_img_path']).convert()

    # Inimigos
    enemies_start_pos = data['enemies_start_pos']
    enemies = [
        Enemy(x, y, s, v, init_dir)
        for (x, y, s, v, init_dir) in enemies_start_pos
    ]

# Vars temporárias para satisfazer o linter — serão sobrescritas por load_level()
platform_pairs = []  # lista de pares de plataformas
barriers = []  # lista de rects de barreiras
death_barriers = [] # lista de rects de death barreiras
goal_rect = pygame.Rect(0, 0, 0, 0)  # rect placeholder do goal
enemies_start_pos = []  # coords iniciais de inimigos
enemies = []  # lista de Enemy()
background_img = background_img  # já definido lá em cima, mas ok
active_pair = 0  # qual par de plataformas começa ativo
ground_offset_atual = 60
ground_level = ALTURA - ground_offset_atual


current_level = 1
load_level(current_level)
reset_player()

# --- LOOP PRINCIPAL ---
running = True
while running:
    clock.tick(60)
    prev_no_chao = no_chao
    played_fall_sound = False
    prev_morto = morto
    for e in pygame.event.get():
        if e.type == QUIT:
            running = False
        elif e.type == VIDEORESIZE:
            LARGURA, ALTURA = e.size
            screen = pygame.display.set_mode((LARGURA, ALTURA), RESIZABLE)
            death_overlay_surface = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
            death_overlay_surface.fill((255, 0, 0, 100))
            ground_level = ALTURA - ground_offset_atual
        elif e.type == KEYDOWN and e.key == K_SPACE:
            active_pair = 1 - active_pair  # alterna plataforma ativa
            new_platforms = platform_pairs[active_pair]

            # percorre cada plataforma horizontal e vertical da nova lista
            for plat in new_platforms['h'] + new_platforms['v']:
                plat_rect = plat['rect']
                for inimigo in enemies:
                    if inimigo.rect.colliderect(plat_rect):
                        # reposiciona o inimigo para fora da plataforma
                        if not inimigo.vertical:
                            if inimigo.rect.centerx < plat_rect.centerx:
                                inimigo.rect.right = plat_rect.left
                            else:
                                inimigo.rect.left = plat_rect.right
                        else:
                            if inimigo.rect.centery < plat_rect.centery:
                                inimigo.rect.bottom = plat_rect.top
                            else:
                                inimigo.rect.top = plat_rect.bottom
                        inimigo.direction *= -1

    teclas = pygame.key.get_pressed()

    if morto and teclas[K_r]:
        reset_player()

    moving = False

    if not morto:
        if teclas[K_LEFT]:
            player_rect.x -= VEL
            facing_right = False
            moving = True
        elif teclas[K_RIGHT]:
            player_rect.x += VEL
            facing_right = True
            moving = True

        if teclas[K_UP] and no_chao:
            vel_y = PULO
            no_chao = False
            jump_counter = fall_counter = 0
            crashing = False
            random.choice(jump_sounds).play()

    # --- LIMITES DA TELA ---
    player_rect.left = max(player_rect.left, 0)
    player_rect.right = min(player_rect.right, LARGURA)

    # antes de aplicar GRAVIDADE, salve a posição antiga
    prev_top = player_rect.top
    prev_bottom = player_rect.bottom

    # --- APLICAR GRAVIDADE ---
    vel_y += GRAVIDADE
    player_rect.y += vel_y

    # --- COLISÃO COM PLATAFORMAS HORIZONTAIS ---
    on_platform = False
    for plat in platform_pairs[active_pair]['h']:
        rect = plat['rect']
        if player_rect.colliderect(rect):
            # colisão de cima (caindo sobre a plataforma)
            if vel_y > 0 and prev_bottom <= rect.top:
                player_rect.bottom = rect.top
                vel_y = 0
                on_platform = True
                if not no_chao:
                    if not prev_no_chao and not played_fall_sound:
                        random.choice(fall_sounds).play()
                        played_fall_sound = True
                    no_chao = True
                    jump_counter = fall_counter = 0

            # colisão por baixo (batendo a cabeça)
            elif vel_y < 0 and prev_top >= rect.bottom:
                player_rect.top = rect.bottom
                vel_y = 0
            # colisões laterais
            elif player_rect.right > rect.left > player_rect.left:
                player_rect.right = rect.left
            elif player_rect.left < rect.right < player_rect.right:
                player_rect.left = rect.right

    # --- COLISÃO COM PLATAFORMAS VERTICAIS (incluindo topo como chão) ---
    for plat in platform_pairs[active_pair]['v']:
        rect = plat['rect']
        if player_rect.colliderect(rect):
            # colisão de cima (caindo sobre a face superior da parede)
            if vel_y > 0 and prev_bottom <= rect.top:
                player_rect.bottom = rect.top
                vel_y = 0
                on_platform = True
                if not no_chao:
                    if not prev_no_chao and not played_fall_sound:
                        random.choice(fall_sounds).play()
                        played_fall_sound = True
                    no_chao = True
                    jump_counter = fall_counter = 0
                continue  # já resolvemos esta plataforma

            # colisão por baixo (batendo a cabeça na face inferior)
            if vel_y < 0 and prev_top >= rect.bottom:
                player_rect.top = rect.bottom
                vel_y = 0
                continue

            # colisões laterais
            if player_rect.right > rect.left > player_rect.left:
                player_rect.right = rect.left
            elif player_rect.left < rect.right < player_rect.right:
                player_rect.left = rect.right

    # --- COLISÃO COM O CHÃO COM DESLOCAMENTO ---
    ground_level = ALTURA - ground_offset_atual  # nível real do chão
    if player_rect.bottom >= ground_level:  # collide bottom at ALTURA - offset
        player_rect.bottom = ground_level  # reposiciona k levando em conta o offset
        vel_y = 0
        if not no_chao:
            if not prev_no_chao and not played_fall_sound:
                random.choice(fall_sounds).play()
                played_fall_sound = True
            no_chao = True
            jump_counter = fall_counter = 0
    elif not on_platform:
        no_chao = False

    # Colisão com barreiras
    for barrier in barriers:
        if player_rect.colliderect(barrier):
            if vel_y > 0 and player_rect.bottom - vel_y <= barrier.top:
                player_rect.bottom = barrier.top
                vel_y = 0
                if not prev_no_chao and not played_fall_sound:
                    random.choice(fall_sounds).play()
                    played_fall_sound = True
                no_chao = True
                jump_counter = fall_counter = 0
            elif vel_y < 0 and player_rect.top - vel_y >= barrier.bottom:
                player_rect.top = barrier.bottom
                vel_y = 0
            elif player_rect.right > barrier.left > player_rect.left:
                player_rect.right = barrier.left
            elif player_rect.left < barrier.right < player_rect.right:
                player_rect.left = barrier.right

    # Colisão com o goal
    if player_rect.colliderect(goal_rect):
        level_pass.play()
        current_level += 1
        if current_level > MAX_LEVELS:
            print("Parabéns, você terminou todos os níveis!")
            running = False
        else:
            load_level(current_level)
            reset_player()

    # --- DETECÇÃO DE COLISÃO COM DEATH BARRIERS ---
    if not morto:
        for db in death_barriers:
            if player_rect.colliderect(db):
                morto = True
                break

    # --- DETECÇÃO DE COLISÃO COM INIMIGOS ---
    if not morto:
        for inimigo in enemies:
            if player_rect.colliderect(inimigo.rect):
                morto = True
                break

    for inimigo in enemies:
        inimigo.update()

    # --- ANIMAÇÃO DO PLAYER ---
    if morto:
        frame = player_death_img
    elif crashing:
        crash_counter += 1
        idx = min((crash_counter // crash_speed), len(crash_neutral) - 1)
        if moving and facing_right:
            frame = crash_right[idx]
        elif moving and not facing_right:
            frame = crash_left[idx]
        else:
            frame = crash_neutral[idx]
        if idx == len(crash_neutral) - 1:
            crashing = False
    elif not no_chao:
        if vel_y < 0:
            jump_counter += 1
            idx = min((jump_counter // jump_speed), len(jump_neutral) - 1)
            if moving and facing_right:
                frame = jump_right[idx]
            elif moving and not facing_right:
                frame = jump_left[idx]
            else:
                frame = jump_neutral[idx]
        else:
            fall_counter += 1
            idx = min((fall_counter // fall_speed), len(fall_neutral) - 1)
            if moving and facing_right:
                frame = fall_right[idx]
            elif moving and not facing_right:
                frame = fall_left[idx]
            else:
                frame = fall_neutral[idx]
    elif moving:
        walk_counter += 1
        idx = (walk_counter // walk_speed) % len(walk_right)
        frame = walk_right[idx] if facing_right else walk_left[idx]
    else:
        walk_counter = 0
        frame = base_right if facing_right else base_left

    # --- SOM DE MORTE ---
    if prev_morto == False and morto == True:
        player_death_sound.play()

    if current_level == 3:
        for s in enemy_bump_sounds:
            s.set_volume(0.1)
    else:
        for s in enemy_bump_sounds:
            s.set_volume(0.3)

    # --- DESENHO ---
    screen.blit(pygame.transform.scale(background_img, (LARGURA, ALTURA)), (0, 0))

    # --- Desenha barreiras ---
    for barrier in barriers:
        screen.blit(barrier_img, barrier)

    # --- Desenha death barriers (letais) ---
    for db in death_barriers:
        screen.blit(death_barrier_img, db)

    # --- cálculo do frame atual da animação do goal ---
    current_time = pygame.time.get_ticks()
    goal_idx = (current_time // GOAL_ANIM_INTERVAL) % 2
    current_goal_img = goal_imgs[goal_idx]

    # Desenha o objetivo do nível atual
    screen.blit(current_goal_img, goal_rect)

    # Desenha todas as plataformas com estado ativo/inativo
    for i, pair in enumerate(platform_pairs):
        # plataformas horizontais
        for plat in pair['h']:
            img = plat['active_img'] if i == active_pair else plat['inactive_img']
            screen.blit(img, plat['rect'])
        # plataformas verticais
        for plat in pair['v']:
            img = plat['active_img'] if i == active_pair else plat['inactive_img']
            screen.blit(img, plat['rect'])

    screen.blit(frame, player_rect)

    for inimigo in enemies:
        inimigo.draw(screen)

    if morto:
        screen.blit(death_overlay_surface, (0, 0))
        img_rect = death_overlay_img.get_rect(center=(LARGURA // 2, ALTURA // 2))
        screen.blit(death_overlay_img, img_rect)

    pygame.display.update()

pygame.quit()
