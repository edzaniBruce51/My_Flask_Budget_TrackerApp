from flask_login import UserMixin # (UserMixin) pre-made security badge system
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Stores user info (username, password)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False) #unique=True : Like a username on social media - everyone needs a unique one
    password_hash = db.Column(db.String(128), nullable=False)  
    
    # Relationships
    #Tells Flask: "Each user has their own category, expense, and budget folders
    #backref='user': Each category can look up who owns it
    #The lazy=True part means: "Don't load everything at once - wait until we actually need it" (saves memory and speed).
    #relationship is there to connect users with their categories. Without this relationship, managing categories for different users would be much more complicated!
    categories = db.relationship('Category', backref='user', lazy=True) 
    expenses = db.relationship('Expense', backref='user', lazy=True)
    budgets = db.relationship('Budget', backref='user', lazy=True)
    
    #The __repr__ function is like creating a name tag for your objects.
    def __repr__(self):
        return f'<User {self.username}>' # Shows for example: <User bruce>

# Stores expense categories (Food, Transport, etc.)
# Connected to specific users (user_id)
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships
    expenses = db.relationship('Expense', backref='category', lazy=True)
    budgets = db.relationship('Budget', backref='category', lazy=True)
    
    def __repr__(self):
        return f'<Category {self.name}>' #self refers to the specific category object being printed
    
    def get_total_expenses(self):
        """Returns the total expenses for this category"""
        from sqlalchemy import func
        result = db.session.query(func.sum(Expense.amount)).filter(
            Expense.category_id == self.id,
            Expense.user_id == self.user_id
        ).scalar() #We just want one number (the sum of expenses) unlike .all() .scalar(): Returns a single value
        return result or 0

# Stores budget limits
# Connected to categories and users
class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f'<Budget {self.name} ({self.start_date} to {self.end_date})>'
    
    def get_spent_amount(self):
        """Calculates total spent amount within budget period and category"""
        from sqlalchemy import func
        result = db.session.query(func.sum(Expense.amount)).filter(
            Expense.category_id == self.category_id,
            Expense.user_id == self.user_id,
            Expense.date >= self.start_date,
            Expense.date <= self.end_date
        ).scalar()
        return float(result) if result else 0.0
    
    def get_remaining_amount(self):
        """Calculates remaining budget amount"""
        return float(self.amount) - self.get_spent_amount()
    
    def get_percentage_used(self):
        """Calculates percentage of budget used"""
        amount = float(self.amount)
        if amount > 0:
            return (self.get_spent_amount() / amount) * 100
        return 0.0


# Stores actual expenses
# Connected to categories and users
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    date = db.Column(db.Date, nullable=False)  # This should be a Date type, not DateTime
    description = db.Column(db.String(200), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Add a relationship to Category to make it easier to access
    category = db.relationship('Category', backref='expenses')
    
    def __repr__(self):
        return f'<Expense {self.description} (${self.amount} on {self.date})>'



