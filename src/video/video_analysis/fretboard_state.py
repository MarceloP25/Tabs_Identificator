from dataclasses import dataclass
import numpy as np
from typing import List, Tuple

@dataclass
class Fret:
    index: int
    x: int  # coordenada x no espaço retificado

@dataclass
class String:
    index: int
    y: int  # coordenada y no espaço retificado

@dataclass
class FretboardState:
    frame_index: int
    rectified_image: np.ndarray

    bbox_original: Tuple[int, int, int, int]

    frets: List[Fret]
    strings: List[String]

    coordinate_space: str = "rectified"
