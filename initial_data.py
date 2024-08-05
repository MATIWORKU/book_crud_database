from sqlalchemy.orm import Session
from database_postgres import engine, sessionLocal
from models import Role, User, Base


Base.metadata.create_all(bind=engine)


def create_default_roles(db: Session):
    roles = [
        Role(name='admin', permissions="read, write, delete"),
        Role(name='user', permissions="read, write"),
        Role(name='guest', permissions="read"),
    ]
    for role in roles:
        db.add(role)
    db.commit()


def main():
    db = sessionLocal()
    create_default_roles(db)
    db.close()


if __name__ == '__main__':
    main()