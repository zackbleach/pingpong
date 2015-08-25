from app import manager, db


@manager.command
def create_db():
    db.create_all()


if __name__ == '__main__':
    manager.run()
