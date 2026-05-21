from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.issues import router as issues_router
from app.middleware.timer import timing_middleware

app = FastAPI()

app.middleware("http")(timing_middleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(issues_router)

# 
items = [
    {"id": 1, "name": "Item One"},
    {"id": 2, "name": "Item Two"},
    {"id": 3, "name": "Item Three"},
]

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/items")
def get_item():
    return items

@app.get(f"/items/{id}")
def get_item_by_id(id: int):
    if (id > len(items) - 1) or (id < 0):
        return {"message": "Item not found"}
    return items[id];

@app.post("/items")
def create_item(item: dict):
    items.append(item)
    return item