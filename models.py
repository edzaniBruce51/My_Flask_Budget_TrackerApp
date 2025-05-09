from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Stores user info (username, password)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)  
    
    # Relationships
    categories = db.relationship('Category', back_populates='user', lazy=True)
    expenses = db.relationship('Expense', back_populates='user', lazy=True)
    budgets = db.relationship('Budget', back_populates='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'

# Stores expense categories (Food, Transport, etc.)
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships
    user = db.relationship('User', back_populates='categories')
    expenses = db.relationship('Expense', back_populates='category', lazy=True)
    budgets = db.relationship('Budget', back_populates='category', lazy=True)
    
    def __repr__(self):
        return f'<Category {self.name}>'
    
    def get_total_expenses(self):
        """Returns the total expenses for this category"""
        from sqlalchemy import func
        result = db.session.query(func.sum(Expense.amount)).filter(
            Expense.category_id == self.id,
            Expense.user_id == self.user_id
        ).scalar()
        return result or 0

# Stores budget limits
class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships
    user = db.relationship('User', back_populates='budgets')
    category = db.relationship('Category', back_populates='budgets')
    
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
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships
    user = db.relationship('User', back_populates='expenses')
    category = db.relationship('Category', back_populates='expenses')
    
    def __repr__(self):
        return f'<Expense {self.description} (${self.amount} on {self.date})>'












