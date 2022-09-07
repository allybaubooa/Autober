# from app import flask_app
import sys
import pygame
from app.autober import main_menu


if __name__ == '__main__':
    # thread= Thread(target=main_menu)
    # thread.start()
    main_menu()
    # Process(target=main_menu)
    pygame.quit()
    sys.exit()
