from sqlalchemy.orm import Session
from auth import AuthHandler
import models, schemas

auth_handler = AuthHandler()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth_handler.get_password_hash(user.password)
    db_user = models.User(username=user.username,
                          email=user.email,
                          hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_hashed_password_by_email(db: Session, email: str):
    return db.query(models.User.hashed_password).filter(models.User.email == email).scalar()


def get_user_id_by_email(db: Session, email: str):
    return db.query(models.User.id).filter(models.User.email == email).scalar()


def sending_message(db: Session, sender_id: int, message: schemas.MessageSend):
    db_message = models.Message(text=message.text,
                                sender_id=sender_id,
                                recipient_id=message.recipient_id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def get_messages(db: Session, sender_id: int, recipient_id: int):
    return db.query(models.Message).filter((models.Message.sender_id==sender_id) & (models.Message.recipient_id==recipient_id) | (models.Message.recipient_id==sender_id) & (models.Message.sender_id==recipient_id)).order_by(models.Message.id.desc()).all()


def add_contact(db: Session, id_user: int, contact: schemas.Contact):
    db_contact = models.Contact(user_id=id_user,
                                contact_user_id=contact.contact_user_id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def get_contacts_user_by_id(db: Session, user_id: int):
    return db.query(models.User.username, models.Contact.contact_user_id, models.Contact.date_of_addition).filter(models.Contact.contact_user_id==models.User.id).filter(models.Contact.user_id==user_id).all()
