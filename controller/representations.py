from pydantic import BaseModel

class Partition:
    name: str | None
    partition_id: int
    categories: list[str] | None


class CategorizedNoun(BaseModel):
    category: str
    original_object: str
    reasoning: str



