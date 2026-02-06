from app.db import Base, engine, SessionLocal
from app.models import Employee

Base.metadata.create_all(bind=engine)

names = [
    "Olivier",
    "Dominic",
    "Marc-André",
    "Sabrina",
    "Jérôme",
    "Victor",
    "Samuel",
    "Quentin",
    "Carlos",
]

db = SessionLocal()
try:
    for n in names:
        if not db.query(Employee).filter(Employee.name == n).first():
            db.add(Employee(name=n, active=True))
    db.commit()
    print("Seed OK")
finally:
    db.close()
