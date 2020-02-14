from random import random

from cell import Cell


class CellMaster:

    def __init__(self, rows, columns, size, chance):
        self.cells = self.init_cells(rows, columns, size, chance)

    @staticmethod
    def init_cells(rows, columns, size, chance):
        cells = {}
        for c in range(columns):
            for r in range(rows):
                cell = Cell((c, r), size)
                roll = random()
                if roll <= chance:
                    cell.state.trigger('get infected')
                cells[(c, r)] = cell

        for cell in cells:
            c = cells[cell]
            c.set_neighbors(cells)

        return cells

    def next_state(self):
        for c in self.cells:
            cell = self.cells[c]
            if cell.state.current == 'healthy' or cell.state.current == 'dead' or cell.state.current == 'immune':
                continue
            elif cell.state.current == 'day 5':
                cell.proc_final_day()
                cell.infect_neighbors()
            elif cell.state.current == 'day 1' or cell.state.current == 'day 2':
                cell.state.trigger('day pass')
            elif cell.state.current == 'day 3' or cell.state.current == 'day 4':
                cell.state.trigger('day pass')
                cell.infect_neighbors()
