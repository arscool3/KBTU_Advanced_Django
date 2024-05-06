from fastapi import APIRouter, Depends, HTTPException

from application.db_app import schemas
from application.services.dish_service import DishService

router = APIRouter(prefix='/api/v1/menus')


@router.post('/{target_menu_id}/submenus/{target_submenu_id}/dishes',
             response_model=schemas.Dish, status_code=201)
def create_dish(target_menu_id: int, target_submenu_id: int, schema: schemas.DishCreate,
                dish: DishService = Depends()) -> HTTPException | schemas.Dish:
    return dish.create_dish(dish_schemas=schema, menu_id=target_menu_id, submenu_id=target_submenu_id)


@router.get('/{target_menu_id}/submenus/{target_submenu_id}/dishes', response_model=list[schemas.Dish])
def read_dishes(target_menu_id: int, target_submenu_id: int,
                dish: DishService = Depends()) -> list[schemas.Dish]:
    return dish.get_dishes(menu_id=target_menu_id, submenu_id=target_submenu_id)


@router.patch('/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}',
              response_model=schemas.Dish)
def update_dish(target_menu_id: int, target_submenu_id: int, target_dish_id: int,
                schema: schemas.DishUpdate, dish: DishService = Depends()) -> HTTPException | schemas.Dish:
    return dish.update_dish(dish_schemas=schema, menu_id=target_menu_id, submenu_id=target_submenu_id,
                            dish_id=target_dish_id)


@router.delete('/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}', response_model=None)
def delete_dish(target_menu_id: int, target_submenu_id: int, target_dish_id: int,
                dish: DishService = Depends()) -> HTTPException | dict[str, str | bool]:
    return dish.delete_dish(menu_id=target_menu_id, submenu_id=target_submenu_id, dish_id=target_dish_id)


@router.get('/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}',
            response_model=schemas.Dish)
def read_dish(target_menu_id: int, target_submenu_id: int, target_dish_id: int,
              dish: DishService = Depends()) -> HTTPException | schemas.Dish:
    return dish.get_dish(menu_id=target_menu_id, submenu_id=target_submenu_id, dish_id=target_dish_id)
