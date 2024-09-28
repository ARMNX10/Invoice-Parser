from dataclasses import dataclass


@dataclass
class Resolution:
    width: int
    height: int


@dataclass
class Vertex:
    x: int
    y: int

    def __add__(self, o):
        return Vertex(x=o.x + self.x, y=o.y + self.y)


@dataclass
class BoundingBox:
    topleft: Vertex
    topright: Vertex
    bottomleft: Vertex
    bottomright: Vertex


@dataclass
class Word:
    text: str
    center: Vertex
    bounding_box: BoundingBox
    page: int
    resolution: Resolution

