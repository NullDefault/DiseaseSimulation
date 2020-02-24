from random import random

import pygame
from fysom import Fysom

infectedStates = ['day 1', 'day 2', 'day 3', 'day 4']

colors = {
    'healthy': pygame.color.Color(200, 200, 255),
    'incubation': pygame.color.Color(255, 255, 150),
    'contagious': pygame.color.Color(255, 0, 0),
    'dead': pygame.color.Color(0, 0, 0),
    'immune': pygame.color.Color(51, 204, 51)
}


class Cell:
    def __init__(self, location, size, disease):
        self.state = Fysom({
            'initial': 'healthy',
            'events': [
                {'name': 'get infected', 'src': 'healthy', 'dst': 'incubation'},
                {'name': 'finish incubation', 'src': 'incubation', 'dst': 'contagious'},
                {'name': 'die', 'src': 'contagious', 'dst': 'dead'},
                {'name': 'recover', 'src': 'contagious', 'dst': 'immune'},
            ],
        })
        self.incubation_duration = disease['incubation duration']
        self.contagious_duration = disease['contagious duration']
        self.color = colors[self.state.current]
        self.next_trigger = None
        self.neighbors = []
        self.size = size
        self.x, self.y = location[0] * self.size, location[1] * self.size

    @property
    def dictionary_address(self):
        return self.x // self.size, self.y // self.size

    def day_trigger(self):
        if self.next_trigger is not None:
            self.state.trigger(self.next_trigger)
        self.next_trigger = None

    def progress_disease(self):
        self.contagious_duration = self.contagious_duration - 1
        if self.contagious_duration <= 0:
            return True

    def incubate(self):
        self.incubation_duration = self.incubation_duration - 1
        if self.incubation_duration <= 0:
            self.state.trigger('finish incubation')
            return True

    def infect_neighbors(self, transmission_rate):
        infections = []
        for neighbor in self.neighbors:
            if neighbor.state.current is 'healthy':
                infected = neighbor.proc_infection_chance(transmission_rate)
                if infected:
                    infections.append(neighbor)

        return infections

    def proc_infection_chance(self, transmission_rate):
        roll = random()
        if roll <= transmission_rate:
            self.next_trigger = 'get infected'
            return True
        else:
            return False

    def proc_final_day(self, death_rate):
        roll = random()
        if roll <= death_rate:
            self.next_trigger = 'die'
            return True
        else:
            self.next_trigger = 'recover'
            return False

    def update_color(self):
        self.color = colors[self.state.current]
