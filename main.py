from math import floor

import pygame
import pygame_gui

from source.cell_master import CellMaster
from source.states import States

# Initialize Pygame
pygame.init()
########################################################################################################################
# Init Vars
rows = 100
columns = 100
size = 10
default_disease = {
    'incubation duration': 2,
    'contagious duration': 3,
}
screen_size = (size * columns + 300, size * rows)
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()

########################################################################################################################
# UI Elements
ui_manager = pygame_gui.UIManager(screen_size)

ui_element_rects = [
                    pygame.Rect((size * columns, 0), (100, 100)),        # 0 Next State
                    pygame.Rect((size * columns + 100, 0), (100, 100)),  # 1 Run / Pause
                    pygame.Rect((size * columns + 200, 0), (100, 100)),  # 2 Reset

                    pygame.Rect((size * columns, 100), (300, 50)),       # 3 Transmission Rate Label
                    pygame.Rect((size * columns, 150), (300, 50)),       # 4 Transmission Rate Slider

                    pygame.Rect((size * columns, 200), (300, 50)),       # 5 Death Rate Label
                    pygame.Rect((size * columns, 250), (300, 50)),       # 6 Death Rate Slider

                    pygame.Rect((size * columns, 300), (300, 300)),      # 7 State Data

                    pygame.Rect((size * columns, 660), (300, 50)),       # 8 Initial Infection Rate Label
                    pygame.Rect((size * columns, 710), (300, 50)),       # 9 Initial Infection Rate Slider
                    pygame.Rect((size * columns, 760), (300, 50)),       # 10 Incubation Duration Rate Label
                    pygame.Rect((size * columns, 810), (300, 50)),       # 11 Incubation Duration Rate Slider
                    pygame.Rect((size * columns, 860), (300, 50)),       # 12 Contagious Duration Rate Label
                    pygame.Rect((size * columns, 910), (300, 50)),       # 13 Contagious Duration Rate Slider
                    ]

########################################################################################################################
# BUTTONS

next_state_button = pygame_gui.elements.UIButton(                      relative_rect=ui_element_rects[0],
                                                                       text="Next State",
                                                                       manager=ui_manager)
run_button = pygame_gui.elements.UIButton(                             relative_rect=ui_element_rects[1],
                                                                       text="Run",
                                                                       manager=ui_manager)
reset_button = pygame_gui.elements.UIButton(                           relative_rect=ui_element_rects[2],
                                                                       text="Reset",
                                                                       manager=ui_manager)
########################################################################################################################
# DYNAMIC DATA SLIDERS (SIM DOES NOT NEED TO BE RESET IN ORDER FOR CHANGES TO TAKE EFFECT)

transmission_slider_label = pygame_gui.elements.UILabel(               relative_rect=ui_element_rects[3],
                                                                       text="Transmission Rate: 0.1",
                                                                       manager=ui_manager)

transmission_rate_slider = pygame_gui.elements.UIHorizontalSlider(     relative_rect=ui_element_rects[4],
                                                                       start_value=0.1,
                                                                       value_range=(0.0, 1.0),
                                                                       manager=ui_manager)

death_rate_label = pygame_gui.elements.UILabel(                        relative_rect=ui_element_rects[5],
                                                                       text="Death Rate: 0.1",
                                                                       manager=ui_manager)

death_rate_slider = pygame_gui.elements.UIHorizontalSlider(            relative_rect=ui_element_rects[6],
                                                                       start_value=0.1,
                                                                       value_range=(0.0, 1.0),
                                                                       manager=ui_manager)
########################################################################################################################
# INIT DATA SLIDERS (MUST RESET SIM FOR CHANGES TO TAKE EFFECT)

initial_infection_slider_label = pygame_gui.elements.UILabel(          relative_rect=ui_element_rects[8],
                                                                       text="Initial Infection Rate: 0.1",
                                                                       manager=ui_manager)

