import logging
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from todo_app.core.config import SessionLocal
from todo_app.auth.utils import hash_password
from todo_app.users.models import User
from todo_app.tasks.models import UserTask

logging.basicConfig(level=logging.INFO)

def populate_db():
    db: Session = SessionLocal()

    # Acquire advisory lock to prevent concurrent seeding
    db.execute("SELECT pg_advisory_lock(12345)")

    try:
        for i in range(1, 6):
            username = f"dummyuser{i}"
            existing_user = db.query(User).filter_by(username=username).first()

            if existing_user:
                logging.info(f"User {username} already exists, skipping...")
                continue

            user = User(
                username=username,
                hashed_password=hash_password(f"password{i}"),
                age=25
            )
            db.add(user)
            db.flush()  # Assigns user.id

            task = UserTask(
                name="Welcome Task",
                description="This is the first task",
                status="pending",
                user_id=user.id
            )
            db.add(task)

        db.commit()
        logging.info("Finished populating users and user_tasks.")

    except IntegrityError:
        db.rollback()
        logging.info("IntegrityError occurred during seeding.")
    except SQLAlchemyError as e:
        db.rollback()
        logging.error(f"Database error during seeding: {e}")
    finally:
        db.execute("SELECT pg_advisory_unlock(12345)")
        db.close()


if __name__ == "__main__":
    populate_db()
