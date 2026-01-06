from fastapi import FastAPI, Form, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import db
import requests
import json

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def get_root(request: Request, response: Response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    items = []
    print("Atualizando página")
    with db._Session() as session:
        items = session.query(db.Item).all()
        for item in items:
            print(f"{item.name} - {item.completed}")
    print("Página atualizada")
    return templates.TemplateResponse(
        "pages/listPage.html",
        {"request": request, "items": items, "itemslength": len(items)},
    )


@app.get("/message", response_class=HTMLResponse)
async def get_message(request: Request):
    res = requests.get("https://api-random.vercel.app/")
    message = json.loads(res.text)

    return templates.TemplateResponse(
        "pages/messagePage.html", {"request": request, "message": message["mensage"]}
    )


@app.delete("/item/{id}", response_class=HTMLResponse)
async def delete_item(id: int, request: Request):
    with db._Session() as session:
        item = session.query(db.Item).filter(db.Item.id == id).first()
        if item:
            session.delete(item)
            session.commit()
        items = session.query(db.Item).all()
    return templates.TemplateResponse(
        "components/itemsList.html",
        {"request": request, "items": items, "itemslength": len(items)},
    )


@app.post("/item/{id}/increase", response_class=HTMLResponse)
async def increse_item_quantity(id: int, request: Request):
    item: db.Item
    with db._Session() as session:
        item = session.query(db.Item).filter(db.Item.id == id).first()
        item.num += 1
        session.commit()
        session.refresh(item)
        return templates.TemplateResponse(
            "components/item.html", {"request": request, "item": item}
        )


@app.post("/item/{id}/decrease", response_class=HTMLResponse)
async def decrese_item_quantity(id: int, request: Request):
    item: db.Item
    with db._Session() as session:
        item = session.query(db.Item).filter(db.Item.id == id).first()
        if item.num == 1:
            return templates.TemplateResponse(
                "components/item.html", {"request": request, "item": item}
            )
        item.num -= 1
        session.commit()
        session.refresh(item)
    return templates.TemplateResponse(
        "components/item.html", {"request": request, "item": item}
    )


@app.post("/item/{id}/completed", response_class=HTMLResponse)
async def toggle_completed_item(
    id: int, request: Request, completed: bool = Form(False)
):
    with db._Session() as session:
        item = session.query(db.Item).filter(db.Item.id == id).first()
        if item:
            item.completed = completed
            session.commit()
            session.refresh(item)
            print(f"Salvo no DB: {item.name} - {item.completed}")

        return templates.TemplateResponse(
            "components/item.html", {"request": request, "item": item}
        )

@app.post("/item", response_class=HTMLResponse)
async def add_new_item(request: Request, name: str = Form("")):
    name = name.strip()
    if not name:
        # Retorna 204 para o HTMX entender que não há nada para atualizar
        return Response(status_code=204)

    with db._Session() as session:
        item = db.Item()
        item.name = name
        item.completed = False
        item.num = 1
        session.add(item)
        session.commit()
        session.refresh(item) 

    return templates.TemplateResponse(
        "components/item.html", {"request": request, "item": item}
    )
