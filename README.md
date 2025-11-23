# Lost and Found Item Management System

A Flask-based web application for managing lost and found items. This is a collaborative project built by a team of 4 members, each responsible for different modules of the application.

## Features

### User Features
- **User Authentication**: Sign up and login functionality
- **Report Lost Items**: Users can report items they have lost
- **Report Found Items**: Users can report items they have found
- **User Dashboard**: View all your submitted items and their status
- **Item Matching**: Automatic matching of lost items with found items based on:
  - Item name
  - Color
  - Location
  - Description keywords
- **Browse Items**: Public browsing of all approved lost and found items
- **Advanced Search**: Filter items by type, category, and keywords

### Admin Features
- **Admin Dashboard**: View all items with filtering options
- **Item Approval**: Approve or reject submitted items
- **Item Management**: Delete items from the system
- **Statistics**: View comprehensive statistics including:
  - Total items
  - Pending/Approved/Rejected counts
  - Lost vs Found items
  - Items by category
  - Recent items
- **Advanced Filtering**: Filter by type, status, and search queries

## Technologies Used

- **Backend**: Python 3.x
- **Web Framework**: Flask 3.0.3
- **Frontend**: HTML, CSS, JavaScript
- **Data Storage**: File-based storage (TXT files)

## Project Structure

```
python_pbl/
├── app.py                      # Main Flask application
├── requirement.txt             # Python dependencies
├── data/                       # Data storage directory
│   ├── users.txt              # User accounts
│   ├── items.txt              # Lost and found items
│   └── admin.txt              # Admin credentials
├── templates/                  # HTML templates
│   ├── index.html             # Home page
│   ├── login.html             # User login page
│   ├── signup.html            # User registration page
│   ├── admin_login.html       # Admin login page
│   ├── admin_dashboard.html   # Admin dashboard
│   ├── dashboard.html         # User dashboard
│   ├── report_lost.html       # Report lost item form
│   ├── report_found.html      # Report found item form
│   └── browse_items.html      # Public browsing page
└── static/                     # Static files
    ├── style.css              # Stylesheet
    └── script.js              # JavaScript files
```

## Installation

### Prerequisites
- Python 3.x installed on your system
- pip (Python package manager)

### Setup Instructions

1. **Clone or download the project**
   ```bash
   cd python_pbl
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirement.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Open your web browser and navigate to: `http://127.0.0.1:5000`

## Usage

### For Users

1. **Sign Up**: Create a new account by clicking "Sign Up" on the home page
2. **Login**: Use your credentials to log in
3. **Report Items**:
   - Click "Report Lost Item" to report something you've lost
   - Click "Report Found Item" to report something you've found
   - Fill in all required details (item name, color, location, description, category, contact)
4. **View Dashboard**: Check your submitted items and see potential matches
5. **Browse Items**: View all approved lost and found items

### For Admins

1. **Admin Login**: Navigate to admin login page and use admin credentials
   - Default credentials: `admin:admin123` (change this in production!)
2. **Dashboard**: View all items and filter by type, status, or search terms
3. **Manage Items**: 
   - Approve pending items
   - Reject inappropriate items
   - Delete items if needed
4. **View Statistics**: Check the statistics panel for insights

## Team Contributions

This project was developed collaboratively with clear module distribution:

- **Member 1**: Login, Signup, and UI components
- **Member 2**: Admin Panel (login, dashboard, approval system, statistics)
- **Member 3**: Lost Item Module (reporting and management)
- **Member 4**: Found Item Module (reporting and management)

All members collaborated on shared utilities for reading/writing items and user data.

## Default Credentials

- **Admin**: `admin:admin123` (Please change in production!)

## API Endpoints

- `/api/statistics` - Get application statistics (Admin only)
- `/api/search` - Search items with query parameters

## Data Storage

The application uses file-based storage:
- **UTF-8 encoding** for proper international character support
- **Pipe-delimited format** (`|`) for items storage
- **Colon-delimited format** (`:`) for user/admin credentials

## Security Notes

⚠️ **Important**: This is a development version. Before deploying to production:
- Change the Flask secret key in `app.py`
- Change default admin credentials
- Implement proper password hashing
- Use a production-grade database instead of text files
- Implement proper session management and CSRF protection

## Future Enhancements

- Database integration (SQLite/PostgreSQL)
- Image upload for items
- Email notifications for matches
- User profiles and contact management
- Enhanced security features
- Mobile-responsive design improvements

## License

This project is developed for educational purposes as part of a Problem-Based Learning (PBL) assignment.

## Support

For issues or questions, please refer to the project documentation or contact the development team.

