from random import random

from cell import Cell


class CellMaster:

    def __init__(self, rows, columns, size, chance, disease):
        self.current_state_data = {
            'infected': 0,
            'contagious': 0,
            'dead': 0,
            'immune': 0,
            'day': 0
        }
        self.cells = self.init_cells(rows, columns, size, chance, disease)
        self.set_cell_neighbors()

    def init_cells(self, rows, columns, size, disease, chance):
        infected_count = 0
        cells = {}
        for c in range(columns):
            for r in range(rows):
                cell = Cell((c, r), size, disease)
                roll = random()
                if roll <= chance:
                    cell.state.trigger('get infected')
                    infected_count = infected_count + 1
                cells[(c, r)] = cell
        self.current_state_data['infected'] = infected_count

        return cells

    def set_cell_neighbors(self):
        for cell in self.cells:
            c = self.cells[cell]
            self.set_neighbors(c)

    def set_neighbors(self, cell):
        x = cell.x // cell.size
        y = cell.y // cell.size

        for c in (x-1, x, x+1):
            for r in (y-1, y, y+1):
                try:
                    neighbor = self.cells[(c, r)]
                except KeyError:
                    neighbor = None
                if neighbor is not None and neighbor is not self:
                    cell.neighbors.append(neighbor)

    def reset(self, rows, columns, size, disease, chance):
        self.current_state_data = {
            'infected': 0,
            'contagious': 0,
            'dead': 0,
            'immune': 0,
            'day': 0
        }
        self.cells = self.init_cells(rows, columns, size, disease, chance)
        self.set_cell_neighbors()

    def next_state(self, transmission_rate, death_rate):
        self.current_state_data['day'] = self.current_state_data['day'] + 1
        state_has_changed = False
        for c in self.cells:
            cell = self.cells[c]
            if cell.state.current == 'healthy' or cell.state.current == 'dead' or cell.state.current == 'immune':
                continue

            elif cell.state.current == 'incubation':
                if not state_has_changed:
                    state_has_changed = True
                incubation_complete = cell.incubate()
                if incubation_complete:
                    self.current_state_data['contagious'] = self.current_state_data['contagious'] + 1

            elif cell.state.current == 'contagious':
                if not state_has_changed:
                    state_has_changed = True
                final_day_reached = cell.progress_disease()
                new_infections = cell.infect_neighbors(transmission_rate)

                self.current_state_data['infected'] = self.current_state_data['infected'] + new_infections

                if final_day_reached:
                    dead = cell.proc_final_day(death_rate)
                    if dead:
                        self.current_state_data['contagious'] = self.current_state_data['contagious'] - 1
                        self.current_state_data['dead'] = self.current_state_data['dead'] + 1
                    else:
                        self.current_state_data['contagious'] = self.current_state_data['contagious'] - 1
                        self.current_state_data['immune'] = self.current_state_data['immune'] + 1

        if state_has_changed:
            # Simulation is not done
            return False
        else:
            # Simulation is done
            return True

    def create_state_text(self):

        t_p = self.cells.__len__()
        i = self.current_state_data['infected']
        i_percent = i / t_p * 100
        c = self.current_state_data['contagious']
        c_percent = c / t_p * 100
        d = self.current_state_data['dead']
        d_percent = d / t_p * 100
        im = self.current_state_data['immune']
        im_percent = im / t_p * 100

        total_population = "Total Population: " + str(t_p)
        infected = "Affected: " + str(i) + " ("+str(i_percent)[0:4]+"% of Total)"
        contagious = "Contagious: " + str(c) + " ("+str(c_percent)[0:4]+"% of Total)"
        dead = "Dead: " + str(d) + " ("+str(d_percent)[0:4]+"% of Total)"
        immune = "Immune: " + str(im) + " ("+str(im_percent)[0:4]+"% of Total)"
        day = "Day: "+str(self.current_state_data['day'])

        state_text = total_population + '<br><br>' + infected + '<br><br>' + contagious + '<br><br>' + dead + \
                     '<br><br>' + immune + '<br><br>' + day

        return state_text
