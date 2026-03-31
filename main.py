import uvicorn
from fastapi import FastAPI, Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, desc, asc
from database import engine, Base, get_session, RecipeModel
from schemas import RecipeSchema

app = FastAPI()

SessionDep = Annotated[AsyncSession, Depends(get_session)]


# ЗАКОММИТИЛ УЖЕ С ГОТОВОЙ
@app.post(
    "/database_startup",
    tags=["База данных"],
    summary="Создание базы данных перед использованием",
)
async def create_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return {"База данных создана": True}


@app.get("/recipes", tags=["Рецепты"], summary="Получить список всех рецептов")
async def get_recipe(session: SessionDep):
    query = select(
        RecipeModel.title, RecipeModel.views, RecipeModel.cooking_time
    ).order_by(desc(RecipeModel.views), asc(RecipeModel.cooking_time))
    result = await session.execute(query)
    return result.mappings().all()


@app.get(
    "/recipes/{recipe_id}", tags=["Рецепты"], summary="Получить один конкретный рецепт"
)
async def get_spec_recipe(recipe_id, session: SessionDep):
    query = select(RecipeModel).where(RecipeModel.id == recipe_id)
    counter_query = (
        update(RecipeModel)
        .values(views=RecipeModel.views + 1)
        .where(RecipeModel.id == recipe_id)
    )
    await session.execute(counter_query)
    await session.commit()
    result = await session.execute(query)
    return result.scalar()


@app.post("/recipes", tags=["Рецепты"], summary="Добавить новый рецепт")
async def get_recipes(data: RecipeSchema, session: SessionDep):
    new_recipe = RecipeModel(
        title=data.title,
        cooking_time=data.cooking_time,
        ingredients=data.ingredients,
        description=data.description,
    )
    session.add(new_recipe)
    await session.commit()
    return {"message": "Рецепт добавлен!"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
