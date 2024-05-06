from fastapi import APIRouter, Depends, HTTPException

from application.db_app import schemas
from application.services.submenu_service import SubmenuService

router = APIRouter(prefix='/api/v1/menus')


@router.post('/{target_menu_id}/submenus', response_model=schemas.Submenu, status_code=201)
def create_submenu(target_menu_id: int, schema: schemas.SubmenuCreate,
                   submenu: SubmenuService = Depends()) -> HTTPException | schemas.Submenu:
    return submenu.create_submenu(submenu_schemas=schema, menu_id=target_menu_id)


@router.get('/{target_menu_id}/submenus', response_model=list[schemas.Submenu])
def read_submenus(target_menu_id: int,
                  submenu: SubmenuService = Depends()) -> HTTPException | list[schemas.Submenu]:
    return submenu.get_submenus(menu_id=target_menu_id)


@router.patch('/{target_menu_id}/submenus/{target_submenu_id}', response_model=schemas.Submenu)
def update_submenu(target_menu_id: int, target_submenu_id: int, schema: schemas.SubmenuUpdate,
                   submenu: SubmenuService = Depends()) -> HTTPException | schemas.Submenu:
    return submenu.update_submenu(submenu_schemas=schema, menu_id=target_menu_id, submenu_id=target_submenu_id)


@router.delete('/{target_menu_id}/submenus/{target_submenu_id}', response_model=None)
def delete_submenus(target_menu_id: int, target_submenu_id: int,
                    submenu: SubmenuService = Depends()) -> HTTPException | dict[str, str | bool]:
    return submenu.delete_submenu(menu_id=target_menu_id, submenu_id=target_submenu_id)


@router.get('/{target_menu_id}/submenus/{target_submenu_id}', response_model=schemas.Submenu)
def read_submenu(target_menu_id: int, target_submenu_id: int,
                 submenu: SubmenuService = Depends()) -> HTTPException | schemas.Submenu:
    return submenu.get_submenu(menu_id=target_menu_id, submenu_id=target_submenu_id)
