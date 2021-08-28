"""
Nathaniel Gonzalez, neg2mhs
Nam Pham, nnp5unm

Overview: The game functions similar to Contra.

REQUIREMENTS:

User Input
Players move with ==> P1: directional keys P2: WASD. P1 shoot with comma, and P2 shoot with space

Graphics/Images
There are several graphics in the game.

Start Screen
our start screen has our names and IDs, and basic game instructions

Small Enough Window
camera window is gamebox.Camera(800,600)

OPTIONAL REQUIREMENTS:

Animation
Our Player models are animated to run.

Enemies
There are moving enemies (aliens)

Scrolling Level
The camera is moving to the right

Timer
There is a time survived timer

Health Bar
There are three hearts as the health bar for each player.

Two players simultaneously
This is a feature of the game


"""
import pygame
import gamebox
import random

camera = gamebox.Camera(800, 600)

p1_score = 0
p2_score = 0
ticks = 0
player_speed = 10
game_on = False

floor = gamebox.from_color(400,600, "slategray", 2000, 200)

number_of_frames = 3
sheet = gamebox.load_sprite_sheet("bluerun2.png", 5, number_of_frames)
sheet2 = gamebox.load_sprite_sheet('redrun3.png', 5, number_of_frames)

frame = 0
counter = 0
enemyCounter = 0

cam_middlex, cam_middley = camera.width // 2 - 1, camera.height // 2 - 1
background = gamebox.from_image(cam_middlex, cam_middley, 'spacebg.jpg')

p1 = gamebox.from_image(150, 530, sheet2[frame])  # gamebox image first pic in sprite sheet
p1.scale_by(1.2)

p2 = gamebox.from_image(150, 530, sheet[frame])  # gamebox image first pic in sprite sheet
p2.scale_by(1.2)

bullet = gamebox.from_image(0, 500,'contrabullet.png')
bullet.scale_by(0.08)

bullet2 = gamebox.from_image(0, 500,'contrabullet.png')
bullet2.scale_by(0.08)

enemyList = []

craterList = []

p1health = [
    gamebox.from_image(camera.right-270, camera.top + 50,
                       "heart.png"),
    gamebox.from_image(camera.right-240, camera.top + 50,
                       "heart.png"),
    gamebox.from_image(camera.right-210, camera.top + 50,
                       "heart.png"),
]
p1copy = p1health.copy()

for heart in p1health:
    heart.scale_by(0.03)

p2health = [
    gamebox.from_image(camera.left + 270, camera.top + 50,
                           "heart.png"),
    gamebox.from_image(camera.left + 240, camera.top + 50,
                           "heart.png"),
    gamebox.from_image(camera.left + 210, camera.top + 50,
                           "heart.png"),
]

p2copy = p2health.copy()

for heart in p2health:
    heart.scale_by(0.03)

