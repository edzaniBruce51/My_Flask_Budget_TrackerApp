# Personal Budget Tracker (Flask Version)

A Flask-based personal budget tracking system that helps users track expenses, manage budgets, and analyze spending patterns.

## Features

- Expense tracking with categorization
- Budget management with progress monitoring
- Monthly spending analysis with charts
- User authentication and data isolation
- Responsive dashboard interface

## Technical Stack

- Flask 2.3.3
- SQLAlchemy for database ORM
- SQLite database for simplicity
- Flask-Login for user authentication
- Chart.js for data visualization
- Responsive CSS design

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate     # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python app.py
   ```
5. Access the application at http://localhost:5000

## Project Structure

- `app.py`: Main application file
- `models.py`: Database models
- `forms.py`: Form definitions
- `routes.py`: Application routes
- `templates/`: HTML templates
- `static/`: Static files (CSS, JavaScript)

## Usage

1. Register a new account
2. Create categories for your expenses
3. Add budgets for different categories
4. Track your expenses
5. View your financial data on the dashboard

## Security Considerations

- User data is isolated through user-specific queries
- Password hashing for secure authentication
- CSRF protection enabled
- Secret key managed through environment variables
