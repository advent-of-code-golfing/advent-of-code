from dataclasses import dataclass


@dataclass
class Vector:
    row: int
    col: int

    def __eq__(self, value: object) -> bool:
        """
        Check if two vectors are equal
        """
        if not isinstance(value, Vector):
            raise ValueError("Cannot object these objects!")
        return self.row == value.row and self.col == value.col

    def __add__(self, value: "Vector") -> "Vector":
        """
        Adds two vectors together
        """
        return Vector(self.row + value.row, self.col + value.col)

    def __str__(self) -> str:
        return f"({self.row},{self.col})"
    
    def __repr__(self) -> str:
        return f"Vector({self.row},{self.col})"

    def __hash__(self) -> int:
        return hash((self.row, self.col))
