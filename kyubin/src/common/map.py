from typing import Any

from src.common.vector import Vector


class Map:
    def __init__(
        self,
        map: list[list[Any]],
    ) -> None:
        self.map = map
        self.nrows = len(map)
        self.ncols = len(map[0])

    def within_range(self, vec: Vector) -> bool:
        """
        Check if Vector is within range of map
        """
        return (
            vec.row >= 0
            and vec.row < self.nrows
            and vec.col >= 0
            and vec.col < self.ncols
        )

    def get_val(self, vec: Vector) -> Any:
        """
        Retrieve integer value at point Vector
        """
        return self.map[vec.row][vec.col]
