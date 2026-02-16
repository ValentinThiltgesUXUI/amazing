"""
Module de génération de labyrinthes.
Fournit l'algorithme de création du labyrinthe à partir d'une grille logique.
"""

from printer import CellType, Printer


def get_neighbour(pos: tuple[int, int], direction: str) -> tuple[int, int]:
    """
    Donne la cellule jouable voisine depuis 'pos' selon la direction.
    Saute de 2 cases (car les cellules jouables sont aux positions impaires).

    Args:
        pos:        Coordonnées (x, y) du point de départ
        direction:  "north", "south", "east", "west"

    Returns:
        Coordonnées (x, y) du voisin jouable
    """
    x, y = pos
    if direction == "north":
        return (x, y - 2)
    elif direction == "south":
        return (x, y + 2)
    elif direction == "east":
        return (x + 2, y)
    elif direction == "west":
        return (x - 2, y)
    else:
        raise ValueError(f"Direction inconnue: {direction}")


def get_wall_between(
    pos: tuple[int, int], neighbour: tuple[int, int]
) -> tuple[int, int]:
    """
    Retourne la position du mur entre deux cellules jouables adjacentes.
    """
    return (pos[0] + neighbour[0]) // 2, (pos[1] + neighbour[1]) // 2


def case_type(cell: tuple | None) -> str:
    """
    Retourne le type de la cellule.

    Args:
        cell: tuple (CellType, couleur) ou None

    Returns:
        "SPACE_UNVISITED", "WALL", "POINT", ou "SPACE_VISITED"
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


def get_free_neighbours(
    grid: list[list[tuple | None]], pos: tuple[int, int]
) -> list[tuple[int, int]]:
    """
    Retourne la liste des cellules jouables voisines non visitées.
    Vérifie les bornes de la grille avant d'accéder.
    """
    grid_h = len(grid)
    grid_w = len(grid[0])
    free = []
    for direction in ["north", "south", "east", "west"]:
        n_pos = get_neighbour(pos, direction)
        nx, ny = n_pos
        if 0 <= ny < grid_h and 0 <= nx < grid_w:
            if case_type(grid[ny][nx]) == "SPACE_UNVISITED":
                free.append(n_pos)
    return free


def generate_maze(
    grid: list[list[tuple | None]],
    seed: int,
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
            next_pos = random.choice(neighbours)
            # Ouvrir le mur entre la position actuelle et le voisin
            wall = get_wall_between(pos, next_pos)
            Printer.set_cell(grid, wall[0], wall[1], CellType.SPACE, Printer.BLACK)
            # Marquer le voisin comme visité
            Printer.set_cell(grid, next_pos[0], next_pos[1], CellType.SPACE, Printer.BLACK)
            stack.append(next_pos)
            yield grid
        else:
            stack.pop()
            yield grid
