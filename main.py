

import pygame

from cell_master import CellMaster
from states import States

########################################################################################################################

screen_size = (1200, 1000)
screen = pygame.display.set_mode(screen_size)

rows = 100
columns = 100
cell_master = CellMaster(rows, columns)

########################################################################################################################


def main():

    running = True

    while running:

        simulation_state = States.AWAIT_INPUT

        render_screen()
        pygame.display.flip()

        e = pygame.event.wait()
        if e.type == pygame.KEYUP:
            key_name = pygame.key.name(e.key)
            if key_name == 'space':
                simulation_state = States.CONTINUE_TO_NEXT_STATE

        if simulation_state == States.CONTINUE_TO_NEXT_STATE:
            cell_master.next_state()

########################################################################################################################


def render_screen():
    for c in cell_master.cells:
        cell = cell_master.cells[c]
        cell.day_trigger()
        cell.update_sprite()
        screen.blit(cell.image, (cell.rect.left, cell.rect.top))


########################################################################################################################

if __name__ == "__main__":
    main()
