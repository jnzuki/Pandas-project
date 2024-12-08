from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..controllers import recipe as controller
from ..schemas.recipe import Recipe, RecipeCreate, RecipeUpdate, RecipeResponse
from ..dependencies.database import get_db
from typing import List


router = APIRouter(
    tags=["Recipes"],
    prefix="/recipes"
)


@router.post("/", response_model=List[RecipeResponse], summary="Create recipes")
def create_recipe_endpoint(request: RecipeCreate, db: Session = Depends(get_db)):
    return controller.create_recipe(db, request)



@router.get("/", response_model=list[Recipe], summary="Retrieve all recipes")
def get_all_recipes(db: Session = Depends(get_db)):
    return controller.read_all(db=db)


@router.get("/{recipe_id}", response_model=Recipe, summary="Retrieve a single recipe by ID")
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db=db, recipe_id=recipe_id)


@router.put("/{recipe_id}", response_model=Recipe, summary="Update a recipe by ID")
def update_recipe(recipe_id: int, request: RecipeUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, recipe_id=recipe_id)


@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a recipe by ID")
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    controller.delete(db=db, recipe_id=recipe_id)
    return {"detail": "Recipe deleted successfully"}
