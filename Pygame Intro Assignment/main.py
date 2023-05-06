"""
-----------------------
-----------------------
pygame intro assignment
-----------------------
-----------------------
"""

import pygame
import os
import random
pygame.font.init()
pygame.mixer.init()

screen_width, screen_height = 900, 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Zombie Apocalypse")

#colours
light_blue = (204, 236, 255)
black = (0, 0, 0)
green = (17, 252, 0)
cobalt_blue = (0, 179, 255)
white = (255, 255, 255)
sky_blue = (73, 182, 205)

#get fonts
health_font = pygame.font.SysFont('roboto mono', 30)
win_font = pygame.font.SysFont('roboto mono', 40)
instructions_font = pygame.font.SysFont('roboto mono', 30)

#border 
border_thickness = 7
border = pygame.Rect(0, (screen_height // 2) - (border_thickness // 2), screen_width, border_thickness)

#game settings
fps = 60
velocity = 7

bullet_width, bullet_height = 3, 25
bullet_velocity = 15
max_bullets = 2

#get images
zombie_image = pygame.image.load(os.path.join('assets', 'images', 'zombie 1 (transparent bg).png'))
man_image = pygame.transform.rotate(pygame.image.load(os.path.join('assets', 'images', 'man 1 (transparent bg).png')), 180)
grass_img = pygame.image.load(os.path.join('assets', 'images', 'grass1.png'))
health_kit_img = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'images', 'health kit 2.png')), (90, 90))

zombie_shoot_img = pygame.image.load(os.path.join('assets', 'images', 'zombie 2 (transparent bg).png'))
man_shoot_img = pygame.transform.rotate(pygame.image.load(os.path.join('assets', 'images', 'man 2 (transparent bg).png')), 180)

intro_bg = pygame.image.load(os.path.join('assets', 'images', 'intro background.jpg'))
intro_zombie_img = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'images', 'zombie animation.png')), (150, 150))

#create userevents
zombie_hit = pygame.USEREVENT + 1
man_hit = pygame.USEREVENT + 2
health_kit_hit_by_zombie = pygame.USEREVENT + 3
health_kit_hit_by_man = pygame.USEREVENT + 4

#get widths and heights of images
character_width = zombie_image.get_width()
character_height = zombie_image.get_height()

health_kit_width = health_kit_img.get_width()
health_kit_height = health_kit_img.get_height()

#center characters
center_x = (screen_width / 2) - (character_width / 2)
center_y_top = (screen_height / 4) - (character_height / 2)
center_y_bottom = ((screen_height / 4) - (character_height / 2)) + (screen_height / 2)

#get sounds and modify volumes
shoot_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'pew sound.mp3'))
shoot_sound.set_volume(0.4)

man_win_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'win sound 1.mp3'))
zombie_win_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'win sound 2.mp3'))
bonus_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'game bonus sound.mp3'))

background_music = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'music.mp3'))
background_music.set_volume(0.7)

intro_background_music = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'intro music.mp3'))
intro_zombie_jump_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'jump sound.mp3'))



#draw intro scene
def draw_intro(bg1, bg2, bg3, intro_zombie):
    #draw background
    screen.fill(sky_blue)
    screen.blit(intro_bg, (bg1.x, bg1.y))
    screen.blit(intro_bg, (bg2.x, bg2.y))
    screen.blit(intro_bg, (bg3.x, bg3.y))

    #draw zombie
    screen.blit(intro_zombie_img, (screen_width / 2 - intro_zombie_img.get_width(), intro_zombie.y))
    
    if intro_zombie.y < 460:
        intro_zombie.y += 5
    
    #create instructions
    header = instructions_font.render("INSTRUCTIONS:", 1, black)
    zombie_instructions = instructions_font.render("Use ESDF to move the zombie. Press LEFT ALT to shoot.", 1, black)
    man_instructions = instructions_font.render("Use IJKL to move the man. Press RIGHT ALT to shoot.", 1, black)
    powerup_instructions = instructions_font.render("A power-up will spawn occasionally. Shoot it to use it.", 1, black)
    start_text = instructions_font.render("(press SPACE to continue)", 1, black)
    click_text = instructions_font.render("(CLICK to see something cool)", 1, black)
    
    
    #draw instructions
    screen.blit(header, (screen_width/2 - header.get_width()/2, screen_height/10))
    screen.blit(zombie_instructions, (screen_width/2 - zombie_instructions.get_width()/2, screen_height/10 * 2))
    screen.blit(man_instructions, (screen_width/2 - man_instructions.get_width()/2, screen_height/10 * 3))
    screen.blit(powerup_instructions, (screen_width/2 - powerup_instructions.get_width()/2, screen_height/10 * 4))
    screen.blit(click_text, (screen_width/2 - click_text.get_width()/2, screen_height/10 * 5))
    screen.blit(start_text, (screen_width/2 - start_text.get_width()/2, screen_height/16 * 9))
    
    pygame.display.update()
    