def tick(keys):

    global game_on, p1_score, p2_score, ticks, frame, counter, enemyCounter, enemyList, p1health, p2health, craterList

    if not game_on:
        camera.clear('black')
        camera.draw(gamebox.from_text(camera.x, camera.top + 170, "Poor Man's Contra", 70, "Yellow",
                                      bold=True))
        camera.draw(gamebox.from_text(camera.right - 220, camera.top + 300, 'P1 Moves with directional Keys', 40, "Red",
                                      bold=False))
        camera.draw(gamebox.from_text(camera.right - 200, camera.top + 330,'P1 Shoots with comma key'
                                      , 40, "Red", bold=False))
        camera.draw(gamebox.from_text(camera.left + 200, camera.top + 300, 'P2 Moves with WASD', 40, "Blue",
                                      bold=False))
        camera.draw(gamebox.from_text(camera.left + 200, camera.top + 330, 'P2 Shoots with space key'
                                      , 40, "Blue", bold=False))
        camera.draw(gamebox.from_text(camera.left + 220, camera.bottom - 100, 'Nathaniel Gonzalez, neg2mhs', 40, "white",
                                      bold=False))
        camera.draw(
            gamebox.from_text(camera.left + 220, camera.bottom - 70, 'Nam Pham, nnp5unm', 40, "white",
                              bold=False))
        camera.draw(
            gamebox.from_text(camera.right - 400, camera.bottom - 200, '*Note: Shooting too fast causes the range to '
                                                                      'decrease.', 40, "orange",bold=False))
        camera.draw(
            gamebox.from_text(camera.left + 580, camera.bottom - 100, 'Press "N" to play!', 40, "purple",
                              bold=True))
    if pygame.K_n in keys:
        game_on = True
    if game_on:
        floor.move(3, 0)

        if pygame.K_RIGHT in keys:
            p1.move(player_speed,0)  # move character right

            if frame == number_of_frames:
                frame = 0
            if counter % 5 == 0:  # control dancer speed by changing
                p1.image = sheet2[frame]
            frame += 1
            counter += 1
        if pygame.K_COMMA in keys: # shooting
            bullet.speedy = 0
            bullet.speedx = player_speed * 10
            bullet.center = [p1.x + 3, p1.y - 4]
        if pygame.K_LEFT in keys:
            p1.move(-player_speed,0)  # move character left

            if frame == number_of_frames:
                frame = 0
            if counter % 5 == 0:  # control dancer speed by changing
                p1.image = sheet2[frame]
            frame += 1
            counter += 1
        if p1.bottom_touches(floor):
            if pygame.K_UP in keys:
                p1.move(0, -player_speed)# move character up
                p1.yspeed = -10
        if pygame.K_d in keys:
            p2.move(player_speed, 0)  # move character right

            if frame == number_of_frames:
                frame = 0
            if counter % 5 == 0:  # control dancer speed by changing
                p2.image = sheet[frame]
            frame += 1
            counter += 1
        if pygame.K_SPACE in keys: # shooting
            bullet2.speedy = 0
            bullet2.speedx = player_speed * 10
            bullet2.center = [p2.x + 3, p2.y - 4]
        if pygame.K_a in keys:
            p2.move(-player_speed,0)  # move character left

            if frame == number_of_frames:
                frame = 0
            if counter % 5 == 0:  # control dancer speed by changing
                p2.image = sheet[frame]
            frame += 1
            counter += 1
        if p2.bottom_touches(floor):
            if pygame.K_w in keys:
                p2.move(0, -player_speed)  # move character up
                p2.yspeed = -10
        if p1.bottom_touches(floor):
            p1.move_to_stop_overlapping(floor)
        if p2.bottom_touches(floor):
            p2.move_to_stop_overlapping(floor)
        p1.yspeed += 1
        p1.y += p1.yspeed
        p2.yspeed += 1
        p2.y += p2.yspeed

        enemyCounter += 1
        if enemyCounter % 10 == 0:  # controls the rate new walls are added
            # random x center, y window top,,random width, height
            new_enemy = gamebox.from_image(camera.right+150, random.randint(floor.top-70, floor.top-20),
                                          'alien.png')
            new_enemy.scale_by(0.15)
            enemyList.append(new_enemy)  # enemy list continues to grow

        if enemyCounter % 100 == 0:  # controls the rate new walls are added
            # random x center, y window top,,random width, height
            new_crater = gamebox.from_image(camera.right+150, random.randint(floor.top+20, floor.top+100),
                                          'rock.png')
            new_crater.scale_by(0.1)
            craterList.append(new_crater)

        for enemy in enemyList:  # collision detection of enemy
            if bullet.touches(enemy) or bullet2.touches(enemy):
                enemyList.remove(enemy)
            if p1.touches(enemy):
                if p1health:
                    p1health.pop()
                    enemyList.remove(enemy)
            if p2.touches(enemy):
                if p2health:
                    p2health.pop()
                    enemyList.remove(enemy)

        # Bound Collision (stop at bounds)
        if p1.x >= camera.right:
            p1.center = [camera.right-3, p1.y]
        if p1.x <= camera.left:
            p1.center = [camera.left+3, p1.y]
        if p2.x >= camera.right:
            p2.center = [camera.right-3, p2.y]
        if p2.x <= camera.left:
            p2.center = [camera.left+3, p2.y]

        camera.move(3,0)
        background.move(3,0)

        # Scores
        ticks += 1
        p1_score = str(int((ticks / ticks_per_second))).zfill(3)
        p2_score = str(int((ticks / ticks_per_second))).zfill(3)

        camera.clear("cyan")
        camera.draw(background)
        camera.draw(p1)
        camera.draw(p2)
        camera.draw(floor)
        camera.draw(gamebox.from_text(camera.right-175, camera.top + 20, 'P1 Health', 40, "Red", bold=False))
        camera.draw(gamebox.from_text(camera.left+175, camera.top+20, 'P2 Health', 40, "Blue", bold=False))
        camera.draw(gamebox.from_text(camera.left+400, camera.top + 20, 'Time Survived: ' + str(p2_score), 40, "Yellow",
                                      bold=False))
        camera.draw(gamebox.from_text(p1.x, p1.y - 30, 'Player 1', 20, "Red", bold=True))
        camera.draw(gamebox.from_text(p2.x, p2.y - 30, 'Player 2', 20, "Blue", bold=True))
        bullet.move_speed()
        bullet2.move_speed()
        camera.draw(bullet)
        camera.draw(bullet2)

        for heart1 in p1health:
            heart1.move(3,0),
            camera.draw(heart1)

        for heart2 in p2health:
            heart2.move(3,0)
            camera.draw(heart2)

        for enemy in enemyList:
            camera.draw(enemy)

        for crater in craterList:
            camera.draw(crater)

        if not p1health or not p2health:
            game_on = False
            p1health = p1copy.copy()
            p2health = p2copy.copy()
            p1_score = 0
            p2_score = 0
            ticks = 0
            frame = 0
            counter = 0
            enemyCounter = 0
            camera.center = [400, 300]
            floor.center = [400, 600]
            p1.center = [150, 530]
            p2.center = [150, 530]
            background.center = [cam_middlex, cam_middley]
            p1health[0].center = [camera.right-270, camera.top + 50]
            p1health[1].center = [camera.right-240, camera.top + 50]
            p1health[2].center = [camera.right-210, camera.top + 50]
            p2health[0].center = [camera.left+270, camera.top + 50]
            p2health[1].center = [camera.left + 240, camera.top + 50]
            p2health[2].center = [camera.left + 210, camera.top + 50]
            enemyList = []
            craterList = []

    camera.display()


ticks_per_second = 30
gamebox.timer_loop(ticks_per_second, tick)