# Here are your Instructions
# Attendance Management System

A comprehensive employee attendance tracking system built with React frontend and FastAPI backend. Track employee attendance, manage employee records, and generate attendance reports with a 70% attendance threshold rule.

![Attendance Management System](https://img.shields.io/badge/Status-Ready-green) ![Python](https://img.shields.io/badge/Python-3.8+-blue) ![React](https://img.shields.io/badge/React-18+-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green) ![MongoDB](https://img.shields.io/badge/MongoDB-4.4+-green)

## 📋 Features

### 🏠 Dashboard
- **System Statistics**: View total employees, attendance records, and compliance metrics
- **Quick Actions**: Generate sample data or calculate attendance with one click
- **70% Threshold Tracking**: Monitor employees meeting attendance requirements

### 👥 Employee Management
- **Add Employees**: Manually add new employees with complete contact information
- **Employee Directory**: View all employees with phone numbers, emails, and departments
- **Search & Filter**: Find employees by name, department, or attendance status
- **Delete Employees**: Remove employees with confirmation dialog

### 📊 Attendance Analysis
- **Attendance Calculation**: Automatic calculation of attendance percentages
- **Status Tracking**: Present, absent, and late day tracking
- **Recent Performance**: 7-day performance trends (Excellent/Good/Average/Poor)
- **Detailed Reports**: Individual employee attendance summaries

### 📱 User Interface
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Professional UI**: Clean, modern interface with Tailwind CSS
- **Real-time Updates**: Instant data refresh and updates
- **Modal Forms**: Professional forms for adding employees

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8 or higher** - [Download Python](https://python.org/downloads/)
- **Node.js 16 or higher** - [Download Node.js](https://nodejs.org/downloads/)
- **MongoDB 4.4 or higher** - [Download MongoDB](https://www.mongodb.com/try/download/community)
- **Git** - [Download Git](https://git-scm.com/downloads/)

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd attendance-management-system
```

### 2. Backend Setup (FastAPI)

#### Navigate to backend directory
```bash
cd backend
```

#### Create Python virtual environment
```bash
# Windows
python -m venv venv
venv\\Scripts\\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### Install Python dependencies
```bash
pip install -r requirements.txt
```

#### Create environment file
```bash
# Create .env file in the backend directory
echo 'MONGO_URL="mongodb://localhost:27017"' > .env
echo 'DB_NAME="attendance_system"' >> .env
```

### 3. Frontend Setup (React)

#### Navigate to frontend directory
```bash
cd ../frontend
```

#### Install Node.js dependencies
```bash
# Using npm
npm install

# Or using yarn (preferred)
yarn install
```

#### Create environment file
```bash
# Create .env file in the frontend directory
echo 'REACT_APP_BACKEND_URL=http://localhost:8001' > .env
```

### 4. Database Setup (MongoDB)

#### Start MongoDB service

**Windows:**
```bash
# If MongoDB is installed as a service
net start MongoDB

# Or start manually
mongod --dbpath "C:\\data\\db"
```

**macOS:**
```bash
# Using Homebrew
brew services start mongodb-community

# Or start manually
mongod --config /usr/local/etc/mongod.conf
```

**Linux:**
```bash
# Using systemd
sudo systemctl start mongod

# Or start manually
mongod --dbpath /var/lib/mongodb
```

#### Verify MongoDB is running
```bash
# Connect to MongoDB
mongo
# or
mongosh

# You should see the MongoDB shell prompt
```

## 🏃\u200d♂️ Running the Application

### 1. Start the Backend Server

```bash
# In the backend directory with virtual environment activated
cd backend
python server.py

# The backend will start on http://localhost:8001
```

### 2. Start the Frontend Server

```bash
# In a new terminal, navigate to frontend directory
cd frontend

# Start the React development server
npm start
# or
yarn start

# The frontend will start on http://localhost:3000
```

### 3. Access the Application

Open your web browser and navigate to:
```
http://localhost:3000
```

## 📖 Usage Guide

### Getting Started

1. **Generate Sample Data**
   - Click "Generate 100 Employees Data" on the dashboard
   - This creates 100 realistic employees with 30 days of attendance data

2. **Calculate Attendance**
   - Click "Calculate Attendance" to process attendance metrics
   - View results in the "Analysis Results" tab

3. **Manage Employees**
   - Navigate to the "Employees" tab
   - Use search and filters to find specific employees
   - Add new employees using the "Add Employee" button

### Adding New Employees

1. Click "Add Employee" button in the Employees section
2. Fill out the form with:
   - **Full Name**: Employee's complete name
   - **Department**: Select from available departments
   - **Position**: Job title or role
   - **Email**: Work email address (must be unique)
   - **Phone**: Contact phone number
3. Click "Add Employee" to save

### Viewing Attendance Reports

1. Navigate to "Analysis Results" tab
2. View summary statistics:
   - Total employees
   - Employees meeting 70% threshold
   - Employees below threshold
   - Average attendance rate
3. Review individual employee details with attendance percentages

## 🔧 API Documentation

### Base URL
```
http://localhost:8001/api
```

### Endpoints

#### Employee Management
- `GET /employees` - Get all employees with attendance summaries
- `POST /add-employee` - Add a new employee
- `DELETE /employees/{employee_id}` - Delete an employee

#### Attendance & Analytics
- `GET /dashboard-stats` - Get dashboard statistics
- `POST /analyze-attendance` - Calculate attendance metrics
- `GET /attendance-report` - Get attendance analysis results

#### Data Management
- `GET /sample-data` - Generate 100 sample employees
- `POST /upload-attendance` - Upload custom attendance data
- `GET /health` - Health check endpoint

### Example API Calls

#### Add Employee
```bash
curl -X POST http://localhost:8001/api/add-employee \\
  -H "Content-Type: application/json" \\
  -d '{
    "name": "John Smith",
    "department": "Engineering",
    "position": "Software Developer",
    "email": "john.smith@company.com",
    "phone": "(555) 123-4567"
  }'
```

#### Get All Employees
```bash
curl http://localhost:8001/api/employees
```

## 📁 Project Structure

```
attendance-management-system/
├── backend/                    # FastAPI backend
│   ├── server.py              # Main FastAPI application
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # Environment variables
├── frontend/                  # React frontend
│   ├── src/
│   │   ├── App.js            # Main React component
│   │   ├── App.css           # Styles and Tailwind imports
│   │   ├── index.js          # React entry point
│   │   └── index.css         # Global styles
│   ├── public/               # Static assets
│   ├── package.json          # Node.js dependencies
│   ├── tailwind.config.js    # Tailwind CSS configuration
│   └── .env                  # Environment variables
├── tests/                    # Test files
├── scripts/                  # Utility scripts
└── README.md                 # This file
```

## 🎨 Customization

### Adding New Departments

Edit the `positions` dictionary in `backend/server.py`:

```python
departments = ["Engineering", "Marketing", "Sales", "HR", "Finance", "Operations", "Customer Service", "Product", "Design", "Legal", "Your New Department"]
```

### Changing Attendance Threshold

Modify the threshold in the `calculate_attendance_metrics` function:

```python
"status": "meets_threshold" if attendance_percentage >= 80 else "below_threshold"  # Changed from 70 to 80
```

### Styling Customization

The frontend uses Tailwind CSS. Modify `frontend/src/App.css` or component classes in `frontend/src/App.js` to customize the appearance.

## 🐛 Troubleshooting

### Common Issues

#### MongoDB Connection Error
```
Error: MongoServerError: connect ECONNREFUSED
```
**Solution**: Ensure MongoDB is running on port 27017

#### Backend Port Already in Use
```
Error: [Errno 48] Address already in use
```
**Solution**: Kill the process using port 8001 or change the port in `server.py`

#### Frontend Build Errors
```
Error: Cannot resolve dependency
```
**Solution**: Delete `node_modules` and reinstall dependencies:
```bash
rm -rf node_modules package-lock.json
npm install
```

#### CORS Errors
```
Error: Access to fetch blocked by CORS policy
```
**Solution**: Ensure backend is running and frontend environment variables are correct

### Port Configuration

If you need to change default ports:

1. **Backend Port** (default: 8001):
   - Modify `uvicorn.run(app, host="0.0.0.0", port=8001)` in `server.py`
   - Update `REACT_APP_BACKEND_URL` in frontend `.env`

2. **Frontend Port** (default: 3000):
   - Create `.env.local` in frontend directory
   - Add `PORT=3001` to change to port 3001

### Database Reset

To reset all data:

```bash
# Connect to MongoDB
mongo
# or
mongosh

# Switch to database
use attendance_system

# Drop all collections
db.employees.drop()
db.attendance_records.drop()
db.analysis_results.drop()
```

## 📊 Sample Data

The system includes realistic sample data:
- **100 employees** across 10 departments
- **2,200+ attendance records** (30 working days)
- **Varied attendance patterns**: High performers (90-95%), good (80-89%), average (70-79%), below average (60-69%), poor (40-59%)
- **Complete contact information**: Professional emails and phone numbers

## 🔒 Security Notes

For production deployment:
1. Change MongoDB connection to use authentication
2. Add input validation and sanitization
3. Implement user authentication and authorization
4. Use HTTPS for all communications
5. Set up proper CORS policies
6. Add rate limiting to API endpoints

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Search existing issues in the repository
3. Create a new issue with detailed information about the problem

## 🎯 System Requirements

### Minimum Requirements
- **CPU**: Dual-core processor
- **RAM**: 4GB RAM
- **Storage**: 1GB free space
- **OS**: Windows 10, macOS 10.14, or Ubuntu 18.04

### Recommended Requirements
- **CPU**: Quad-core processor
- **RAM**: 8GB RAM
- **Storage**: 2GB free space
- **OS**: Latest versions of Windows, macOS, or Linux

---

**Happy tracking! 📈👥**