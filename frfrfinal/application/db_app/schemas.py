from pydantic import BaseModel, ConfigDict, field_validator


class DishBase(BaseModel):
    id: int | str | None = None

    @field_validator('id')
    def id_to_str(cls, v: int) -> str:
        return str(v)


class DishCreate(DishBase):
    title: str
    description: str
    price: str


class DishUpdate(DishBase):
    title: str | None = None
    description: str | None = None
    price: str | None = None


class Dish(DishBase):
    submenu_id: int
    title: str
    description: str
    price: str
    model_config = ConfigDict(from_attributes=True)

    @field_validator('price')
    def new_price(cls, v) -> str:
        return f'{float(v.title()):.2f}'


class SubmenuBase(BaseModel):
    id: int | str | None = None

    @field_validator('id')
    def id_to_str(cls, v: int) -> str:
        return str(v)


class SubmenuCreate(SubmenuBase):
    title: str
    description: str


class SubmenuUpdate(SubmenuBase):
    title: str | None = None
    description: str | None = None


class Submenu(SubmenuBase):
    menu_id: int | None = None
    title: str
    description: str
    dishes_count: int
    model_config = ConfigDict(from_attributes=True)


class MenuBase(BaseModel):
    id: int | str | None = None

    @field_validator('id')
    def id_to_str(cls, v: int) -> str:
        return str(v)


class MenuCreate(MenuBase):
    title: str
    description: str


class MenuUpdate(MenuBase):
    title: str | None = None
    description: str | None = None


class Menu(MenuBase):
    title: str
    description: str
    submenus_count: int
    dishes_count: int
    model_config = ConfigDict(from_attributes=True)
