from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Data file paths
USERS_FILE = 'data/users.txt'
ITEMS_FILE = 'data/items.txt'
ADMIN_FILE = 'data/admin.txt'

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

# Initialize admin file if it doesn't exist
if not os.path.exists(ADMIN_FILE):
    with open(ADMIN_FILE, 'w', encoding='utf-8') as f:
        f.write('admin:admin123\n')  # Default admin credentials

def read_users():
    """Read users from file"""
    users = {}
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if ':' in line:
                        parts = line.split(':', 1)
                        if len(parts) == 2:
                            username, password = parts
                            users[username] = password
        except Exception as e:
            print(f"Error reading users file: {e}")
    return users

def write_user(username, password):
    """Write new user to file"""
    try:
        # Ensure data directory exists
        os.makedirs('data', exist_ok=True)
        
        # Validate inputs
        if not username or not password:
            raise ValueError("Username and password cannot be empty")
        
        # Ensure username and password don't contain colons (our delimiter)
        if ':' in username:
            raise ValueError("Username cannot contain ':' character")
        if ':' in password:
            raise ValueError("Password cannot contain ':' character")
        
        with open(USERS_FILE, 'a', encoding='utf-8') as f:
            f.write(f'{username}:{password}\n')
            f.flush()  # Ensure data is written immediately
    except (IOError, OSError) as e:
        print(f"Error writing user to file: {e}")
        raise ValueError(f"Failed to save user data: {str(e)}")
    except Exception as e:
        print(f"Unexpected error writing user: {e}")
        raise

def read_admin():
    """Read admin credentials"""
    admin = {}
    if os.path.exists(ADMIN_FILE):
        try:
            with open(ADMIN_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if ':' in line:
                        parts = line.split(':', 1)
                        if len(parts) == 2:
                            username, password = parts
                            admin[username] = password
        except Exception as e:
            print(f"Error reading admin file: {e}")
    return admin

def read_items():
    """Read items from file"""
    items = []
    if os.path.exists(ITEMS_FILE):
        try:
            with open(ITEMS_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        parts = line.split('|')
                        if len(parts) >= 8:
                            items.append({
                                'id': parts[0],
                                'type': parts[1],  # 'found' or 'lost'
                                'item_name': parts[2],
                                'color': parts[3],
                                'location': parts[4],
                                'description': parts[5],
                                'reported_by': parts[6],
                                'status': parts[7],  # 'pending', 'approved', 'rejected'
                                'date': parts[8] if len(parts) > 8 else ''
                            })
        except Exception as e:
            print(f"Error reading items file: {e}")
    return items

def write_item(item):
    """Write new item to file"""
    try:
        item_id = str(len(read_items()) + 1)
        # Replace pipe characters in data to avoid conflicts
        item_name = str(item['item_name']).replace('|', '-')
        color = str(item['color']).replace('|', '-')
        location = str(item['location']).replace('|', '-')
        description = str(item['description']).replace('|', '-')
        reported_by = str(item['reported_by']).replace('|', '-')
        
        item_line = f"{item_id}|{item['type']}|{item_name}|{color}|{location}|{description}|{reported_by}|{item['status']}|{item['date']}\n"
        with open(ITEMS_FILE, 'a', encoding='utf-8') as f:
            f.write(item_line)
        return item_id
    except Exception as e:
        print(f"Error writing item to file: {e}")
        raise

def update_item_status(item_id, status):
    """Update item status"""
    try:
        items = read_items()
        updated_items = []
        for item in items:
            if item['id'] == item_id:
                item['status'] = status
            updated_items.append(item)
        
        # Rewrite all items
        with open(ITEMS_FILE, 'w', encoding='utf-8') as f:
            for item in updated_items:
                # Replace pipe characters to avoid conflicts
                item_name = str(item['item_name']).replace('|', '-')
                color = str(item['color']).replace('|', '-')
                location = str(item['location']).replace('|', '-')
                description = str(item['description']).replace('|', '-')
                reported_by = str(item['reported_by']).replace('|', '-')
                
                item_line = f"{item['id']}|{item['type']}|{item_name}|{color}|{location}|{description}|{reported_by}|{item['status']}|{item['date']}\n"
                f.write(item_line)
    except Exception as e:
        print(f"Error updating item status: {e}")
        raise

@app.route('/')
def index():
    """Home page with login, signup, and admin login options"""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        try:
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '').strip()
            
            if not username or not password:
                flash('Please enter both username and password', 'danger')
                return render_template('login.html')
            
            users = read_users()
            
            if username in users and users[username] == password:
                session['username'] = username
                session['user_type'] = 'user'
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password', 'danger')
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """User signup"""
    if request.method == 'POST':
        try:
            # Get form data safely
            username = request.form.get('username', '') or ''
            password = request.form.get('password', '') or ''
            confirm_password = request.form.get('confirm_password', '') or ''
            
            # Convert to string and strip (handle None values)
            username = str(username).strip() if username is not None else ''
            password = str(password).strip() if password is not None else ''
            confirm_password = str(confirm_password).strip() if confirm_password is not None else ''
            
            # Validate input
            if not username or not password or not confirm_password:
                flash('All fields are required', 'danger')
                return render_template('signup.html')
            
            if len(username) < 3:
                flash('Username must be at least 3 characters long', 'danger')
                return render_template('signup.html')
            
            if len(password) < 4:
                flash('Password must be at least 4 characters long', 'danger')
                return render_template('signup.html')
            
            if password != confirm_password:
                flash('Passwords do not match', 'danger')
                return render_template('signup.html')
            
            users = read_users()
            if username in users:
                flash('Username already exists', 'danger')
                return render_template('signup.html')
            
            write_user(username, password)
            flash('Account created successfully! Please login.', 'success')
            return redirect(url_for('login'))
        except ValueError as ve:
            flash(f'Invalid input: {str(ve)}', 'danger')
            return render_template('signup.html')
        except Exception as e:
            import traceback
            error_msg = f'An error occurred: {str(e)}'
            print(f"Signup error: {error_msg}")
            print(traceback.format_exc())
            flash(error_msg, 'danger')
            return render_template('signup.html')
    
    return render_template('signup.html')

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    """Admin login"""
    if request.method == 'POST':
        try:
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '').strip()
            
            if not username or not password:
                flash('Please enter both username and password', 'danger')
                return render_template('admin_login.html')
            
            admin = read_admin()
            
            if username in admin and admin[username] == password:
                session['username'] = username
                session['user_type'] = 'admin'
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Invalid admin credentials', 'danger')
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')
    
    return render_template('admin_login.html')

