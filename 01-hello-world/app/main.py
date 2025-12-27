from fastapi import FastAPI, APIRouter, HTTPException, Depends
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

from app.schema.recipe import RecipeCreate, RecipeSearchResults, Recipe, GetRecipeRequest
from app.schema.food import Food, GetFoodResponse

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

# REQUEST BODY ITU HARUS PAKE PYDANTIC MODEL
# PATH PAKE {} DI URL DAN DIBACA DI PARAM : When you declare other function parameters that are not part of the path parameters, they are automatically interpreted as "query" parameters.
# QUERY BAKAL DI BACA OTOMATIS DI PARAM

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
# untuk init dynamic path, disini pake {<variable>}

@api_router.get('/recipe/{id_recipe}', response_model=List[Recipe])
def getRecipe(*, id_recipe: int):
    # parameter * artinya Semua parameter setelah * harus pakai key value pairs, contoh pemanggilan getRecipe(id_recipe=1)
    # Nb: kalo disini sih gak ngaruh krn cuma ada 1 param
    # Cek : https://fastapi.tiangolo.com/tutorial/path-params-numeric-validations/#summary
    
    mappedResult = [n for n in RECIPES if n["id"]==id_recipe]
    
    if (len(mappedResult) == 0):
        raise HTTPException(
            status_code=404, detail=f"Recipe with ID {id_recipe} not found"
        )
    
    return mappedResult[0] if len(mappedResult) > 0 else {}

# note: deps injection
# kali ini kita akan implement search dari sebuah object
# status_code ini adalah optional params, gaboleh langsung misal:
# @api_router.get('/search', 200)
# bakal dapet error ini -> TypeError: APIRouter.get() takes 2 positional arguments but 3 were given
# parameter tanpa default (request) tidak boleh setelah yang punya default

# note: query parameter
# jadi untuk parameter di python ini gausah di pusingin urutannya, apalagi yang udah ada key nya (e.g get_data(Name=Optional[str]=None)) jadi anggap aja ini object dan manggilnya pun pake key ya gini (e.g get_data(Name="Hafhis"))
# 
# Untuk kasus di bawah ini juga sama, gak ada aturan pakem yang harus dipikirin. Jadi sebelumnya itu pake (keyword: Optional[str] = None, max_result: Optional[int] = None) juga bisa
# 
# Nah karena mau pake pydantic, kita bisa set. Yang ngebedain antara request body dan query params ya cuma ada Depends() nya ajah
# 
# When you declare other function parameters that are not part of the path parameters, they are automatically interpreted as "query" parameters.

@api_router.get('/search', status_code=200, response_model=RecipeSearchResults)
def searchRecipe(
    request: GetRecipeRequest = Depends()
):
    if not request.keyword and request.max_result:
        # list slicing, googling pak
        return {"results": RECIPES[:request.max_result]}
    
    results = filter(lambda recipe: request.keyword.lower() in recipe["label"].lower(), RECIPES)
    return {"results": list(results)[:request.max_result]}

# setelah param * itu semua param selanjutnya harus pake key value pairs
@api_router.post('/add-recipe', status_code=201)
def createRecipe(*, payload: RecipeCreate):

    return [*payload]

@api_router.get('/foods/{total}', response_model=GetFoodResponse)
def getAllFood(*, total: int):
    
    try:
        now = datetime.now()

        foods = [
            Food(
                id=i,
                description=None,
                # name=f"The name of food{i}",
                created_at=now,
                updated_at=now
            )
            for i in range(1, total + 1)
        ]

        return GetFoodResponse(data=foods)
    except Exception as e:
        print('HERE===>',e)
        raise HTTPException(status_code=500, detail=str(e))
    

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

"""
Expect request body seperti dibawah ini:
{
    "name": "Foo",
    "description": "An optional description",
    "price": 45.2,
    "tax": 3.5
}
"""
@app.post("/items/")
async def create_item(item: Item):
    # convert pydantic model to dict
    item_dict = item.model_dump()
    
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        # ini gabisa kalo langsung ke pydantic model
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

app.include_router(api_router)


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")