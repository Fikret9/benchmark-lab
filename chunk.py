from dataclasses import dataclass

@dataclass
class Chunk:
    id: int
    text: str
    source: str
    word_offset: int
    vector: list[float] | None = None