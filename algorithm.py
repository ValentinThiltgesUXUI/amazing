"""
Module de génération de labyrinthes.
Fournit l'algorithme de création du labyrinthe à partir d'une grille logique.
"""

from printer import CellType, Printer

def get_neighbour(pos: tuple[int, int], direction: str) -> tuple[int, int]:
    """
    Donne la coordonnée voisine (x, y) depuis la position 'pos' selon la direction donnée.

    Args:
        pos:        Coordonnées (x, y) du point de départ
        direction:  "north", "south", "east", "west"

    Returns:
        Coordonnées (x, y) du voisin dans la direction choisie
    """
    x, y = pos
    if direction == "north":
        return (x, y - 1)
    elif direction == "south":
        return (x, y + 1)
    elif direction == "east":
        return (x + 1, y)
    elif direction == "west":
        return (x - 1, y)
    else:
        raise ValueError(f"Direction inconnue: {direction}")

def case_type(cell: tuple | None) -> str:
    """
    Retourne le type de la cellule sous forme de chaine et un code numérique.
    Args:
        cell: tuple (CellType, couleur) ou None

    Returns:
        tuple : (type_str, code)
            type_str in ("WALL", "POINT", "SPACE", "UNDEFINED")
            code: 0 (WALL), 1 (POINT), 2 (SPACE), 3 (UNDEFINED)
    """
    if cell is None:
        return "SPACE_UNVISITED"
    if cell[0] == CellType.WALL:
        return "WALL"
    elif cell[0] == CellType.POINT:
        return "POINT"
    elif cell[0] == CellType.SPACE:
        return "SPACE_VISITED"
    else:
        raise ValueError(f"Type de case inconnue: {cell[0]}")

def get_free_neighbours(grid, pos) -> list[tuple[str, str]]:
    free = []
    for direction in ["north", "south", "east", "west"]:
        n_pos = get_neighbour(pos, direction)
        n_ct = grid[n_pos[1]][n_pos[0]]
        if case_type(n_ct) == "SPACE_UNVISITED":
            free.append(n_pos)
    return free

def generate_maze(
    grid: list[list[tuple | None]],
    seed: str,
    entry: tuple[int, int],
    exit_: tuple[int, int],
) -> list[list[tuple | None]]:
    """
    Génère le labyrinthe avec un DFS (recursive backtracker).
    Utilise yield pour animer chaque étape.
    """
    import random
    random.seed(seed)

    stack = [entry]
    yield grid

    while stack:
        pos = stack[-1]
        neighbours = get_free_neighbours(grid, pos)

        if neighbours:
            # Choisir un voisin libre au hasard
            next_pos = random.choice(neighbours)
            # Creuser le passage
            Printer.set_cell(grid, next_pos[0], next_pos[1], CellType.SPACE, Printer.BLACK)
            stack.append(next_pos)
            yield grid
        else:
            # Impasse → backtrack
            stack.pop()
            yield grid
