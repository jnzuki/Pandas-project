from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models.recipe import Recipe
from ..models.ingredient import Ingredient
from ..models import recipe as model
from sqlalchemy.exc import SQLAlchemyError
from ..schemas.recipe import RecipeCreate, RecipeUpdate, RecipeResponse
from typing import List



def create_recipe(db: Session, request: RecipeCreate) -> List[RecipeResponse]:
    created_recipes = []

    for ingredient_id, quantity_needed in zip(request.ingredient_id, request.quantity):
        # Check if the ingredient exists
        ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
        if not ingredient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Ingredient with ID {ingredient_id} not found!"
            )

        # Check if sufficient quantity exists
        if ingredient.quantity < quantity_needed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock for ingredient '{ingredient.name}'. Required: {quantity_needed}, Available: {ingredient.quantity}"
            )

        # Deduct the quantity from the ingredient stock
        ingredient.quantity -= quantity_needed
        db.add(ingredient)

        # Create a recipe entry
        new_recipe = Recipe(
            menu_item_id=request.menu_item_id,
            ingredient_id=ingredient_id,
            quantity=quantity_needed
        )
        db.add(new_recipe)
        db.flush()  # Ensure IDs are assigned
        created_recipes.append(new_recipe)

    # Commit the changes
    db.commit()

    # Convert SQLAlchemy objects to Pydantic models
    response = [RecipeResponse.from_orm(recipe) for recipe in created_recipes]
    return response




def read_all(db: Session) -> list[Recipe]:
    try:
        return db.query(Recipe).all()
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e.__dict__.get("orig", "Database error occurred"))
        )


def read_one(db: Session, recipe_id: int) -> Recipe:
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recipe with ID {recipe_id} not found."
        )
    return recipe


def update(db: Session, recipe_id: int, request: RecipeUpdate) -> Recipe:
    recipe_query = db.query(Recipe).filter(Recipe.id == recipe_id)
    existing_recipe = recipe_query.first()

    if not existing_recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recipe with ID {recipe_id} not found."
        )

    try:
        update_data = request.dict(exclude_unset=True)
        recipe_query.update(update_data, synchronize_session=False)
        db.commit()
        return recipe_query.first()

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e.__dict__.get("orig", "Database error occurred"))
        )


def delete(db: Session, recipe_id: int) -> None:
    recipe_query = db.query(Recipe).filter(Recipe.id == recipe_id)
    existing_recipe = recipe_query.first()

    if not existing_recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recipe with ID {recipe_id} not found."
        )

    try:
        recipe_query.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e.__dict__.get("orig", "Database error occurred"))
        )
