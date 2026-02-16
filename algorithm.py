"""
Module de génération de labyrinthes.
Fournit l'algorithme de création du labyrinthe à partir d'une grille logique.
"""

from printer import CellType, Printer
from collections import deque


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

def get_reachable_neighbours(grid, pos):
    """
    Retourne la liste des voisins accessibles pour une cellule donnée.
    Un voisin est accessible si le mur qui le sépare de la cellule courante est ouvert.

    Args:
        grid: Grille logique du labyrinthe.
        pos:  Position de la cellule (x, y).

    Returns:
        Liste de tuples ((nx, ny), direction) pour chaque voisin accessible.
        - (nx, ny): coordonnées du voisin.
        - direction: 'north', 'south', 'east' ou 'west'.
    """
    grid_h = len(grid)
    grid_w = len(grid[0])
    directions = {
        "north": (0, -2),
        "south": (0, 2),
        "east":  (2, 0),
        "west":  (-2, 0),
    }
    reachable = []

    x, y = pos

    for direction, (dx, dy) in directions.items():
        nx, ny = x + dx, y + dy

        # Vérifie que les coordonnées sont dans la grille
        if not (0 <= nx < grid_w and 0 <= ny < grid_h):
            continue

        # Calculer la position du mur entre la cellule et le voisin
        wx, wy = get_wall_between((x, y), (nx, ny))
        ct = case_type(grid[wy][wx])

        # Si le mur n'est pas un mur (donc ouvert), le voisin est accessible
        if ct != "WALL":
            reachable.append(((nx, ny), direction))

    return reachable

def find_shortest_path(grid, entry, exit_):
    """
    BFS : trouve le plus court chemin de entry à exit_.
    Retourne une string de directions (ex: "SSSEENNWS").
    """
    queue = deque()
    queue.append(entry)
    # Pour chaque cellule visitée, on stocke d'où on vient et par quelle direction
    came_from = {entry: None}

    while queue:
        pos = queue.popleft()

        if pos == exit_:
            # Reconstruire le chemin
            path = []
            current = exit_
            while came_from[current] is not None:
                prev_pos, direction = came_from[current]
                path.append(direction[0].upper())  # "north" → "N"
                current = prev_pos
            path.reverse()
            return "".join(path)

        for neighbour, direction in get_reachable_neighbours(grid, pos):
            if neighbour not in came_from:
                came_from[neighbour] = (pos, direction)
                queue.append(neighbour)

    return ""  # Pas de chemin trouvé

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
