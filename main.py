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

# Page endpoints

@app.get("/list", response_class=HTMLResponse)
async def get_list_page(request: Request):
    items = []
    with db._Session() as session:
        items = session.query(db.Item).all()
    return templates.TemplateResponse(
        "pages/list.html",
        {"request": request, "items": items, "itemslength": len(items)},
    )


@app.get("/message", response_class=HTMLResponse)
async def get_message_page(request: Request):
    res = requests.get("https://api-random.vercel.app/")
    message = json.loads(res.text)

    return templates.TemplateResponse(
        "pages/message.html", {"request": request, "message": message["mensage"]}
    )


# Component endpoints

@app.delete("/list/item/{id}", response_class=HTMLResponse)
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

@app.post("/list/item/{id}/increase", response_class=HTMLResponse)
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

@app.post("/list/item/{id}/decrease", response_class=HTMLResponse)
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

@app.post("/list/item/{id}/completed", response_class=HTMLResponse)
async def toggle_completed_item(
    id: int, request: Request, completed: bool = Form(False)
):
    with db._Session() as session:
        item = session.query(db.Item).filter(db.Item.id == id).first()
        if item:
            item.completed = completed
            session.commit()
            session.refresh(item)

        return templates.TemplateResponse(
            "components/item.html", {"request": request, "item": item}
        )

@app.post("/list/item", response_class=HTMLResponse)
async def add_new_item(request: Request, name: str = Form("")):
    name = name.strip()
    if not name:
        # Retorna 204 para o HTMX entender que não há nada para atualizar
        return Response(status_code=204)

    items: list(db.Item)
    with db._Session() as session:
        item = db.Item()
        item.name = name
        item.completed = False
        item.num = 1
        session.add(item)
        session.commit()
        session.refresh(item)
        items = session.query(db.Item).all()

    return templates.TemplateResponse(
            "components/itemsList.html", {"request": request, "items": items, "itemslength": len(items)}
    )

@app.get("/list/item/search", response_class=HTMLResponse)
async def search_item_list(request: Request, status: str = "all", search: str = ""):
    with db._Session() as session:
        items_query = session.query(db.Item)
        if status == "completed":
            items_query = session.query(db.Item).filter(db.Item.completed == True)
        elif status == "pending":
            items_query = session.query(db.Item).filter(db.Item.completed == False)

        if search:
            items_query = items_query.filter(db.Item.name.contains(search))

        items = items_query.all()

        return templates.TemplateResponse(
            "/components/itemsList.html",
            {"request": request, "items": items, "itemslength": len(items)},
        )
