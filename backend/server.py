from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
from datetime import datetime, timedelta
import json
import asyncio
import uuid
from motor.motor_asyncio import AsyncIOMotorClient
from emergentintegrations.llm.chat import LlmChat, UserMessage
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Attendance Analyzer", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'attendance_system')

client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

# Gemini AI setup
GEMINI_API_KEY = "AIzaSyAYYBn61_8r8tnVYUTqVxKvcy7PYQa5Jow"

# Pydantic models
class Employee(BaseModel):
    employee_id: str
    name: str
    department: str
    position: str
    email: str
    phone: str

class AttendanceRecord(BaseModel):
    employee_id: str
    date: str
    check_in_time: Optional[str] = None
    check_out_time: Optional[str] = None
    status: str = "absent"  # present, absent, late, half_day
    hours_worked: float = 0.0

class AttendanceData(BaseModel):
    employees: List[Employee]
    attendance_records: List[AttendanceRecord]
    analysis_period: str
    work_hours_start: str = "09:00"
    work_hours_end: str = "17:00"
    late_threshold_minutes: int = 30

class AnalysisResult(BaseModel):
    employee_id: str
    name: str
    department: str
    total_days: int
    present_days: int
    absent_days: int
    late_days: int
    attendance_percentage: float
    status: str  # meets_threshold, below_threshold
    ai_insights: str

# Helper functions
def generate_sample_data():
    """Generate sample attendance data for demonstration"""
    employees = [
        Employee(employee_id="EMP001", name="John Smith", department="Engineering", position="Senior Developer", email="john@company.com"),
        Employee(employee_id="EMP002", name="Sarah Johnson", department="Marketing", position="Marketing Manager", email="sarah@company.com"),
        Employee(employee_id="EMP003", name="Mike Chen", department="Engineering", position="Software Engineer", email="mike@company.com"),
        Employee(employee_id="EMP004", name="Emily Davis", department="HR", position="HR Specialist", email="emily@company.com"),
        Employee(employee_id="EMP005", name="David Wilson", department="Sales", position="Sales Executive", email="david@company.com"),
    ]
    
    # Generate 30 days of sample attendance data
    attendance_records = []
    start_date = datetime.now() - timedelta(days=30)
    
    for employee in employees:
        for day in range(30):
            current_date = start_date + timedelta(days=day)
            if current_date.weekday() < 5:  # Monday to Friday
                # Simulate different attendance patterns
                import random
                
                if employee.employee_id == "EMP001":  # High performer
                    present_chance = 0.95
                elif employee.employee_id == "EMP002":  # Average
                    present_chance = 0.80
                elif employee.employee_id == "EMP003":  # Good
                    present_chance = 0.88
                elif employee.employee_id == "EMP004":  # Below average
                    present_chance = 0.65
                else:  # EMP005 - Poor
                    present_chance = 0.60
                
                if random.random() < present_chance:
                    # Present - generate check-in and check-out times
                    base_checkin = 9 * 60  # 9:00 AM in minutes
                    base_checkout = 17 * 60  # 5:00 PM in minutes
                    
                    # Add some randomness
                    checkin_minutes = base_checkin + random.randint(-30, 60)
                    checkout_minutes = base_checkout + random.randint(-30, 60)
                    
                    checkin_time = f"{checkin_minutes // 60:02d}:{checkin_minutes % 60:02d}"
                    checkout_time = f"{checkout_minutes // 60:02d}:{checkout_minutes % 60:02d}"
                    
                    # Determine status
                    if checkin_minutes > base_checkin + 30:  # Late by more than 30 minutes
                        status = "late"
                    else:
                        status = "present"
                    
                    hours_worked = max(0, (checkout_minutes - checkin_minutes) / 60)
                    
                    attendance_records.append(AttendanceRecord(
                        employee_id=employee.employee_id,
                        date=current_date.strftime("%Y-%m-%d"),
                        check_in_time=checkin_time,
                        check_out_time=checkout_time,
                        status=status,
                        hours_worked=round(hours_worked, 2)
                    ))
                else:
                    # Absent
                    attendance_records.append(AttendanceRecord(
                        employee_id=employee.employee_id,
                        date=current_date.strftime("%Y-%m-%d"),
                        status="absent"
                    ))
    
    return AttendanceData(
        employees=employees,
        attendance_records=attendance_records,
        analysis_period="Last 30 days",
        work_hours_start="09:00",
        work_hours_end="17:00",
        late_threshold_minutes=30
    )

