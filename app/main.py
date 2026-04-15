from fastapi import FastAPI
from a2wsgi import WSGIMiddleware
from fastapi_pagination import add_pagination

from app.api.items import router as items_router
from app.db import Base, engine, SessionLocal
from app.models import ItemModel
from app.web import create_flask_app

app = FastAPI(title="Hybrid Flask + FastAPI")


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        has_items = db.query(ItemModel).first()
        if not has_items:
            db.add_all([
                ItemModel(name="Laptop", price=1200.0),
                ItemModel(name="Mouse", price=25.0),
            ])
            db.commit()
    finally:
        db.close()


app.include_router(items_router, prefix="/api")
add_pagination(app)

flask_app = create_flask_app()
app.mount("/", WSGIMiddleware(flask_app))