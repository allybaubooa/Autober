# from app import flask_app
import sys
import pygame
from app.autober import main_menu


if __name__ == '__main__':
    main_menu()
    # flask_app.run()
    pygame.quit()
    sys.exit()
