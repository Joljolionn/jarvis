from fastapi import APIRouter

import db

mobileRouter = APIRouter()


@mobileRouter.get("/all")
def get_all_items():
    with db._Session() as session:
        items = session.query(db.Item).all()
    return [db.ItemResponseDto.model_validate(item).model_dump() for item in items]


@mobileRouter.post("/add")
def add_new_item(new_item_title: db.ItemTitleRequestDto):
    new_item = db.Item()
    with db._Session() as session:
        new_item.name = new_item_title.title
        new_item.num = 1
        new_item.completed = False
        session.add(new_item)
        session.commit()
        session.refresh(new_item)
    return new_item


@mobileRouter.delete("/delete")
def delete_item(id: db.ItemIdRequestDto):
    rows_affected: int
    with db._Session() as session:
<<<<<<< HEAD
        rows_affected = session.query(db.Item).filter(db.Item.id == id.id).delete()
    return rows_affected == 1
=======
        query = session.query(db.Item).filter(db.Item.id == id.id)
        print(f"Tentando deletar item com ID: {id.id}")  # Veja se o ID bate
        rows_affected = query.delete()
        session.commit()
        print(f"Linhas afetadas: {rows_affected}")
    return {"success": rows_affected > 0, "rows": rows_affected}
>>>>>>> 4bcdf90 (fix: arrumando rota de delete para mobile)


@mobileRouter.patch("/increase")
def increase_item_num(id: db.ItemIdRequestDto):
    with db._Session() as session:
        item = session.query(db.Item).filter(db.Item.id == id.id).first()
        item.num += 1
        session.commit()
        session.refresh(item)
    return item

<<<<<<< HEAD
=======

>>>>>>> 4bcdf90 (fix: arrumando rota de delete para mobile)
@mobileRouter.patch("/decrease")
def decrease_item_num(id: db.ItemIdRequestDto):
    with db._Session() as session:
        item = session.query(db.Item).filter(db.Item.id == id.id).first()
<<<<<<< HEAD
        item.num = item.num-1 if item.num > 1 else item.num
=======
        item.num = item.num - 1 if item.num > 1 else item.num
>>>>>>> 4bcdf90 (fix: arrumando rota de delete para mobile)
        session.commit()
        session.refresh(item)
    return item

<<<<<<< HEAD
=======

>>>>>>> 4bcdf90 (fix: arrumando rota de delete para mobile)
@mobileRouter.patch("/completed")
def toggle_completed_item(id: db.ItemIdCompletedRequestDto):
    with db._Session() as session:
        item = session.query(db.Item).filter(db.Item.id == id.id).first()
        item.completed = id.completed
        session.commit()
        session.refresh(item)
<<<<<<< HEAD
    
=======
>>>>>>> 4bcdf90 (fix: arrumando rota de delete para mobile)
