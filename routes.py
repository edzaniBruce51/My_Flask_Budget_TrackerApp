from app import app, db
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Category, Budget, Expense
from forms import LoginForm, RegistrationForm, ExpenseForm, BudgetForm, CategoryForm
from datetime import datetime, timedelta
import json

# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm() 
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Login unsuccessful. Please check username and password', 'error')
    
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

# Dashboard route
@app.route('/')
@login_required
def dashboard():
    # Get current month's date range
    today = datetime.now()
    month_start = today.replace(day=1)
    month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    
    # Get last 30 days for trend chart
    thirty_days_ago = today - timedelta(days=30)
    
    # Get monthly expenses
    monthly_expenses = Expense.query.filter(
        Expense.user_id == current_user.id,
        Expense.date >= month_start,
        Expense.date <= month_end
    ).all()
    
    # Calculate total expenses for the month
    total_expenses = sum(float(expense.amount) for expense in monthly_expenses)
    
    # Get recent expenses
    recent_expenses = Expense.query.filter_by(
        user_id=current_user.id
    ).order_by(Expense.date.desc()).limit(5).all()    #.all() doesn't mean “get everything in the table” — it means “fetch all the results that match the query you've built up so far
    
    # Get active budgets
    active_budgets = Budget.query.filter(
        Budget.user_id == current_user.id,
        Budget.start_date <= today,
        Budget.end_date >= today
    ).all()
    
    # Prepare budget data | Prepare budget data for chart
    budget_names = [budget.name for budget in active_budgets]
    budget_amounts = [float(budget.amount) for budget in active_budgets]
    spent_amounts = [budget.get_spent_amount() for budget in active_budgets]
    
    # Get category expenses for the month
    expenses_by_category = db.session.query(
        Category.name,
        db.func.sum(Expense.amount).label('total')
    ).join(Expense).filter(
        Expense.user_id == current_user.id,
        Expense.date >= month_start,
        Expense.date <= month_end
    ).group_by(Category.name).all()
    
    category_names = [item[0] for item in expenses_by_category]
    category_amounts = [float(item[1]) for item in expenses_by_category]
    
    # Get expense trend data
    expense_trend = db.session.query(
        Expense.date,
        db.func.sum(Expense.amount).label('daily_total')
    ).filter(
        Expense.user_id == current_user.id,
        Expense.date >= thirty_days_ago,
        Expense.date <= today
    ).group_by(Expense.date).order_by(Expense.date).all()
    
    trend_dates = [item[0].strftime('%Y-%m-%d') for item in expense_trend]
    trend_amounts = [float(item[1]) for item in expense_trend]
    
    return render_template(
        'dashboard.html',
        total_expenses=total_expenses,
        recent_expenses=recent_expenses,
        active_budgets=active_budgets,
        expenses_by_category=expenses_by_category,
        budget_names_json=json.dumps(budget_names),
        budget_amounts_json=json.dumps(budget_amounts),
        spent_amounts_json=json.dumps(spent_amounts),
        category_names_json=json.dumps(category_names),
        category_amounts_json=json.dumps(category_amounts),
        trend_dates_json=json.dumps(trend_dates),
        trend_amounts_json=json.dumps(trend_amounts)
    )

# Expense routes
@app.route('/expenses')
@login_required
def expense_list():
    expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.date.desc()).all()
    return render_template('expense_list.html', expenses=expenses)

@app.route('/expenses/add', methods=['GET', 'POST'])
@login_required
def expense_create():
    form = ExpenseForm()
    
    # Populate category choices
    form.category.choices = [(c.id, c.name) for c in Category.query.filter_by(user_id=current_user.id).all()]
    
    if form.validate_on_submit():
        expense = Expense(
            description=form.description.data,
            amount=form.amount.data,
            date=form.date.data,
            category_id=form.category.data,
            user_id=current_user.id
        )
        db.session.add(expense)
        db.session.commit()
        flash('Expense added successfully!', 'success')
        return redirect(url_for('expense_list'))
    
    return render_template('expense_form.html', form=form)

