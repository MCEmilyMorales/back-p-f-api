from fastapi import FastAPI
from app.api.database import db
from app.api.user.route import add_user_routes
from app.api.image.route import add_imagen_routes

app = FastAPI()

add_user_routes(app)
add_imagen_routes(app)

@app.on_event("startup")
async def startup():
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()
    
@app.get("/")
async def root():
    return {"message": "ejecutado desde main"}