#animate intro scene
def animate_intro(bg1, bg2, bg3):
    if bg1.x > 0 - intro_bg.get_width():
        bg1.x -= 1
    else: 
        bg1.x = bg3.x + intro_bg.get_width() - 1
        
    if bg2.x > 0 - intro_bg.get_width():
        bg2.x -= 1
    else: 
        bg2.x = bg1.x + intro_bg.get_width() - 1
        
    if bg3.x > 0 - intro_bg.get_width():
        bg3.x -= 1
    else: 
        bg3.x = bg2.x + intro_bg.get_width() - 1
        
    

def draw_window(zombie, man, zombie_bullets, man_bullets, zombie_health, man_health, health_kits, health_kit_x, health_kit_y):
    screen.fill(light_blue)
    #draw background and border
    screen.blit(grass_img, (0, 0))
    pygame.draw.rect(screen, black, border)

    #draw health text
    zombie_health_text = health_font.render("health: " + str(zombie_health), 1, black)
    man_health_text = health_font.render("health: " + str(man_health), 1, black)
    screen.blit(zombie_health_text, (10, 10))
    screen.blit(man_health_text, (10, screen_height/2 + border_thickness + 10))
    
    #draw health kit
    for health_kit in health_kits:
        screen.blit(health_kit_img, (health_kit_x, health_kit_y)) 

    #draw characters
    screen.blit(zombie_image, (zombie.x, zombie.y)) 
    screen.blit(man_image, (man.x, man.y))

    #draw bullets
    for bullet in zombie_bullets:
        pygame.draw.rect(screen, green, bullet) #zombie

    for bullet in man_bullets:
        pygame.draw.rect(screen, cobalt_blue, bullet) #man
        
    pygame.display.update()


def handle_zombie_movement(keys_pressed, zombie):
    if keys_pressed[pygame.K_e] and zombie.y - velocity >= 0: #up
        zombie.y -= velocity
    if keys_pressed[pygame.K_d] and zombie.y + velocity < border.y - character_height: #down
        zombie.y += velocity
    if keys_pressed[pygame.K_s] and zombie.x - velocity >= 0: #left
        zombie.x -= velocity
    if keys_pressed[pygame.K_f] and zombie.x + velocity < screen_width - character_width: #right
        zombie.x += velocity


def handle_man_movement(keys_pressed, man):
    if keys_pressed[pygame.K_i] and man.y - velocity > border.y + border_thickness: #up
        man.y -= velocity
    if keys_pressed[pygame.K_k] and man.y + velocity < screen_height - character_height: #down
        man.y += velocity
    if keys_pressed[pygame.K_j] and man.x - velocity >= 0: #left
        man.x -= velocity
    if keys_pressed[pygame.K_l] and man.x + velocity < screen_width - character_width: #right
        man.x += velocity


def health_kit_collision(zombie_bullets, man_bullets, health_kit_x, health_kit_y, health_kits):
    for health_kit in health_kits:
        #if zombie shoots health kit
        for bullet in zombie_bullets:
            if bullet.y < health_kit_y + health_kit_height and bullet.y > health_kit_y and bullet.x < health_kit_x + health_kit_width and bullet.x > health_kit_x:
                pygame.event.post(pygame.event.Event(health_kit_hit_by_zombie))
                zombie_bullets.remove(bullet)
                
        #if man shoots health kit
        for bullet in man_bullets:
            if bullet.y < health_kit_y + health_kit_height and bullet.y > health_kit_y and bullet.x < health_kit_x + health_kit_width and bullet.x > health_kit_x:
                pygame.event.post(pygame.event.Event(health_kit_hit_by_man))
                man_bullets.remove(bullet)


def handle_bullets(zombie_bullets, man_bullets, zombie, man):
    for bullet in zombie_bullets:
        bullet.y += bullet_velocity
        #if zombie shoots man
        if man.colliderect(bullet):
            pygame.event.post(pygame.event.Event(man_hit))
            zombie_bullets.remove(bullet)
        if bullet.y > screen_height:
            try:
                zombie_bullets.remove(bullet)
            except:
                print("no bullets in list")

    for bullet in man_bullets:
        bullet.y -= bullet_velocity
        #if man shoots zombie
        if zombie.colliderect(bullet):
            pygame.event.post(pygame.event.Event(zombie_hit))
            man_bullets.remove(bullet)
        if bullet.y < 0:
            try:
                man_bullets.remove(bullet)
            except:
                print("no bullets in list")


