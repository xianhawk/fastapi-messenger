# uvicorn main:app
from fastapi import Depends, FastAPI, HTTPException, Response, Cookie, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import uvicorn
from database import SessionLocal, engine
import crud, models, schemas
from auth import AuthHandler

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")
templates = Jinja2Templates(directory="../frontend/templates")
auth_handler = AuthHandler()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

    
@app.get("/", response_class=RedirectResponse)
async def index(token: str | None = Cookie(None)):
    if not auth_handler.decode_token(token=token) or token is None:
        return RedirectResponse("/signup/")
    return RedirectResponse("/chat/")


@app.post("/signup/")
async def create_user(user: schemas.UserCreate,
                      db: Session = Depends(get_db)):
    db_user_email = crud.get_user_by_email(db, email=user.email)
    if db_user_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    crud.create_user(db=db, user=user)
    return {"detail": "ok"}


@app.get("/signin/", response_class=HTMLResponse)
async def signin(request: Request,
                token: str | None = Cookie(None)):
    if not auth_handler.decode_token(token=token) or token is None:
        return templates.TemplateResponse("signin.html", {"request": request})
    return RedirectResponse("/chat/")


@app.get("/chat/", response_class=HTMLResponse)
async def chat(request: Request,
                token: str | None = Cookie(None),
                db: Session = Depends(get_db)):
    if not auth_handler.decode_token(token=token) or token is None:
        return RedirectResponse("/signin/")
    user = crud.get_user_by_email(db=db, email=auth_handler.decode_token(token=token))
    return templates.TemplateResponse("chat.html", {"request": request, "user": user})


@app.get("/signup/", response_class=HTMLResponse)
async def signup(request: Request,
                token: str | None = Cookie(None)):
    if not auth_handler.decode_token(token=token) or token is None:
         return templates.TemplateResponse("signup.html", {"request": request})
    return RedirectResponse("/chat/")


@app.post("/token/")
async def get_token(response: Response,
                    user: schemas.UserLogin,
                    db: Session = Depends(get_db)):
    db_user_email = crud.get_user_by_email(db, email=user.email)
    db_user_hashed_password = crud.get_hashed_password_by_email(db=db, email=user.email)
    
    if (db_user_email is None) or (not auth_handler.verify_password(user.password, db_user_hashed_password)):
        raise HTTPException(status_code=400, detail='Invalid email and/or password')
    token = auth_handler.encode_token(user.email)
    response.set_cookie(key="token", value=token)
    return {"token": token}


@app.post("/logout/")
async def logout(response: Response):
    response.set_cookie(key="token", value="0")
    return {"logout": True}
    

@app.post("/sending-message/")
async def sending_message(message: schemas.MessageSend,
                          token: str | None = Cookie(None),
                          db: Session = Depends(get_db)):
    if not auth_handler.decode_token(token=token) or token is None:
        return {"detail": "error"}
    auth_email = auth_handler.decode_token(token=token)
    id_auth_user = crud.get_user_id_by_email(db, email=auth_email)
    db_recipient_user = crud.get_user_by_id(db, user_id=message.recipient_id)
    if not db_recipient_user:
        raise HTTPException(status_code=400, detail="Recipient user not found")
    return crud.sending_message(db=db, sender_id=id_auth_user, message=message)


@app.post("/get-messages/")
async def get_messages(recipient: schemas.MessageGet,
                       token: str | None = Cookie(None),
                       db: Session = Depends(get_db)):
    if not auth_handler.decode_token(token=token) or token is None:
        return {"detail": "error"}
    auth_email = auth_handler.decode_token(token=token)
    id_auth_user = crud.get_user_id_by_email(db, email=auth_email)
    return crud.get_messages(db=db, sender_id=id_auth_user, recipient_id=recipient.recipient_id)
    

@app.post("/search-contanct/")
async def search_contanct(data: schemas.ContactSearch,
               token: str | None = Cookie(None),
               db: Session = Depends(get_db)):
    if not auth_handler.decode_token(token=token) or token is None:
        return {"detail": "error"}
    email_contact = data.email
    db_contact = crud.get_user_by_email(db, email=email_contact)
    if not db_contact:
        raise HTTPException(status_code=400, detail="User not found") 
    return {"id_contact": db_contact.id, "username": db_contact.username}


@app.post("/add-contact/")
async def add_contact(contact: schemas.ContactAdd,
                      token: str | None = Cookie(None),
                      db: Session = Depends(get_db)):
    if not auth_handler.decode_token(token=token) or token is None:
        return {"detail": "error"}
    auth_email = auth_handler.decode_token(token=token)
    id_auth_user = crud.get_user_id_by_email(db, email=auth_email)
    return crud.add_contact(db=db, id_user=id_auth_user, contact=contact)


@app.post("/get-contacts/")
async def get_contacts(token: str | None = Cookie(None),
               db: Session = Depends(get_db)):
    if not auth_handler.decode_token(token=token) or token is None:
        return {"detail": "error"}
    auth_email = auth_handler.decode_token(token=token)
    id_auth_user = crud.get_user_id_by_email(db, email=auth_email)
    return crud.get_contacts_user_by_id(db=db, user_id=id_auth_user)


if __name__ == "__main__":
    uvicorn.run("main:app", log_level="info")