@app.route('/dashboard')
def dashboard():
    """User dashboard"""
    if 'username' not in session or session.get('user_type') != 'user':
        return redirect(url_for('login'))
    
    items = read_items()
    user_items = [item for item in items if item['reported_by'] == session['username']]
    
    return render_template('dashboard.html', username=session['username'], items=user_items)

@app.route('/admin_dashboard')
def admin_dashboard():
    """Admin dashboard"""
    if 'username' not in session or session.get('user_type') != 'admin':
        return redirect(url_for('admin_login'))
    
    items = read_items()
    pending_items = [item for item in items if item['status'] == 'pending']
    all_items = items
    
    return render_template('admin_dashboard.html', username=session['username'], 
                         pending_items=pending_items, all_items=all_items)

@app.route('/report_found', methods=['GET', 'POST'])
def report_found():
    """Report found item"""
    if 'username' not in session or session.get('user_type') != 'user':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            item_name = request.form.get('item_name', '').strip()
            color = request.form.get('color', '').strip()
            location = request.form.get('location', '').strip()
            description = request.form.get('description', '').strip()
            
            if not item_name or not color or not location:
                flash('Please fill in all required fields', 'danger')
                return render_template('report_found.html')
            
            item = {
                'type': 'found',
                'item_name': item_name,
                'color': color,
                'location': location,
                'description': description,
                'reported_by': session['username'],
                'status': 'pending',
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            write_item(item)
            flash('Found item reported successfully! Waiting for admin approval.', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')
            return render_template('report_found.html')
    
    return render_template('report_found.html')

@app.route('/report_lost', methods=['GET', 'POST'])
def report_lost():
    """Report lost item"""
    if 'username' not in session or session.get('user_type') != 'user':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            item_name = request.form.get('item_name', '').strip()
            color = request.form.get('color', '').strip()
            location = request.form.get('location', '').strip()
            description = request.form.get('description', '').strip()
            
            if not item_name or not color or not location:
                flash('Please fill in all required fields', 'danger')
                return render_template('report_lost.html')
            
            item = {
                'type': 'lost',
                'item_name': item_name,
                'color': color,
                'location': location,
                'description': description,
                'reported_by': session['username'],
                'status': 'pending',
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            write_item(item)
            flash('Lost item reported successfully! Waiting for admin approval.', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')
            return render_template('report_lost.html')
    
    return render_template('report_lost.html')

@app.route('/approve_item/<item_id>')
def approve_item(item_id):
    """Approve an item (admin only)"""
    if 'username' not in session or session.get('user_type') != 'admin':
        return redirect(url_for('admin_login'))
    
    update_item_status(item_id, 'approved')
    flash('Item approved successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/reject_item/<item_id>')
def reject_item(item_id):
    """Reject an item (admin only)"""
    if 'username' not in session or session.get('user_type') != 'admin':
        return redirect(url_for('admin_login'))
    
    update_item_status(item_id, 'rejected')
    flash('Item rejected.', 'info')
    return redirect(url_for('admin_dashboard'))

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    return redirect(url_for('index'))

@app.route('/browse_items')
def browse_items():
    """Browse all approved items"""
    items = read_items()
    approved_items = [item for item in items if item['status'] == 'approved']
    return render_template('browse_items.html', items=approved_items)

if __name__ == '__main__':
    app.run(debug=True)

