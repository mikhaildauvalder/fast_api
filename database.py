from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.testing.schema import mapped_column

engine = create_async_engine("sqlite+aiosqlite:///recipes.db")
new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with new_session() as session:
        yield session


class Base(DeclarativeBase):
    pass


class RecipeModel(Base):
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    cooking_time: Mapped[int]
    ingredients: Mapped[str]
    description: Mapped[str]
    views: Mapped[int] = mapped_column(default=0)
