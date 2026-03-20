import random
from datetime import datetime, timedelta
from app import create_app
from app.model import db
from database.models import PredictionHistory

def seed():
    app = create_app()
    with app.app_context():
        # Clear existing
        PredictionHistory.query.delete()
        
        dummy_statements = [
            ("The earth revolves around the sun.", "True", 99.5),
            ("Water is composed of hydrogen and oxygen.", "True", 98.2),
            ("The moon is made entirely of green cheese and mice.", "Fake", 95.7),
            ("Humans only use 10% of their brains.", "Fake", 88.4),
            ("Regular exercise improves cardiovascular health.", "True", 94.1),
            ("Drinking 8 glasses of bleach a day cures all diseases.", "Fake", 99.9),
            ("Python is a widely used high-level programming language.", "True", 92.3)
        ]
        
        print("Seeding database with history records...")
        
        now = datetime.utcnow()
        for i, (stmt, pred, conf) in enumerate(dummy_statements):
            record = PredictionHistory(
                statement=stmt,
                prediction=pred,
                confidence=conf,
                timestamp=now - timedelta(hours=i*2)
            )
            db.session.add(record)
            
        db.session.commit()
        print("Database seeded successfully with 7 records!")

if __name__ == "__main__":
    seed()
