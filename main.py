import pygame
import pygame_gui

from cell_master import CellMaster
from states import States

# Initialize Pygame
pygame.init()
########################################################################################################################
# Init Vars
rows = 120
columns = 120
size = 8

disease = {
    'incubation duration': 2,
    'contagious duration': 3,
}
cell_master = CellMaster(rows, columns, size, disease, 0.1)

screen_size = (size * columns + 300, size * rows)
screen = pygame.display.set_mode(screen_size)

clock = pygame.time.Clock()

########################################################################################################################
# UI Elements
ui_manager = pygame_gui.UIManager(screen_size)

ui_element_rects = [pygame.Rect((size * columns, 0), (100, 100)),
                    pygame.Rect((size * columns + 100, 0), (100, 100)),
                    pygame.Rect((size * columns + 200, 0), (100, 100)),
                    pygame.Rect((size * columns, 100), (300, 50)),
                    pygame.Rect((size * columns, 150), (300, 50)),
                    pygame.Rect((size * columns, 200), (300, 50)),
                    pygame.Rect((size * columns, 250), (300, 50)),
                    pygame.Rect((size * columns, 300), (300, 50)),
                    pygame.Rect((size * columns, 350), (300, 50)),
                    pygame.Rect((size * columns, 400), (300, 200))
                    ]

next_state_button = pygame_gui.elements.UIButton(relative_rect=ui_element_rects[0],
                                                 text="Next State",
                                                 manager=ui_manager)
run_button = pygame_gui.elements.UIButton(relative_rect=ui_element_rects[1],
                                          text="Run",
                                          manager=ui_manager)
reset_button = pygame_gui.elements.UIButton(relative_rect=ui_element_rects[2],
                                            text="Reset",
                                            manager=ui_manager)

infection_slider_label = pygame_gui.elements.UILabel(relative_rect=ui_element_rects[3],
                                                     text="Initial Infection Rate: 0.1",
                                                     manager=ui_manager)

initial_infection_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=ui_element_rects[4],
                                                                  start_value=0.1,
                                                                  value_range=(0.0, 1.0),
                                                                  manager=ui_manager)

transmission_slider_label = pygame_gui.elements.UILabel(relative_rect=ui_element_rects[5],
                                                        text="Transmission Rate: 0.1",
                                                        manager=ui_manager)

transmission_rate_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=ui_element_rects[6],
                                                                  start_value=0.1,
                                                                  value_range=(0.0, 1.0),
                                                                  manager=ui_manager)

death_rate_label = pygame_gui.elements.UILabel(relative_rect=ui_element_rects[7],
                                               text="Death Rate: 0.1",
                                               manager=ui_manager)

death_rate_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=ui_element_rects[8],
                                                           start_value=0.1,
                                                           value_range=(0.0, 1.0),
                                                           manager=ui_manager)


########################################################################################################################


def main():
    running = True  # Keeps main running
    auto_run = False  # To run the simulation without repeated inputs from the user
    simulation_state = States.AWAIT_INPUT

    while running:

        time_delta = clock.tick(60) / 1000.0  # Needed for the UI library
        if auto_run:
            clock.tick(200)  # Ticks the clock so the simulation doesnt go arbitrarily fast
        else:
            simulation_state = States.AWAIT_INPUT  # Prompts input again

        state_text_display = pygame_gui.elements.UITextBox(relative_rect=ui_element_rects[9],
                                                           html_text=cell_master.create_state_text(),
                                                           manager=ui_manager)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.USEREVENT:
                if event.user_type == 'ui_button_pressed':

                    if event.ui_element == next_state_button:
                        simulation_state = States.CONTINUE_TO_NEXT_STATE

                    elif event.ui_element == run_button:
                        if auto_run:
                            auto_run = False
                            run_button.set_text("Run")
                        else:
                            auto_run = True
                            if simulation_state is not States.CONTINUE_TO_NEXT_STATE:
                                simulation_state = States.CONTINUE_TO_NEXT_STATE
                            run_button.set_text("Pause")

                    elif event.ui_element == reset_button:
                        cell_master.reset(rows, columns, size, disease, initial_infection_slider.get_current_value())

            infection_slider_label.set_text("Initial Infection Rate: " +
                                            str(initial_infection_slider.get_current_value())[0:5])

            transmission_slider_label.set_text("Transmission Rate: " +
                                               str(transmission_rate_slider.get_current_value())[0:5])

            death_rate_label.set_text("Death Rate: " +
                                      str(death_rate_slider.get_current_value())[0:5])

            ui_manager.process_events(event)

        ui_manager.update(time_delta)
        render_screen()
        ui_manager.draw_ui(screen)
        pygame.display.update()

        if simulation_state == States.CONTINUE_TO_NEXT_STATE:
            simulation_complete = cell_master.next_state(transmission_rate_slider.get_current_value(),
                                                         death_rate_slider.get_current_value())
            if simulation_complete and auto_run:
                auto_run = False
                run_button.set_text("Run")


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
