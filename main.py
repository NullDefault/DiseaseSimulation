

import pygame

from cell_master import CellMaster
from states import States

########################################################################################################################

rows = 100
columns = 200
size = 7
cell_master = CellMaster(rows, columns, size, 0.05)
screen_size = (size*columns, size*rows)
screen = pygame.display.set_mode(screen_size)

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
        cell.update_color()
        pygame.draw.rect(screen, cell.color, pygame.Rect(cell.x, cell.y, cell.size, cell.size))


########################################################################################################################

if __name__ == "__main__":
    main()