#draws text for winner
def draw_winner(text):
    draw_text = win_font.render(text, 1, white)
    screen.blit(draw_text, (screen_width/2 - draw_text.get_width()/2, screen_height/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)


def main():
    #creates characters
    zombie = pygame.Rect(center_x, center_y_top, character_width, character_height)
    man = pygame.Rect(center_x, center_y_bottom, character_width, character_height)

    zombie_bullets = []
    man_bullets = []
    health_kits = []

    zombie_health = 20
    man_health = 20

    current_ticks = 1
    clock = pygame.time.Clock()
    
    #loops music
    background_music.play(-1)
    
    run = True
    while run:
        clock.tick(fps)
                
        #creates health kit power-up every 500 ticks
        if len(health_kits) < 1:
            health_kit_x = random.randint(0, screen_width - health_kit_img.get_width())
            health_kit_y = random.randint(60, screen_height - health_kit_img.get_height() - 60)
        if len(health_kits) < 1:
            if current_ticks % 500 == 0:
                health_kits.append("health kit")
                bonus_sound.play()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            #allows ships to shoot bullets
            if event.type == pygame.KEYDOWN:
                #zombie
                if event.key == pygame.K_LALT and len(zombie_bullets) < max_bullets:
                    bullet = pygame.Rect((zombie.x + zombie.width // 2) + 17, zombie.y + zombie.height, bullet_width, bullet_height)
                    screen.blit(zombie_shoot_img, (zombie.x, zombie.y))
                    pygame.display.update()
                    zombie_bullets.append(bullet)
                    shoot_sound.play()
                    delay = 1500000
                    while delay != 0:
                        delay -= 1

                #man
                if event.key == pygame.K_RALT and len(man_bullets) < max_bullets:
                    bullet = pygame.Rect((man.x + man.width // 2) + 17, man.y - man.height, bullet_width, bullet_height)
                    screen.blit(man_shoot_img, (man.x, man.y))
                    pygame.display.update()
                    man_bullets.append(bullet)
                    shoot_sound.play()
                    delay = 1500000
                    while delay != 0:
                        delay -= 1

            #zombie loses health if shot
            if event.type == zombie_hit:
                zombie_health -= 1

            #man loses health if shot
            if event.type == man_hit:
                man_health -= 1
            
            #zombie gains health if shoots health kit
            if event.type == health_kit_hit_by_zombie:
                zombie_health += 5
                try:
                    health_kits.remove(health_kits[0])
                except:
                    print("no health kits")
            
            #man gains health if shoots health kit
            if event.type == health_kit_hit_by_man:
                man_health += 5
                try:
                    health_kits.remove(health_kits[0])
                except:
                    print("no health kits")
    
        winner_text = ""
        #display text if zombie wins
        if zombie_health <= 0:
            background_music.stop()
            pygame.time.delay(500)
            winner_text = "The man took down the zombie~!"
            man_win_sound.play()

        #display text if man wins
        if man_health <= 0:
            background_music.stop()
            pygame.time.delay(500)
            winner_text = "The zombie ate the man~!"
            zombie_win_sound.play()

        if winner_text != "":
            draw_winner(winner_text)
            run = False
            break

        keys_pressed = pygame.key.get_pressed()
        handle_zombie_movement(keys_pressed, zombie)
        handle_man_movement(keys_pressed, man)
        
        handle_bullets(zombie_bullets, man_bullets, zombie, man)
        health_kit_collision(zombie_bullets, man_bullets, health_kit_x, health_kit_y, health_kits)
        draw_window(zombie, man, zombie_bullets, man_bullets, zombie_health, man_health, health_kits, health_kit_x, health_kit_y)
        
        current_ticks += 1


#background coordinates
bg_start_y = screen_height - intro_bg.get_height()
bg1_start_x = 0
bg2_start_x = intro_bg.get_width()
bg3_start_x = intro_bg.get_width() * 2

#create background rects
bg1 = pygame.Rect(bg1_start_x, bg_start_y, intro_bg.get_width(), intro_bg.get_height())
bg2 = pygame.Rect(bg2_start_x, bg_start_y, intro_bg.get_width(), intro_bg.get_height()) 
bg3 = pygame.Rect(bg3_start_x, bg_start_y, intro_bg.get_width(), intro_bg.get_height()) 

#create intro zombie rect
intro_zombie = pygame.Rect(screen_width / 2 - intro_zombie_img.get_width(), 460, intro_zombie_img.get_width(), intro_zombie_img.get_height())

playing = True
while playing:
    intro_background_music.play(-1)
    #run intro
    intro = True
    while intro:
        animate_intro(bg1, bg2, bg3)
        draw_intro(bg1, bg2, bg3, intro_zombie)
        delay = 100000
        while delay > 0:
            delay -= 1
        for event in pygame.event.get():
            #quit pygame
            if event.type == pygame.QUIT:
                intro = False
                pygame.quit()
            #exit intro if SPACE is pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro_background_music.stop()
                    intro = False
            if event.type == pygame.MOUSEBUTTONUP:
                #zombie jumps
                intro_zombie_jump_sound.play()
                jump_height = 80
                intro_zombie.y -= jump_height
                      

    if __name__ == "__main__":
        main()
