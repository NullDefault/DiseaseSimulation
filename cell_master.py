from random import randint
from cell import Cell


class CellMaster:

    def __init__(self, rows, columns):
        self.cells = self.init_cells(rows, columns)

    @staticmethod
    def init_cells(rows, columns):
        cells = {}
        for c in range(columns):
            for r in range(rows):
                cell = Cell((c, r))
                roll = randint(0, 9)
                if roll == 0:
                    cell.state.trigger('get infected')
                cells[(c, r)] = cell

        for cell in cells:
            c = cells[cell]
            c.set_neighbors(cells)

        return cells

    def next_state(self):
        for c in self.cells:
            cell = self.cells[c]
            if cell.state.current == 'healthy':
                cell.proc_infection_chance()
            elif cell.state.current == 'day 5':
                cell.proc_final_day()
            elif cell.state.current is not 'dead' and cell.state.current is not 'immune':
                cell.proc_day_pass()