initial_infection_slider = pygame_gui.elements.UIHorizontalSlider(     relative_rect=ui_element_rects[9],
                                                                       start_value=0.1,
                                                                       value_range=(0.0, 1.0),
                                                                       manager=ui_manager)

incubation_duration_label = pygame_gui.elements.UILabel(               relative_rect=ui_element_rects[10],
                                                                       text="Incubation Duration: 2",
                                                                       manager=ui_manager)

incubation_duration_slider = pygame_gui.elements.UIHorizontalSlider(   relative_rect=ui_element_rects[11],
                                                                       start_value=2,
                                                                       value_range=(0, 10),
                                                                       manager=ui_manager)

contagious_duration_label = pygame_gui.elements.UILabel(               relative_rect=ui_element_rects[12],
                                                                       text="Contagious Duration: 3",
                                                                       manager=ui_manager)

contagious_duration_slider = pygame_gui.elements.UIHorizontalSlider(   relative_rect=ui_element_rects[13],
                                                                       start_value=3,
                                                                       value_range=(0, 10),
                                                                       manager=ui_manager)

########################################################################################################################
# MAIN


def main():
    running = True  # Keeps main running
    auto_run = False  # To run the simulation without repeated inputs from the user
    simulation_state = States.AWAIT_INPUT
    cell_master = CellMaster(rows, columns, size, default_disease, 0.1)

    while running:

        if auto_run:
            time_delta = clock.tick(1000) / 1000.0  # Ticks the clock so the simulation doesnt go arbitrarily fast
        else:
            time_delta = clock.tick(60) / 1000.0
            simulation_state = States.AWAIT_INPUT  # Prompts input again

        pygame_gui.elements.UITextBox(relative_rect=ui_element_rects[7],        # Displays current state data
                                      html_text=cell_master.create_state_text(),
                                      manager=ui_manager)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.USEREVENT:
                if event.user_type == 'ui_button_pressed':
                    simulation_state, auto_run, cell_master = \
                        process_ui_event(event, simulation_state, auto_run, cell_master)

            update_labels()
            ui_manager.process_events(event)

        ui_manager.update(time_delta)
        render_screen(cell_master)
        pygame.display.update()

        if simulation_state == States.CONTINUE_TO_NEXT_STATE:

            simulation_complete = cell_master.next_state(transmission_rate_slider.get_current_value(),
                                                         death_rate_slider.get_current_value())
            if simulation_complete and auto_run:
                auto_run = False
                run_button.set_text("Run")


########################################################################################################################
# HELPER FUNCTIONS

def render_screen(cell_master):
    for c in cell_master.cell_dictionary:
        cell = cell_master.get_cell(c)
        cell.day_trigger()
        cell.update_color()
        pygame.draw.rect(screen, cell.color, pygame.Rect(cell.x, cell.y, cell.size, cell.size))

    ui_manager.get_sprite_group().draw(screen)


def process_ui_event(event, simulation_state, auto_run, cell_master):
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
        if auto_run:
            auto_run = False
            run_button.set_text("Run")
        disease = {
            'incubation duration': floor(incubation_duration_slider.get_current_value()),
            'contagious duration': floor(contagious_duration_slider.get_current_value()),
        }
        cell_master = CellMaster(rows, columns, size, disease, initial_infection_slider.get_current_value())

    return simulation_state, auto_run, cell_master


def update_labels():
    initial_infection_slider_label.set_text(    "Initial Infection Rate: " +
                                                 str(initial_infection_slider.get_current_value())[0:5])

    transmission_slider_label.set_text(         "Transmission Rate: " +
                                                 str(transmission_rate_slider.get_current_value())[0:5])

    death_rate_label.set_text(                  "Death Rate: " +
                                                 str(death_rate_slider.get_current_value())[0:5])

    incubation_duration_label.set_text(         "Incubation Duration: " +
                                                 str(floor(incubation_duration_slider.get_current_value())))

    contagious_duration_label.set_text(         "Contagious Duration: " +
                                                 str(floor(contagious_duration_slider.get_current_value())))

########################################################################################################################


if __name__ == "__main__":
    main()
