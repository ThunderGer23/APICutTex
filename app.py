from fastapi import FastAPI
from routes.cutFile import cF
from docs.docs import tags_metadata
from os import environ as env

app = FastAPI(
    title= "Someone title :v/ vrgs",
    description= "Someone description :v/ prrna",
    version= "1.1.0",
    openapi_tags= tags_metadata
)

app.include_router(cF)