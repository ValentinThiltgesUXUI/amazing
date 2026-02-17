class OutOfBound(Exception):
    """Exception levée quand une coordonnée est hors des limites."""
    pass


def check_bounds(grid: list[list], point: tuple[int, int]) -> bool:
    """
    Vérifie si un point se trouve dans les limites de la grille.

    Args:
        grid: La grille (liste de listes)
        point: Le point à vérifier (x, y)

    Returns:
        True si le point est dans les limites, False sinon

    Raises:
        OutOfBound: Si le point est hors des limites de la grille
    """
    x, y = point
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0

    if x < 0 or x >= width or y < 0 or y >= height:
        msg = f"Coordonnée ({x}, {y}) est hors des limites "
        msg += f"({width}x{height})"
        raise OutOfBound(msg)

    return True
