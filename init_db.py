from app import app, db
from models import User, Category, Budget, Expense
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

def init_db():
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Check if we already have users
        if User.query.count() == 0:
            print("Creating demo user...")
            # Create a demo user
            demo_user = User(
                username="demo",
                password_hash=generate_password_hash("demo123")
            )
            db.session.add(demo_user)
            db.session.commit()
            
            # Create some categories
            categories = [
                Category(name="Food", description="Groceries and eating out", user_id=demo_user.id),
                Category(name="Transportation", description="Gas, public transit, etc.", user_id=demo_user.id),
                Category(name="Entertainment", description="Movies, games, etc.", user_id=demo_user.id),
                Category(name="Utilities", description="Electricity, water, internet", user_id=demo_user.id)
            ]
            
            db.session.add_all(categories)
            db.session.commit()
            
            # Create some budgets
            today = datetime.now()
            month_start = today.replace(day=1)
            month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            
            budgets = [
                Budget(
                    name="Monthly Food",
                    amount=500.00,
                    start_date=month_start,
                    end_date=month_end,
                    category_id=categories[0].id,
                    user_id=demo_user.id
                ),
                Budget(
                    name="Monthly Transportation",
                    amount=200.00,
                    start_date=month_start,
                    end_date=month_end,
                    category_id=categories[1].id,
                    user_id=demo_user.id
                ),
                Budget(
                    name="Monthly Entertainment",
                    amount=100.00,
                    start_date=month_start,
                    end_date=month_end,
                    category_id=categories[2].id,
                    user_id=demo_user.id
                )
            ]
            
            db.session.add_all(budgets)
            db.session.commit()
            
            # Create some expenses
            expenses = [
                Expense(
                    description="Grocery shopping",
                    amount=75.50,
                    date=today - timedelta(days=5),
                    category_id=categories[0].id,
                    user_id=demo_user.id
                ),
                Expense(
                    description="Gas",
                    amount=45.00,
                    date=today - timedelta(days=3),
                    category_id=categories[1].id,
                    user_id=demo_user.id
                ),
                Expense(
                    description="Movie tickets",
                    amount=30.00,
                    date=today - timedelta(days=2),
                    category_id=categories[2].id,
                    user_id=demo_user.id
                ),
                Expense(
                    description="Internet bill",
                    amount=60.00,
                    date=today - timedelta(days=1),
                    category_id=categories[3].id,
                    user_id=demo_user.id
                )
            ]
            
            db.session.add_all(expenses)
            db.session.commit()
            
            print("Demo data created successfully!")
        else:
            print("Database already contains data. Skipping initialization.")

if __name__ == "__main__":
    init_db()
