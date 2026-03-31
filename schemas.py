from pydantic import BaseModel, Field


class RecipeSchema(BaseModel):
    title: str
    cooking_time: int = Field(ge=0, le=200)
    ingredients: str
    description: str
