import pygame

import time

from Graph import *
from Calculator import *

def get_elapsed_time(func):
    timer = pygame.time.Clock()
    func()
    return timer.tick() / 10002

def main():
    sf = input("Enter a function of f: ")
    bet = get_binary_expresion_tree(sf)
    #print(evaluate_binary_expression_tree(bet, 5))

    f = lambda x: evaluate_binary_expression_tree(bet, x)

    pygame.init()

    window = pygame.display.set_mode((500, 500))

    pygame.display.set_caption("Graphing Calculator")

    canvas = Canvas(500, 500, (-10, 10), (-10, 10))

    fpsClock = pygame.time.Clock()

    running = True
    drag = False
    while running:
        dt = fpsClock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    canvas.zoom(0.95)
                elif event.button == 5:
                    canvas.zoom(1.05)
                if event.button == 1:
                    drag = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drag = False

        canvas.clear()
        graph(canvas, f, COLOR_GREEN)

        offset = pygame.mouse.get_rel()
        if drag:
            canvas.move_viewport(-offset[0], offset[1])

        img = pygame.image.frombuffer(bytearray(canvas.pixels), (canvas.width, canvas.height), "RGBA") 

        #clear window
        window.fill((0, 0, 0))

        #draw img
        window.blit(img, (0, 0))

        pygame.display.update()

    pygame.display.quit()
    pygame.quit()

if __name__ == "__main__":
    main()
