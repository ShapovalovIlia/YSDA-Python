class LifeGame(object):
    """
    Class for Game life
    """

    def __init__(self, ocean: list[list[int]]):
        self._cells = ocean
        self._rows = len(ocean)
        self._cols = len(ocean[0]) if ocean else 0

    def _get_neighbours(self, i: int, j: int) -> list[int]:
        lst: list[int] = []
        for x in range(max(0, i - 1), min(i + 2, self._rows)):
            for y in range(max(0, j - 1), min(j + 2, self._cols)):
                if (x, y) != (i, j):
                    lst.append(self._cells[x][y])
        return lst

    def _check_animal(self, animal: int, i: int, j: int) -> int:
        ngb: list[int] = self._get_neighbours(i, j)
        animal_count: int = ngb.count(animal)
        if animal_count >= 4 or animal_count <= 1:
            return 0
        return animal

    def _check_empty(self, i: int, j: int) -> int:
        ngb: list[int] = self._get_neighbours(i, j)
        if ngb.count(2) == 3:
            return 2
        elif ngb.count(3) == 3:
            return 3
        return 0

    def _check_any(self, i: int, j: int) -> int:
        match self._cells[i][j]:
            case 0:
                return self._check_empty(i, j)
            case 2:
                return self._check_animal(2, i, j)
            case 3:
                return self._check_animal(3, i, j)
            case 1:
                return 1
            case _:
                raise ValueError

    def _update(self) -> None:
        new_cells = [[0 for _ in range(self._cols)] for _ in range(self._rows)]
        for i in range(self._rows):
            for j in range(self._cols):
                new_cells[i][j] = self._check_any(i, j)

        self._cells = new_cells

    def get_next_generation(self) -> list[list[int]]:
        self._update()
        return self._cells
