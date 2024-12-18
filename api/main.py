from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from .routers import vehicles, users, employees, clients
from fastapi.staticfiles import StaticFiles
from models import Usuario
from database import get_db
from sqlalchemy.orm import Session
from .routers.protected import router as protected_router

app = FastAPI()
app.include_router(protected_router)
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Redirección inicial
@app.get("/", include_in_schema=False)
async def home():
    return RedirectResponse("/login")

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(request: Request):
    try:
        # Obtener los datos JSON del body
        data = await request.json()
        email: str = data.get("email")
        password: str = data.get("password")
        
        db = next(get_db())
        user = db.query(Usuario).filter(Usuario.correo == email).first()
        
        if not user or user.contraseña != password:
            raise HTTPException(status_code=401, detail="Credenciales inválidas")
        
        return JSONResponse(content={
            "user_id": user.id,
            "tipo": user.tipo,
            "message": "Login exitoso"
        })
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# @app.post("/login")
# async def login(
#     email: str = Form(...),
#     password: str = Form(...),
#     db: Session = Depends(get_db)
# ):
#     user = db.query(Usuario).filter(Usuario.correo == email).first()
#     if not user or user.contraseña != password:
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#     return {"user_id": user.id, "tipo": user.tipo}

# @app.post("/login")
# def login(email: str, password: str, db: Session = Depends(get_db)):
#     user = db.query(Usuario).filter(Usuario.correo == email).first()
#     if not user or user.contraseña != password:
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#     return {"user_id": user.id, "tipo": user.tipo}

@app.get("/register", response_class=HTMLResponse)
async def get_register_usuario(request: Request):
    return templates.TemplateResponse("usuarios/registrarUsuario.html", {"request": request})

@app.get("/enlaces", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("listaEnlaces.html", {"request": request})

@app.get("/enlacesClient", response_class=HTMLResponse)
async def get_form_client(request: Request):
    return templates.TemplateResponse("listaEnlacesCliente.html", {"request": request})

# Vehículos
@app.get("/vehicles/register", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("vehiculos/registrarVehiculo.html", {"request": request})

@app.get("/vehicles/list", response_class=HTMLResponse)
async def get_lista_vehiculos(request: Request):
    return templates.TemplateResponse("vehiculos/listarVehiculos.html", {"request": request})

@app.get("/vehicles/update", response_class=HTMLResponse)
async def get_update_vehiculo(request: Request):
    return templates.TemplateResponse("vehiculos/updateVehiculo.html", {"request": request})

# Clientes
@app.get("/clients/register", response_class=HTMLResponse)
async def get_register_usuario(request: Request):
    return templates.TemplateResponse("usuarios/registrarUsuario.html", {"request": request})

@app.get("/clients/list", response_class=HTMLResponse)
async def get_listar_usuarios(request: Request):
    return templates.TemplateResponse("usuarios/listarUsuarios.html", {"request": request})

@app.get("/users/update", response_class=HTMLResponse)
async def get_update_usuario(request: Request):
    return templates.TemplateResponse("usuarios/updateUsuario.html", {"request": request})

# Empleados
@app.get("/employees/register", response_class=HTMLResponse)
async def get_register_empleado(request: Request):
    return templates.TemplateResponse("usuarios/registrarUsuario.html", {"request": request})

@app.get("/employees/list", response_class=HTMLResponse)
async def get_listar_empleados(request: Request):
    return templates.TemplateResponse("usuarios/listarUsuarios.html", {"request": request})


# Incluir las rutas de los módulos
app.include_router(vehicles.router, prefix="/vehicles", tags=["Vehicles"])
app.include_router(users.router, prefix="/users", tags=["Usuarios"])
app.include_router(employees.router, prefix="/employees", tags=["Empleados"])
app.include_router(clients.router, prefix="/clients", tags=["Clientes"])
