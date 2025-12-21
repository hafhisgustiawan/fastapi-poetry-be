from fastapi import FastAPI, APIRouter, HTTPException
from typing import Optional, List

from app.schemas import RecipeCreate, RecipeSearchResults, Recipe

app = FastAPI(title="Recipe API", openapi_url="/openapi.json")

api_router = APIRouter()

RECIPES = [
        {
            "id": 1,
            "label": "Chicken Vesuvio",
            "source": "Serious Eats",
            "url": "http://www.seriouseats.com/recipes/2011/12/chicken-vesuvio-recipe.html",
        },
        {
            "id": 2,
            "label": "Chicken Paprikash",
            "source": "No Recipes",
            "url": "http://norecipes.com/recipe/chicken-paprikash/",
        },
        {
            "id": 3,
            "label": "Cauliflower and Tofu Curry Recipe",
            "source": "Serious Eats",
            "url": "http://www.seriouseats.com/recipes/2011/02/cauliflower-and-tofu-curry-recipe.html",
        },
    ]

@api_router.get("/", status_code=200)
def root() -> dict:
    """
    Root GET
    """
    return {"msg": "Hello, World!"}

@api_router.get('/test', status_code=200)
def test() -> list[dict]:
    # key property disini harus pake tanda kutip
    name = [
        {
            "name": 'hafhis',
            "active": True
        }, 
        {
            "name": 'hafhis',
            "active": False
        }, 
        {
            "name": 'hafhis',
            "active": True
        }, 
    ]
    
    # ini adalah list comprehension, seperti .map() di js
    
    # list comprehension ini versi simple dari for loop dibawah
    # for n in numbers:
    #     if n % 2 == 0:
    #         result.append(n)
    return [n for n in name if n["active"]]

# route kali ini kita akan coba pake validasi otomatis dari pydantic (ini ter-install otomatis ketika install fastapi di venv), cek -> pip list
# untuk init dynamic path, disini pake {<variable>} dan kalo di js pake :<variable>
@api_router.get('/recipe/{id_recipe}', response_model=List[Recipe])
def getRecipe(*, id_recipe: int):
    # kalo langsung return ini akan error karena function ini infer type nya dict (atau object kalo di js), kalo mau return array ya pake list[dict]
    # return RECIPES
    
    mappedResult = [n for n in RECIPES if n["id"]==id_recipe]
    
    if (len(mappedResult) == 0):
        raise HTTPException(
            status_code=404, detail=f"Recipe with ID {id_recipe} not found"
        )
    
    return mappedResult[0] if len(mappedResult) > 0 else {}


# kali ini kita akan implement search dari sebuah object
# status_code ini adalah optional params, gaboleh langsung misal:
# @api_router.get('/search', 200)
# bakal dapet error ini -> TypeError: APIRouter.get() takes 2 positional arguments but 3 were given
@api_router.get('/search', status_code=200, response_model=RecipeSearchResults)
# parameter tanpa default (request) tidak boleh setelah yang punya default
def searchRecipe(
    keyword: Optional[str] = None, max_result: Optional[int] = None
):
    
    # if dengan negasi
    if not keyword and max_result:
        # list slicing, googling pak
        return {"results": RECIPES[:max_result]}
    
    results = filter(lambda recipe: keyword.lower() in recipe["label"].lower(), RECIPES)
    return {"results": list(results)[:max_result]}

# kita akan add recipe
@api_router.post('/add-recipe', status_code=201)
def createRecipe(*, payload: RecipeCreate):

    return [*payload]

app.include_router(api_router)


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")