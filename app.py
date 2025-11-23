# ======================= MEMBER 1: LOGIN + SIGNUP + UI =======================
# This full app.py contains humanized comments explaining which member made
# which module. Comments also describe what each part of the code does.

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import os
import json
from datetime import datetime
from collections import Counter

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# ---------------------- Common Data Files (Shared Module) ---------------------
# These files store users, items, and admin credentials. All team members rely on these.
USERS_FILE = 'data/users.txt'
ITEMS_FILE = 'data/items.txt'
ADMIN_FILE = 'data/admin.txt'

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

# Initialize admin file if missing (default admin credentials)
if not os.path.exists(ADMIN_FILE):
    with open(ADMIN_FILE, 'w', encoding='utf-8') as f:
        f.write('admin:admin123\n')

# ======================== MEMBER 1: LOGIN + SIGNUP ===========================

def read_users():
    """Member 1: Reads user accounts from file."""
    users = {}
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', encoding='utf-8') as f:#encodeing utf means hwo to read and write properly(standard encoding that supports all languages)
            for line in f:
                line = line.strip()#removes unwanted sapces
                if ':' in line:
                    username, password = line.split(':', 1)
                    users[username] = password
    return users

def write_user(username, password):
    """Member 1: Saves a new user to file."""
    with open(USERS_FILE, 'a', encoding='utf-8') as f:
        f.write(f'{username}:{password}\n')


