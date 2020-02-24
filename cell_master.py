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
        self.cell_dictionary, self.active_cells = self.init_cells(rows, columns, size, chance, disease)
        self.set_cell_neighbors()

    def get_cell(self, cell_address):
        return self.cell_dictionary[cell_address]

    def init_cells(self, rows, columns, size, disease, chance):
        cells = {}
        infected = {}
        for c in range(columns):
            for r in range(rows):
                cell = Cell((c, r), size, disease)
                roll = random()
                if roll <= chance:
                    cell.state.trigger('get infected')
                    infected[(c, r)] = cell

                cells[(c, r)] = cell
        self.current_state_data['infected'] = infected.__len__()

        return cells, infected

    def set_cell_neighbors(self):
        for cell in self.cell_dictionary:
            c = self.get_cell(cell)
            self.set_neighbors(c)

    def set_neighbors(self, cell):
        x, y = cell.dictionary_address

        for c in (x-1, x, x+1):
            for r in (y-1, y, y+1):
                try:
                    cell_address = c, r
                    neighbor = self.get_cell(cell_address)
                except KeyError:
                    neighbor = None
                if neighbor is not None and neighbor is not self:
                    cell.neighbors.append(neighbor)

    def next_state(self, transmission_rate, death_rate):
        self.current_state_data['day'] = self.current_state_data['day'] + 1
        state_has_changed = False

        for c in list(self.active_cells.keys()):
            cell = self.get_cell(c)

            if cell.state.current == 'incubation':
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
                for i in new_infections:
                    self.active_cells[i.dictionary_address] = i

                if final_day_reached:
                    del self.active_cells[c]  # Remove Cell From Active Cell List
                    dead = cell.proc_final_day(death_rate)
                    if dead:
                        self.current_state_data['contagious'] = self.current_state_data['contagious'] - 1
                        self.current_state_data['dead'] = self.current_state_data['dead'] + 1
                    else:
                        self.current_state_data['contagious'] = self.current_state_data['contagious'] - 1
                        self.current_state_data['immune'] = self.current_state_data['immune'] + 1

        self.current_state_data['infected'] = self.active_cells.__len__()

        if state_has_changed:
            # Simulation is not done
            return False
        else:
            # Simulation is done
            return True

    def create_state_text(self):

        t_p = self.cell_dictionary.__len__()
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
