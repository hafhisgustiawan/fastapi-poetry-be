from pydantic import BaseModel, HttpUrl

from typing import Sequence, Optional

class Recipe(BaseModel):
    id: int
    label: str
    source: str
    url: HttpUrl
    holee: Optional[str] = "" 
    # walaupun optional tetap harus pakai default value ""

"""
Sequence[T] adalah type hint untuk koleksi berurutan yang bisa di-iterasi
dan diakses via index.

Contoh yang termasuk Sequence:
- list
- tuple
- string
- range

Sequence bersifat read-only secara konsep (tidak menjamin bisa dimodifikasi),
cocok untuk data yang hanya dibaca seperti response model.
"""
class RecipeSearchResults(BaseModel):
    results: Sequence[Recipe]


class RecipeCreate(BaseModel):
    label: str
    source: str
    url: HttpUrl
    submitter_id: int