def read_admin():
    """Reads admin credentials from admin file."""
    admin = {}
    with open(ADMIN_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if ':' in line:
                username, password = line.split(':', 1)
                admin[username] = password
    return admin

# ======================== MEMBER 3 & 4: ITEMS MODULE =========================
# Member 3 → Lost Item Module
# Member 4 → Found Item Module
# Both rely on shared item reading/writing utilities.


def read_items():
    """Reads all lost + found items from file."""
    items = []
    if os.path.exists(ITEMS_FILE):
        with open(ITEMS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) >= 8:
                    item = {
                        'id': parts[0],
                        'type': parts[1],      # 'lost' or 'found'
                        'item_name': parts[2],
                        'color': parts[3],
                        'location': parts[4],
                        'description': parts[5],
                        'reported_by': parts[6],
                        'status': parts[7],     # 'pending', 'approved', 'rejected'
                        'date': parts[8] if len(parts) > 8 else '',
                        'category': parts[9] if len(parts) > 9 else 'other',
                        'contact': parts[10] if len(parts) > 10 else ''
                    }
                    items.append(item)
    return items


def write_item(item):
    """Writes a new item (lost or found) to file. (Used by Member 3 & 4)"""
    items = read_items()
    item_id = str(len(items) + 1)
    category = item.get('category', 'other')
    contact = item.get('contact', '')
    with open(ITEMS_FILE, 'a', encoding='utf-8') as f:
        line = f"{item_id}|{item['type']}|{item['item_name']}|{item['color']}|{item['location']}|{item['description']}|{item['reported_by']}|{item['status']}|{item['date']}|{category}|{contact}\n"
        f.write(line)
    return item_id

def delete_item(item_id):
    """Deletes an item from the file."""
    items = read_items()
    items = [i for i in items if i['id'] != item_id]
    with open(ITEMS_FILE, 'w', encoding='utf-8') as f:
        for item in items:
            category = item.get('category', 'other')
            contact = item.get('contact', '')
            line = f"{item['id']}|{item['type']}|{item['item_name']}|{item['color']}|{item['location']}|{item['description']}|{item['reported_by']}|{item['status']}|{item['date']}|{category}|{contact}\n"
            f.write(line)

def get_statistics():
    """Returns statistics for admin dashboard."""
    items = read_items()
    stats = {
        'total': len(items),
        'pending': len([i for i in items if i['status'] == 'pending']),
        'approved': len([i for i in items if i['status'] == 'approved']),
        'rejected': len([i for i in items if i['status'] == 'rejected']),
        'lost': len([i for i in items if i['type'] == 'lost']),
        'found': len([i for i in items if i['type'] == 'found']),
        'by_category': dict(Counter([i.get('category', 'other') for i in items])),
        'recent_items': sorted(items, key=lambda x: x['date'], reverse=True)[:5]
    }
    return stats

def find_matching_items(item):
    """Finds potential matches for a lost/found item."""
    items = read_items()
    matches = []
    search_type = 'found' if item['type'] == 'lost' else 'lost'
    
    for other_item in items:
        if (other_item['type'] == search_type and 
            other_item['status'] == 'approved' and
            other_item['id'] != item.get('id', '')):
            score = 0
            # Match by item name
            if item['item_name'].lower() in other_item['item_name'].lower() or \
               other_item['item_name'].lower() in item['item_name'].lower():
                score += 3
            # Match by color
            if item['color'].lower() in other_item['color'].lower() or \
               other_item['color'].lower() in item['color'].lower():
                score += 2
            # Match by location
            if item['location'].lower() in other_item['location'].lower() or \
               other_item['location'].lower() in item['location'].lower():
                score += 1
            # Match by description keywords
            if item.get('description') and other_item.get('description'):
                desc1_words = set(item['description'].lower().split())
                desc2_words = set(other_item['description'].lower().split())
                common_words = desc1_words.intersection(desc2_words)
                score += len(common_words) * 0.5
            
            if score > 0:
                other_item['match_score'] = score
                matches.append(other_item)
    
    return sorted(matches, key=lambda x: x['match_score'], reverse=True)[:5]


def update_item_status(item_id, status):
    """Updates item approval status. Used by Admin (Member 2)."""
    items = read_items()
    with open(ITEMS_FILE, 'w', encoding='utf-8') as f:
        for item in items:
            if item['id'] == item_id:
                item['status'] = status
            category = item.get('category', 'other')
            contact = item.get('contact', '')
            line = f"{item['id']}|{item['type']}|{item['item_name']}|{item['color']}|{item['location']}|{item['description']}|{item['reported_by']}|{item['status']}|{item['date']}|{category}|{contact}\n"
            f.write(line)

# =========================== ROUTES START ===================================

@app.route('/')
def index():
    """Home page made by Member 1."""
    return render_template('index.html')

# -------------------------- MEMBER 1: LOGIN ----------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users = read_users()
        if username in users and users[username] == password:
            session['username'] = username
            session['user_type'] = 'user'
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')

# -------------------------- MEMBER 1: SIGNUP ----------------------------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handles user account creation."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm_password']

        if password != confirm:
            flash('Passwords do not match', 'danger')
            return render_template('signup.html')

        users = read_users()
        if username in users:
            flash('Username already exists', 'danger')
            return render_template('signup.html')

        write_user(username, password)
        flash('Signup successful! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

# ========================== MEMBER 2: ADMIN PANEL ============================
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    """Admin login (Member 2)"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = read_admin()

        if username in admin and admin[username] == password:
            session['username'] = username
            session['user_type'] = 'admin'
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid admin credentials', 'danger')

    return render_template('admin_login.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    """Admin dashboard showing pending items (Member 2)."""
    if session.get('user_type') != 'admin':
        return redirect(url_for('admin_login'))

    items = read_items()
    pending_items = [i for i in items if i['status'] == 'pending']
    stats = get_statistics()
    
    # Filter parameters
    filter_type = request.args.get('type', 'all')
    filter_status = request.args.get('status', 'all')
    search_query = request.args.get('search', '').lower()
    
    filtered_items = items
    if filter_type != 'all':
        filtered_items = [i for i in filtered_items if i['type'] == filter_type]
    if filter_status != 'all':
        filtered_items = [i for i in filtered_items if i['status'] == filter_status]
    if search_query:
        filtered_items = [i for i in filtered_items if 
                         search_query in i['item_name'].lower() or 
                         search_query in i['location'].lower() or 
                         search_query in i.get('description', '').lower()]

    return render_template('admin_dashboard.html', 
                         pending_items=pending_items, 
                         all_items=filtered_items,
                         stats=stats,
                         filter_type=filter_type,
                         filter_status=filter_status,
                         search_query=search_query)

@app.route('/approve_item/<item_id>')
def approve_item(item_id):
    """Admin approves an item."""
    if session.get('user_type') != 'admin':
        return redirect(url_for('admin_login'))
    update_item_status(item_id, 'approved')
    flash('Item approved successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/reject_item/<item_id>')
def reject_item(item_id):
    """Admin rejects an item."""
    if session.get('user_type') != 'admin':
        return redirect(url_for('admin_login'))
    update_item_status(item_id, 'rejected')
    flash('Item rejected.', 'info')
    return redirect(url_for('admin_dashboard'))

@app.route('/delete_item/<item_id>')
def delete_item_route(item_id):
    """Admin deletes an item."""
    if session.get('user_type') != 'admin':
        return redirect(url_for('admin_login'))
    delete_item(item_id)
    flash('Item deleted successfully.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/api/statistics')
def api_statistics():
    """API endpoint for statistics."""
    if session.get('user_type') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    return jsonify(get_statistics())

@app.route('/api/search')
def api_search():
    """API endpoint for searching items."""
    query = request.args.get('q', '').lower()
    item_type = request.args.get('type', 'all')
    category = request.args.get('category', 'all')
    
    items = read_items()
    approved = [i for i in items if i['status'] == 'approved']
    
    if item_type != 'all':
        approved = [i for i in approved if i['type'] == item_type]
    if category != 'all':
        approved = [i for i in approved if i.get('category', 'other') == category]
    if query:
        approved = [i for i in approved if 
                   query in i['item_name'].lower() or 
                   query in i['color'].lower() or
                   query in i['location'].lower() or 
                   query in i.get('description', '').lower()]
    
    return jsonify(approved)

# ===================== MEMBER 3: LOST ITEM MODULE ============================
@app.route('/report_lost', methods=['GET', 'POST'])
def report_lost():
    """User reports a LOST item (Member 3)."""
    if session.get('user_type') != 'user':
        return redirect(url_for('login'))

    if request.method == 'POST':
        item = {
            'type': 'lost',
            'item_name': request.form.get('item_name', '').strip(),
            'color': request.form.get('color', '').strip(),
            'location': request.form.get('location', '').strip(),
            'description': request.form.get('description', '').strip(),
            'reported_by': session['username'],
            'status': 'pending',
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'category': request.form.get('category', 'other'),
            'contact': request.form.get('contact', '')
        }
        # Find potential matches
        matches = find_matching_items(item)
        write_item(item)
        if matches:
            flash(f'Lost item reported! Found {len(matches)} potential matches. Check your dashboard!', 'success')
        else:
            flash('Lost item reported! Waiting for admin approval.', 'success')
        return redirect(url_for('dashboard'))

    return render_template('report_lost.html')

# ===================== MEMBER 4: FOUND ITEM MODULE ===========================
@app.route('/report_found', methods=['GET', 'POST'])
def report_found():
    """User reports a FOUND item (Member 4)."""
    if session.get('user_type') != 'user':
        return redirect(url_for('login'))

    if request.method == 'POST':
        item = {
            'type': 'found',
            'item_name': request.form.get('item_name', '').strip(),
            'color': request.form.get('color', '').strip(),
            'location': request.form.get('location', '').strip(),
            'description': request.form.get('description', '').strip(),
            'reported_by': session['username'],
            'status': 'pending',
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'category': request.form.get('category', 'other'),
            'contact': request.form.get('contact', '')
        }
        # Find potential matches
        matches = find_matching_items(item)
        write_item(item)
        if matches:
            flash(f'Found item reported! Found {len(matches)} potential matches. Check your dashboard!', 'success')
        else:
            flash('Found item reported! Waiting for admin approval.', 'success')
        return redirect(url_for('dashboard'))

    return render_template('report_found.html')

# ========================== USER DASHBOARD ==================================
@app.route('/dashboard')
def dashboard():
    """Shows user's own submitted lost/found items."""
    if session.get('user_type') != 'user':
        return redirect(url_for('login'))

    items = read_items()
    user_items = [i for i in items if i['reported_by'] == session['username']]
    # Find matches for each item
    for item in user_items:
        if item['status'] == 'approved':
            item['matches'] = find_matching_items(item)
    return render_template('dashboard.html', items=user_items, username=session['username'])

# =============================== LOGOUT ======================================
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# ====================== PUBLIC BROWSING (OPTIONAL) ===========================
@app.route('/browse_items')
def browse_items():
    """Shows all approved items to public."""
    items = read_items()
    approved = [i for i in items if i['status'] == 'approved']
    
    # Filter parameters
    filter_type = request.args.get('type', 'all')
    category = request.args.get('category', 'all')
    search_query = request.args.get('search', '').lower()
    
    if filter_type != 'all':
        approved = [i for i in approved if i['type'] == filter_type]
    if category != 'all':
        approved = [i for i in approved if i.get('category', 'other') == category]
    if search_query:
        approved = [i for i in approved if 
                  search_query in i['item_name'].lower() or 
                  search_query in i['color'].lower() or
                  search_query in i['location'].lower() or 
                  search_query in i.get('description', '').lower()]
    
    # Get unique categories
    categories = sorted(set([i.get('category', 'other') for i in items]))
    
    return render_template('browse_items.html', 
                         items=approved, 
                         filter_type=filter_type,
                         category=category,
                         search_query=search_query,
                         categories=categories)

# ============================== MAIN RUNNER ==================================
if __name__ == '__main__':
    app.run(debug=True)
