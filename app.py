from fastapi import FastAPI
from routes.cutFile import cF
from docs.docs import tags_metadata
from notigram import ping

ping('daa39d53-6283-47a1-b945-b7ee6528dde0', 'Aquí API ya esta pateando!')
app = FastAPI(
    title= "APICutText",
    description= "Someone description :v/ prrna",
    version= "1.1.0",
    openapi_tags= tags_metadata
)

app.include_router(cF)