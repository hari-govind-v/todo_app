from sqlalchemy.orm import Session
from todo_app.users.models import User
from todo_app.tasks.models import UserTask
from todo_app.core.config import SessionLocal
from todo_app.auth.utils import hash_password
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import logging

def populate_db():
    db: Session = SessionLocal()
    try:
        if db.query(User).count() == 0:
            for i in range(1,6):
                user =  User(
                    username=f"dummyuser{i}",
                    hashed_password=hash_password(f"password{i}"),
                    age=25
                )

                db.add(user)
                db.flush()

                task = UserTask(
                    name="Welcome Task",
                    description="This is the first task",
                    status="pending",
                    user_id=user.id
                )
                db.add(task)
            db.commit()
            logging.info("Populated tables users and user_tasks.")
        else:
            logging.info("SKipping populate_users because users database is not empty.")
    except IntegrityError:
        db.rollback()
        logging.info("User already exists, skipping dummy user seed data.")
    except SQLAlchemyError as e:
        db.rollback()
        logging.error(e)
    finally:
        db.close()


def seed_data():
    populate_db()
    


