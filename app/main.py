from fastapi import FastAPI
from app.api.database import db
from app.api.user.route import add_user_routes
from app.api.image.route import add_imagen_routes
from app.api.patient.route import add_paciente_routes
from app.api.informe.route import add_informe_routes

app = FastAPI(
    openapi_tags=[
        {"name": "Usuarios", "description": "Operaciones relacionadas con la tabla usuarios"},
        {"name": "Imágenes", "description": "Operaciones relacionadas con la tabla imágenes"},
        {"name": "Paciente", "description": "Operaciones relacionadas con la tabla paciente"},
        {"name": "Informe", "description": "Operaciones relacionadas con la tabla de informe"},

    ])

add_user_routes(app)
add_imagen_routes(app)
add_paciente_routes(app)
add_informe_routes(app)

@app.on_event("startup")
async def startup():
    print("✅ Prisma está conectado correctamente")
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()
    
@app.get("/")
async def root():
    return {"message": "ejecutado desde main"}