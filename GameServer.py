import threading
import pygame
import socket
import sys
import random
from math import sqrt

name = "test"
posx = 300
posy = 500
ballx = 0
bally = 40

nom_direction = 0

def GameThread():
    pygame.init()
    background = (204, 230, 255)
    shapeColor = (0, 51, 204)
    shapeColorOver = (255, 0, 204)
    shapeColorColor = (0, 204, 0)

    
    fps = pygame.time.Clock()
    screen_size = screen_width, screen_height = 650, 650
    screen = pygame.display.set_mode(screen_size)
    # c1 = pygame.draw.circle(screen, (255, 0, 0), (10, 10), 25)
    # c2 = pygame.draw.circle(screen, (255, 0, 0), (10, 10), 25)
    # c3 = pygame.draw.circle(screen, (255, 0, 0), (10, 10), 25)
    pygame.display.set_caption('Welcome to CCN games')

    text_font = pygame.font.SysFont(None, 30)
    background_img = pygame.image.load('background.jpg')
    background_img = pygame.transform.scale(background_img, (screen_width, screen_height))

    nombucket_img = pygame.image.load('nom.png')
    nombucket_img = pygame.transform.scale(nombucket_img, (100, 100))
    
    candy_img = pygame.image.load('candy.png')
    candy_img = pygame.transform.scale(candy_img, (100, 100))

    colorc1 = (shapeColor)
    colorc2 = (shapeColorOver)
    colorc3 = (shapeColorColor)
    global posx 
    global posy 
    global ballx
    global bally
    global nom_direction
    ballx = random.randint(0, screen_width)

    score = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(background_img, (0,0))
        
        # draw candy
        screen.blit(candy_img, (ballx, bally))
        
        bally += 5 + sqrt(score)

        if bally > screen_height:
            bally = 0
            ballx = random.randint(0, screen_width)

        if nom_direction > 0:
            posx += 5 + sqrt(score)
        elif nom_direction < 0:
            posx -= 5 + sqrt(score)

        # current score
        score_board = text_font.render(f"Score: {score}", True, (0, 255, 0))
        screen.blit(score_board, (50, 50))

        # draw bucket
        screen.blit(nombucket_img, (posx, posy))

        # collision
        nom_rect = nombucket_img.get_rect(topleft=(posx, posy))
        nom_mask = pygame.mask.from_surface(nombucket_img)
        
        candy_rect = candy_img.get_rect(topleft=(ballx, bally))
        candy_mask = pygame.mask.from_surface(candy_img)

        if nom_mask.overlap(candy_mask, (nom_rect.left - candy_rect.left, nom_rect.top - candy_rect.top)):
            ballx = random.randint(0, screen_width)
            bally = 40
            score += 1

        pygame.display.update()
        fps.tick(60)

    pygame.quit()


def ServerThread():
    global posy
    global posx
    global nom_direction
    # get the hostname
    host = socket.gethostbyname(socket.gethostname())
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    host = s.getsockname()[0]
    s.close()
    print(host)
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together
    server_socket.settimeout(15)
    print("Server enabled...")
    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))    
    while True:        
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        
        print("from connected user: " + str(data))
        if(data == 'w'):
            nom_direction = 0
        if(data == 's'):
            nom_direction = 0
        if(data == 'a'):
            nom_direction = -1
        if(data == 'd'):
            nom_direction = 1
    conn.close()  # close the connection


t1 = threading.Thread(target=GameThread, args=[])
t2 = threading.Thread(target=ServerThread, args=[])
t1.start()
t2.start()