async def analyze_with_gemini(employee_data: Dict, attendance_summary: Dict) -> str:
    """Use Gemini AI to analyze attendance patterns and provide insights"""
    try:
        # Create a new chat instance for this analysis
        chat = LlmChat(
            api_key=GEMINI_API_KEY,
            session_id=f"attendance_analysis_{uuid.uuid4()}",
            system_message="You are an expert HR analytics assistant. Analyze attendance data and provide professional insights about employee performance, patterns, and recommendations."
        ).with_model("gemini", "gemini-2.0-flash")
        
        # Create analysis prompt
        prompt = f"""
        Analyze the following employee attendance data and provide insights:
        
        Employee: {employee_data['name']} ({employee_data['employee_id']})
        Department: {employee_data['department']}
        Position: {employee_data['position']}
        
        Attendance Summary:
        - Total Working Days: {attendance_summary['total_days']}
        - Present Days: {attendance_summary['present_days']}
        - Absent Days: {attendance_summary['absent_days']}
        - Late Days: {attendance_summary['late_days']}
        - Attendance Percentage: {attendance_summary['attendance_percentage']:.1f}%
        - Average Hours Worked: {attendance_summary.get('avg_hours', 0):.1f} hours/day
        
        Please provide:
        1. Overall attendance assessment (2-3 sentences)
        2. Key patterns or concerns (if any)
        3. Specific recommendations for improvement (if attendance < 70%)
        4. Recognition for good performance (if attendance >= 85%)
        
        Keep the response professional, constructive, and under 200 words.
        """
        
        user_message = UserMessage(text=prompt)
        response = await chat.send_message(user_message)
        
        return response
        
    except Exception as e:
        logger.error(f"Error analyzing with Gemini: {str(e)}")
        return f"Analysis unavailable. Basic assessment: {'Meets expectations' if attendance_summary['attendance_percentage'] >= 70 else 'Below standard - requires attention'}."

def calculate_attendance_metrics(employee: Employee, records: List[AttendanceRecord]) -> Dict:
    """Calculate attendance metrics for an employee"""
    employee_records = [r for r in records if r.employee_id == employee.employee_id]
    
    total_days = len(employee_records)
    present_days = len([r for r in employee_records if r.status in ["present", "late"]])
    absent_days = len([r for r in employee_records if r.status == "absent"])
    late_days = len([r for r in employee_records if r.status == "late"])
    
    attendance_percentage = (present_days / total_days * 100) if total_days > 0 else 0
    
    # Calculate average hours worked
    worked_records = [r for r in employee_records if r.hours_worked > 0]
    avg_hours = sum(r.hours_worked for r in worked_records) / len(worked_records) if worked_records else 0
    
    return {
        "total_days": total_days,
        "present_days": present_days,
        "absent_days": absent_days,
        "late_days": late_days,
        "attendance_percentage": attendance_percentage,
        "avg_hours": avg_hours,
        "status": "meets_threshold" if attendance_percentage >= 70 else "below_threshold"
    }

# API Routes
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "AI Attendance Analyzer"}

@app.get("/api/sample-data")
async def get_sample_data():
    """Get sample attendance data for demonstration"""
    try:
        sample_data = generate_sample_data()
        
        # Store sample data in database
        await db.employees.delete_many({})
        await db.attendance_records.delete_many({})
        
        # Insert employees
        employee_docs = [emp.dict() for emp in sample_data.employees]
        await db.employees.insert_many(employee_docs)
        
        # Insert attendance records
        record_docs = [rec.dict() for rec in sample_data.attendance_records]
        await db.attendance_records.insert_many(record_docs)
        
        return {
            "message": "Sample data generated successfully",
            "employees_count": len(sample_data.employees),
            "records_count": len(sample_data.attendance_records),
            "analysis_period": sample_data.analysis_period
        }
        
    except Exception as e:
        logger.error(f"Error generating sample data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze-attendance")
