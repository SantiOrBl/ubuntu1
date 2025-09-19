# pip install sqlmodel pymysql
# pip install sqlalchemy databases pymysql


from fastapi import FastAPI, Depends, Query, HTTPException
from sqlmodel import Field, Session, create_engine, select, SQLModel
from typing import Annotated, Optional
#conexion
url_connection = 'mysql+pymysql://aprendiz:Sena2025@localhost:3306/inventario'
engine = create_engine(url_connection)

def create_db_ant_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

session_dep = Annotated[Session, Depends(get_session)]

#creacion de modelos
#creacion de modelos
class ProductoBase(SQLModel):
    nombre: str = Field(min_length=3, max_length=30)
    cantidad: int
    descripcion: str = Field(min_length=3, max_length=100)
    id_categoria: int
    id_origen: int

class Producto(ProductoBase, table=True):
    id_producto: int = Field(default= None, primary_key=True)


class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(ProductoBase):
    nombre: Optional[str] = Field(default=None, min_length=3, max_length=30)
    cantidad: Optional[int] = None
    descripcion: Optional[str] = Field(default=None, min_length=5, max_length=100)

class ProductoPublic(ProductoBase):
    id_producto: int

#categoria
class CategoriaBase(SQLModel):
    nombre: str = Field(min_length=3, max_length=30)
    descripcion: str = Field(min_length=3, max_length=100)

class Categoria(CategoriaBase, table=True):
    id_categoria: int = Field(default= None, primary_key=True)

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaUpdate(CategoriaBase):
    nombre: Optional[str] = Field(default=None, min_length=3, max_length=30)
    descripcion: Optional[str] = Field(default=None, min_length=5, max_length=100)

class CategoriaPublic(CategoriaBase):
    id_categoria: int


# origen
class OrigenBase(SQLModel):
    nombre: str = Field(min_length=3, max_length=30)
    direccion: str = Field(min_length=3, max_length=100)

class Origen(OrigenBase, table=True):
    id_origen: int = Field(default= None, primary_key=True)

class OrigenCreate(OrigenBase):
    pass

class OrigenUpdate(OrigenBase):
    nombre: Optional[str] = Field(default=None, min_length=3, max_length=30)
    direccion: Optional[str] = Field(default=None, min_length=5, max_length=100)

class OrigenPublic(OrigenBase):
    id_origen: int

#rutas
app = FastAPI()

@app.get('/')
def root():
    return{'message':'Hello'}

@app.on_event('startup')
def on_startup():
    create_db_ant_tables()

@app.post("/producto/", response_model=ProductoPublic)
def create_producto(producto:ProductoCreate, session:session_dep): # type: ignore
    db_producto = Producto.model_validate(producto)
    session.add(db_producto)
    session.commit()
    session.refresh(db_producto)
    return db_producto

@app.post("/categoria/", response_model=CategoriaPublic)
def create_categoria(categoria:CategoriaCreate, session:session_dep): # type: ignore
    db_categoria = Categoria.model_validate(categoria)
    session.add(db_categoria)
    session.commit()
    session.refresh(db_categoria)
    return db_categoria

@app.post("/origen/", response_model=OrigenPublic)
def create_origen(origen:OrigenCreate, session:session_dep): # type: ignore
    db_origen = Categoria.model_validate(origen)
    session.add(db_origen)
    session.commit()
    session.refresh(db_origen)
    return db_origen



@app.get("/produtos/", response_model=list[ProductoPublic])
def read_prod(
    session:session_dep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    prods = session.exec(select(Producto).offset(offset).limit(limit)).all()
    return prods

@app.get("/productos/{prod_id}", response_model=ProductoPublic)
def read_prod(prod_id: int, session: session_dep):
    prod = session.get(Producto,prod_id)
    if not prod:
        raise HTTPException(status_code=404,detail='No se encontro')
    return prod

@app.patch("/productos/{prod_id}",response_model=ProductoPublic)
def update_prod(prod_id: int, prod: ProductoUpdate, session: session_dep):
    prod_db = session.get(Producto, prod_id)
    if not prod_db:
        raise HTTPException(status_code=404,detail='No se encontro')
    prod_data = Producto.model_dump(exclude_unset=True)
    prod_db.sqlmodel_update(prod_data)
    session.add(prod_db)
    session.commit()
    session.refresh(prod_db)
    return prod_db

@app.delete("/productos/{prod_id}")
def delete_prod(prod_id: int, session: session_dep):
    prod = session.get(Producto,prod_id)
    if not prod:
        raise HTTPException(status_code=404,detail="No se encontro")
    session.delete(prod)
    session.commit()
    return {"ok":True}