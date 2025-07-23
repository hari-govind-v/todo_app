from sqlalchemy.orm import Session
from todo_app.users.models import User
from todo_app.tasks.models import UserTask
from todo_app.core.config import SessionLocal
from todo_app.auth.utils import hash_password
from sqlalchemy.exc import SQLAlchemyError

def populate_db():
    db: Session = SessionLocal()
    try:
        if db.query(User).count() == 0:
            for i in range(1,6):
                username = f"dummyuser{i}"
                password = f"password{i}"
                hashed_password = hash_password(password)
                user =  User(
                    username=username,
                    hashed_password=hashed_password,
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
            print("Populated tables users and user_tasks.")
        else:
            print("SKipping populate_users because users database is not empty.")
    except SQLAlchemyError:
        print("Populating Users table failed.")
    finally:
        db.close()


def seed_data():
    populate_db()
    