async def analyze_attendance():
    """Analyze attendance data and generate AI-powered insights"""
    try:
        # Get employees and attendance records from database
        employees_cursor = db.employees.find({})
        employees_list = await employees_cursor.to_list(length=None)
        
        records_cursor = db.attendance_records.find({})
        records_list = await records_cursor.to_list(length=None)
        
        if not employees_list or not records_list:
            raise HTTPException(status_code=404, detail="No attendance data found. Please generate sample data first.")
        
        # Convert to Pydantic models
        employees = [Employee(**emp) for emp in employees_list]
        records = [AttendanceRecord(**rec) for rec in records_list]
        
        analysis_results = []
        
        # Analyze each employee
        for employee in employees:
            # Calculate basic metrics
            metrics = calculate_attendance_metrics(employee, records)
            
            # Get AI insights
            ai_insights = await analyze_with_gemini(employee.dict(), metrics)
            
            # Create analysis result
            result = AnalysisResult(
                employee_id=employee.employee_id,
                name=employee.name,
                department=employee.department,
                total_days=metrics["total_days"],
                present_days=metrics["present_days"],
                absent_days=metrics["absent_days"],
                late_days=metrics["late_days"],
                attendance_percentage=metrics["attendance_percentage"],
                status=metrics["status"],
                ai_insights=ai_insights
            )
            
            analysis_results.append(result)
        
        # Store analysis results
        await db.analysis_results.delete_many({})
        result_docs = [result.dict() for result in analysis_results]
        await db.analysis_results.insert_many(result_docs)
        
        # Calculate summary statistics
        total_employees = len(analysis_results)
        meeting_threshold = len([r for r in analysis_results if r.status == "meets_threshold"])
        below_threshold = total_employees - meeting_threshold
        
        avg_attendance = sum(r.attendance_percentage for r in analysis_results) / total_employees if total_employees > 0 else 0
        
        return {
            "message": "Attendance analysis completed successfully",
            "summary": {
                "total_employees": total_employees,
                "meeting_70_percent_threshold": meeting_threshold,
                "below_threshold": below_threshold,
                "average_attendance_rate": round(avg_attendance, 1),
                "analysis_timestamp": datetime.now().isoformat()
            },
            "detailed_results": [result.dict() for result in analysis_results]
        }
        
    except Exception as e:
        logger.error(f"Error analyzing attendance: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/attendance-report")
async def get_attendance_report():
    """Get the latest attendance analysis report"""
    try:
        # Get analysis results from database
        results_cursor = db.analysis_results.find({})
        results_list = await results_cursor.to_list(length=None)
        
        if not results_list:
            return {"message": "No analysis results found. Please run attendance analysis first.", "results": []}
        
        # Convert ObjectId to string for JSON serialization
        for result in results_list:
            if '_id' in result:
                result['_id'] = str(result['_id'])
        
        # Calculate summary
        total_employees = len(results_list)
        meeting_threshold = len([r for r in results_list if r["status"] == "meets_threshold"])
        below_threshold = total_employees - meeting_threshold
        avg_attendance = sum(r["attendance_percentage"] for r in results_list) / total_employees if total_employees > 0 else 0
        
        return {
            "summary": {
                "total_employees": total_employees,
                "meeting_70_percent_threshold": meeting_threshold,
                "below_threshold": below_threshold,
                "average_attendance_rate": round(avg_attendance, 1)
            },
            "results": results_list
        }
        
    except Exception as e:
        logger.error(f"Error getting attendance report: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/upload-attendance")
async def upload_attendance_data(data: AttendanceData):
    """Upload custom attendance data for analysis"""
    try:
        # Clear existing data
        await db.employees.delete_many({})
        await db.attendance_records.delete_many({})
        await db.analysis_results.delete_many({})
        
        # Insert new data
        employee_docs = [emp.dict() for emp in data.employees]
        await db.employees.insert_many(employee_docs)
        
        record_docs = [rec.dict() for rec in data.attendance_records]
        await db.attendance_records.insert_many(record_docs)
        
        return {
            "message": "Attendance data uploaded successfully",
            "employees_count": len(data.employees),
            "records_count": len(data.attendance_records)
        }
        
    except Exception as e:
        logger.error(f"Error uploading attendance data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/dashboard-stats")
async def get_dashboard_stats():
    """Get dashboard statistics"""
    try:
        # Get counts from database
        employees_count = await db.employees.count_documents({})
        records_count = await db.attendance_records.count_documents({})
        analysis_count = await db.analysis_results.count_documents({})
        
        # Get recent analysis summary if available
        recent_analysis = await db.analysis_results.find({}).to_list(length=None)
        
        stats = {
            "employees_count": employees_count,
            "records_count": records_count,
            "analysis_count": analysis_count,
            "has_analysis": analysis_count > 0
        }
        
        if recent_analysis:
            meeting_threshold = len([r for r in recent_analysis if r["status"] == "meets_threshold"])
            below_threshold = len(recent_analysis) - meeting_threshold
            avg_attendance = sum(r["attendance_percentage"] for r in recent_analysis) / len(recent_analysis)
            
            stats.update({
                "meeting_threshold": meeting_threshold,
                "below_threshold": below_threshold,
                "average_attendance": round(avg_attendance, 1)
            })
        
        return stats
        
    except Exception as e:
        logger.error(f"Error getting dashboard stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)