@app.route('/expenses/edit/<int:expense_id>', methods=['GET', 'POST'])
@login_required
def expense_edit(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    
    # Check if the expense belongs to the current user
    if expense.user_id != current_user.id:
        flash('You do not have permission to edit this expense', 'error')
        return redirect(url_for('expense_list'))
    
    form = ExpenseForm()
    
    # Populate category choices
    form.category.choices = [(c.id, c.name) for c in Category.query.filter_by(user_id=current_user.id).all()]
    
    if form.validate_on_submit():
        expense.description = form.description.data
        expense.amount = form.amount.data
        expense.date = form.date.data
        expense.category_id = form.category.data
        db.session.commit()
        flash('Expense updated successfully!', 'success')
        return redirect(url_for('expense_list'))
    elif request.method == 'GET':
        form.description.data = expense.description
        form.amount.data = expense.amount
        form.date.data = expense.date
        form.category.data = expense.category_id
    
    return render_template('expense_form.html', form=form, expense=expense)

@app.route('/expenses/delete/<int:expense_id>', methods=['GET', 'POST'])
@login_required
def expense_delete(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    
    # Check if the expense belongs to the current user
    if expense.user_id != current_user.id:
        flash('You do not have permission to delete this expense', 'error')
        return redirect(url_for('expense_list'))
    
    if request.method == 'POST':
        db.session.delete(expense)
        db.session.commit()
        flash('Expense deleted successfully!', 'success')
        return redirect(url_for('expense_list'))
    
    return render_template('expense_confirm_delete.html', expense=expense)

# Budget routes
@app.route('/budgets')
@login_required
def budget_list():
    budgets = Budget.query.filter_by(user_id=current_user.id).order_by(Budget.start_date.desc()).all()
    return render_template('budget_list.html', budgets=budgets)

@app.route('/budgets/add', methods=['GET', 'POST'])
@login_required
def budget_create():
    form = BudgetForm()
    
    # Populate category choices
    form.category.choices = [(c.id, c.name) for c in Category.query.filter_by(user_id=current_user.id).all()]
    
    if form.validate_on_submit():
        budget = Budget(
            name=form.name.data,
            amount=form.amount.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            category_id=form.category.data,
            user_id=current_user.id
        )
        db.session.add(budget)
        db.session.commit()
        flash('Budget created successfully!', 'success')
        return redirect(url_for('budget_list'))
    
    return render_template('budget_form.html', form=form)

@app.route('/budgets/edit/<int:budget_id>', methods=['GET', 'POST'])
@login_required
def budget_edit(budget_id):
    budget = Budget.query.get_or_404(budget_id)
    
    # Check if the budget belongs to the current user
    if budget.user_id != current_user.id:
        flash('You do not have permission to edit this budget', 'error')
        return redirect(url_for('budget_list'))
    
    form = BudgetForm()
    
    # Populate category choices
    form.category.choices = [(c.id, c.name) for c in Category.query.filter_by(user_id=current_user.id).all()]
    
    if form.validate_on_submit():
        budget.name = form.name.data
        budget.amount = form.amount.data
        budget.start_date = form.start_date.data
        budget.end_date = form.end_date.data
        budget.category_id = form.category.data
        db.session.commit()
        flash('Budget updated successfully!', 'success')
        return redirect(url_for('budget_list'))
    elif request.method == 'GET':
        form.name.data = budget.name
        form.amount.data = budget.amount
        form.start_date.data = budget.start_date
        form.end_date.data = budget.end_date
        form.category.data = budget.category_id
    
    return render_template('budget_form.html', form=form, budget=budget)

@app.route('/budgets/delete/<int:budget_id>', methods=['GET', 'POST'])
@login_required
def budget_delete(budget_id):
    budget = Budget.query.get_or_404(budget_id)
    
    # Check if the budget belongs to the current user
    if budget.user_id != current_user.id:
        flash('You do not have permission to delete this budget', 'error')
        return redirect(url_for('budget_list'))
    
    if request.method == 'POST':
        db.session.delete(budget)
        db.session.commit()
        flash('Budget deleted successfully!', 'success')
        return redirect(url_for('budget_list'))
    
    return render_template('budget_confirm_delete.html', budget=budget)

# Category routes
@app.route('/categories')
@login_required
def category_list():
    categories = Category.query.filter_by(user_id=current_user.id).order_by(Category.name).all()
    return render_template('category_list.html', categories=categories)

@app.route('/categories/add', methods=['GET', 'POST'])
@login_required
def category_create():
    form = CategoryForm()
    
    if form.validate_on_submit():
        category = Category(
            name=form.name.data,
            description=form.description.data,
            user_id=current_user.id
        )
        db.session.add(category)
        db.session.commit()
        flash('Category created successfully!', 'success')
        return redirect(url_for('category_list'))
    
    return render_template('category_form.html', form=form)

@app.route('/categories/edit/<int:category_id>', methods=['GET', 'POST'])
@login_required
def category_edit(category_id):
    category = Category.query.get_or_404(category_id)
    
    # Check if the category belongs to the current user
    if category.user_id != current_user.id:
        flash('You do not have permission to edit this category', 'error')
        return redirect(url_for('category_list'))
    
    form = CategoryForm()
    
    if form.validate_on_submit():
        category.name = form.name.data
        category.description = form.description.data
        db.session.commit()
        flash('Category updated successfully!', 'success')
        return redirect(url_for('category_list'))
    elif request.method == 'GET':
        form.name.data = category.name
        form.description.data = category.description
    
    return render_template('category_form.html', form=form, category=category)

@app.route('/categories/delete/<int:category_id>', methods=['GET', 'POST'])
@login_required
def category_delete(category_id):
    category = Category.query.get_or_404(category_id)
    
    # Check if the category belongs to the current user
    if category.user_id != current_user.id:
        flash('You do not have permission to delete this category', 'error')
        return redirect(url_for('category_list'))
    
    # Check if the category is being used by any expenses or budgets
    if Expense.query.filter_by(category_id=category_id).first() or Budget.query.filter_by(category_id=category_id).first():
        flash('Cannot delete category because it is being used by expenses or budgets', 'error')
        return redirect(url_for('category_list'))
    
    if request.method == 'POST':
        db.session.delete(category)
        db.session.commit()
        flash('Category deleted successfully!', 'success')
        return redirect(url_for('category_list'))
    
    return render_template('category_confirm_delete.html', category=category)



