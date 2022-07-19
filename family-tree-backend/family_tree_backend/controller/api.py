from fastapi import FastAPI

from family_tree_backend import STORAGE_FOLDER
from family_tree_backend.__main__ import ft
from family_tree_backend.model.person_light import PersonLight
from family_tree_backend.util.rdf_interface import store_graph

app = FastAPI()


@app.get("/")
def get_ft():
    return [PersonLight.from_person(p) for p in ft.persons]


@app.get("/load")
def load_ft(file: str):
    ft.import_ft(f"{STORAGE_FOLDER}/{file}")
    return get_ft()


@app.post("/store")
def store_ft(file: str):
    store_graph(ft.graph, f"{STORAGE_FOLDER}/{file}")


@app.get("/person/{person}")
def get_person(person: str):
    pass