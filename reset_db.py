from app import app, db, User
from werkzeug.security import generate_password_hash
from datetime import datetime

def reset_database():
    with app.app_context():
        db.drop_all()
        db.create_all()
        admin = User(username='admin', email='admin@gmail.com',
                     password_hash=generate_password_hash('admin123'), role='ADMIN')
        db.session.add(admin)
        db.session.commit()
        print(f"[{datetime.utcnow()}] Database reset complete. Default admin created.")

if __name__=='__main__':
    reset_database()
