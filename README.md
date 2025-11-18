# Lost & Found Portal - Campus Item Recovery System

A comprehensive web application for managing lost and found items on campus. Built with Flask (Python) backend and HTML/CSS frontend.

## Features

- **User Authentication**: Login and Signup functionality
- **Admin Panel**: Admin login with approval system
- **Report Lost Items**: Users can report items they've lost with details (item name, color, location, description)
- **Report Found Items**: Users can report items they've found with details
- **Admin Approval**: Admins can approve or reject reported items
- **Browse Items**: View all approved lost and found items
- **Text File Storage**: All data stored in text files (users.txt, items.txt, admin.txt)

## Installation

1. Install Python 3.7 or higher
2. Install required packages:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

## Default Admin Credentials

- **Username**: `admin`
- **Password**: `admin123`

⚠️ **Important**: Change the admin password in production by editing `data/admin.txt`

## Project Structure

```
python_pbl/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── data/                 # Data storage directory
│   ├── users.txt         # User credentials
│   ├── items.txt         # Lost/Found items
│   └── admin.txt         # Admin credentials
├── templates/            # HTML templates
│   ├── index.html        # Home page
│   ├── login.html        # User login
│   ├── signup.html       # User signup
│   ├── admin_login.html  # Admin login
│   ├── dashboard.html    # User dashboard
│   ├── admin_dashboard.html  # Admin dashboard
│   ├── report_lost.html  # Report lost item
│   ├── report_found.html # Report found item
│   └── browse_items.html # Browse approved items
└── static/               # Static files
    └── style.css         # Stylesheet
```

## Usage Guide

### For Users:

1. **Sign Up**: Create a new account from the home page
2. **Login**: Access your account
3. **Report Lost Item**: Click "Report Lost Item" and fill in:
   - Item name
   - Color
   - Location where you lost it
   - Additional description (optional)
4. **Report Found Item**: Click "Report Found Item" and fill in:
   - Item name
   - Color
   - Location where you found it
   - Additional description (optional)
5. **Browse Items**: View all approved items to find matches

### For Admins:

1. **Admin Login**: Use admin credentials to login
2. **Review Items**: View all pending items awaiting approval
3. **Approve/Reject**: Review item details and approve or reject them
4. **View All Items**: See all items in the system with their status

## Data Storage

All data is stored in text files in the `data/` directory:

- **users.txt**: Format: `username:password`
- **items.txt**: Format: `id|type|item_name|color|location|description|reported_by|status|date`
- **admin.txt**: Format: `username:password`

## Security Notes

- This is a development version. For production:
  - Change the Flask secret key in `app.py`
  - Implement password hashing (currently passwords are stored in plain text)
  - Use a proper database instead of text files
  - Add CSRF protection
  - Implement session timeout

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3
- **Storage**: Text files

## License

This project is created for educational purposes.

