from random import randint

import pygame
from fysom import Fysom

infectedStates = ['day 1', 'day 2', 'day 3', 'day 4']

colors = {
    'healthy': pygame.color.Color(200, 200, 255),  # White
    'day 1': pygame.color.Color(255, 255, 170),  # Pale Yellow
    'day 2': pygame.color.Color(255, 255, 100),  # Yellow
    'day 3': pygame.color.Color(255, 102, 0),  # Orange
    'day 4': pygame.color.Color(255, 0, 0),  # Red
    'day 5': pygame.color.Color(128, 0, 0),  # Dark Red
    'dead': pygame.color.Color(0, 0, 0),  # Black
    'immune': pygame.color.Color(51, 204, 51)  # Green
}


class Cell:
    def __init__(self, location, size):
        self.state = Fysom({
            'initial': 'healthy',
            'events': [
                {'name': 'get infected', 'src': 'healthy', 'dst': 'day 1'},

                {'name': 'day pass', 'src': 'day 1', 'dst': 'day 2'},
                {'name': 'day pass', 'src': 'day 2', 'dst': 'day 3'},
                {'name': 'day pass', 'src': 'day 3', 'dst': 'day 4'},
                {'name': 'day pass', 'src': 'day 4', 'dst': 'day 5'},

                {'name': 'die', 'src': 'day 5', 'dst': 'dead'},
                {'name': 'recover', 'src': 'day 5', 'dst': 'immune'}
            ],
        })
        self.color = colors[self.state.current]
        self.next_trigger = None
        self.neighbors = []
        self.size = size
        self.x, self.y = location[0] * self.size, location[1] * self.size

    def day_trigger(self):
        if self.next_trigger is not None:
            self.state.trigger(self.next_trigger)
        self.next_trigger = None

    def infect_neighbors(self):
        for neighbor in self.neighbors:
            if neighbor.state.current is 'healthy':
                neighbor.proc_infection_chance()

    def proc_infection_chance(self):
        roll = randint(0, 9)
        if roll == 0:
            self.next_trigger = 'get infected'

    def proc_final_day(self):
        roll = randint(0, 9)
        if roll == 0:
            self.next_trigger = 'die'
        else:
            self.next_trigger = 'recover'

    def proc_day_pass(self):
        self.next_trigger = 'day pass'

    def set_neighbors(self, cell_dict):
        x = self.x // self.size
        y = self.y // self.size

        try:
            top_left = cell_dict[(x - 1, y - 1)]
        except KeyError:
            top_left = None
        if top_left is not None:
            self.neighbors.append(top_left)

        try:
            top = cell_dict[(x, y - 1)]
        except KeyError:
            top = None
        if top is not None:
            self.neighbors.append(top)

        try:
            top_right = cell_dict[(x + 1, y - 1)]
        except KeyError:
            top_right = None
        if top_right is not None:
            self.neighbors.append(top_right)

        try:
            left = cell_dict[(x - 1, y)]
        except KeyError:
            left = None
        if left is not None:
            self.neighbors.append(left)

        try:
            right = cell_dict[(x + 1, y)]
        except KeyError:
            right = None
        if right is not None:
            self.neighbors.append(right)

        try:
            bot_left = cell_dict[(x - 1, y + 1)]
        except KeyError:
            bot_left = None
        if bot_left is not None:
            self.neighbors.append(bot_left)

        try:
            bot = cell_dict[(x, y + 1)]
        except KeyError:
            bot = None
        if bot is not None:
            self.neighbors.append(bot)

        try:
            bot_right = cell_dict[(x + 1, y + 1)]
        except KeyError:
            bot_right = None
        if bot_right is not None:
            self.neighbors.append(bot_right)

    def update_color(self):
        self.color = colors[self.state.current]
