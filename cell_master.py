from random import random

from cell import Cell


class CellMaster:

    def __init__(self, rows, columns, size, chance):
        self.current_state_data = {
            'infected': 0,
            'contagious': 0,
            'dead': 0,
            'immune': 0
        }
        self.cells = self.init_cells(rows, columns, size, chance)

    def init_cells(self, rows, columns, size, chance):
        infected_count = 0
        cells = {}
        for c in range(columns):
            for r in range(rows):
                cell = Cell((c, r), size)
                roll = random()
                if roll <= chance:
                    cell.state.trigger('get infected')
                    infected_count = infected_count + 1
                cells[(c, r)] = cell
        self.current_state_data['infected'] = infected_count
        for cell in cells:
            c = cells[cell]
            c.set_neighbors(cells)

        return cells

    def reset(self, rows, columns, size, chance):
        self.current_state_data = {
            'infected': 0,
            'contagious': 0,
            'dead': 0,
            'immune': 0
        }
        self.cells = self.init_cells(rows, columns, size, chance)

    def next_state(self, transmission_rate, death_rate):
        state_has_changed = False
        for c in self.cells:
            cell = self.cells[c]
            if cell.state.current == 'healthy' or cell.state.current == 'dead' or cell.state.current == 'immune':
                continue
            elif cell.state.current == 'day 5':
                if not state_has_changed:
                    state_has_changed = True
                dead = cell.proc_final_day(death_rate)
                new_infections = cell.infect_neighbors(transmission_rate)

                if dead:
                    self.current_state_data['contagious'] = self.current_state_data['contagious'] - 1
                    self.current_state_data['dead'] = self.current_state_data['dead'] + 1
                else:
                    self.current_state_data['contagious'] = self.current_state_data['contagious'] - 1
                    self.current_state_data['immune'] = self.current_state_data['immune'] + 1

                self.current_state_data['infected'] = self.current_state_data['infected'] + new_infections

            elif cell.state.current == 'day 1':
                if not state_has_changed:
                    state_has_changed = True
                cell.state.trigger('day pass')
            elif cell.state.current == 'day 2':
                if not state_has_changed:
                    state_has_changed = True
                cell.state.trigger('day pass')
                self.current_state_data['contagious'] = self.current_state_data['contagious'] + 1
            elif cell.state.current == 'day 3' or cell.state.current == 'day 4':
                if not state_has_changed:
                    state_has_changed = True
                cell.state.trigger('day pass')
                new_infections = cell.infect_neighbors(transmission_rate)

                self.current_state_data['infected'] = self.current_state_data['infected'] + new_infections

        if state_has_changed:
            # Simulation is not done
            return False
        else:
            # Simulation is done
            return True

    def create_state_text(self):

        total_population = "Total Population: " + str(self.cells.__len__())
        infected = "Infected: " + str(self.current_state_data['infected'])
        contagious = "Contagious: " + str(self.current_state_data['contagious'])
        dead = "Dead: " + str(self.current_state_data['dead'])
        immune = "Immune: " + str(self.current_state_data['immune'])

        state_text = total_population + '<br><br>' + infected + '<br><br>' + contagious + '<br><br>' + dead + '<br><br>' + immune

        return state_text
