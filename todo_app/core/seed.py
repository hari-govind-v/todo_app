import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import text
import sys
from todo_app.users.models import User
from todo_app.tasks.models import UserTask
from todo_app.core.config import SessionLocal
from todo_app.auth.utils import hash_password

logging.basicConfig(level=logging.INFO)
ADVISORY_LOCK_KEY = 12345

def populate_db():
    db: Session = SessionLocal()

    db.execute(text(f"SELECT pg_advisory_lock({ADVISORY_LOCK_KEY})"))

    try:
        user_count = db.query(User).count()
        if user_count == 0:
            for i in range(1, 6):
                user = User(
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
            logging.info("Populated tables 'users' and 'user_tasks'.")
        else:
            logging.info("ℹUsers already exist. Skipping seeding.")
    except IntegrityError as e:
        db.rollback()
        logging.warning(f"Integrity error during seeding: {e}")
    except SQLAlchemyError as e:
        db.rollback()
        logging.error(f"Database error during seeding: {e}")
    finally:
        db.execute(text(f"SELECT pg_advisory_unlock({ADVISORY_LOCK_KEY})"))
        db.close()

def seed_data():
    populate_db()

if __name__ == "__main__":
    try:
        seed_data()
        sys.exit(0)
    except Exception as e:
        logging.error(f"Seeding failed: {e}")
        sys.exit(1)
