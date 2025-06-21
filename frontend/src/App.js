import React, { useState, useEffect } from 'react';
import './App.css';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL;

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [dashboardStats, setDashboardStats] = useState(null);
  const [analysisResults, setAnalysisResults] = useState(null);
  const [employeesData, setEmployeesData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterDepartment, setFilterDepartment] = useState('');
  const [filterStatus, setFilterStatus] = useState('');

  // Fetch dashboard stats on component mount
  useEffect(() => {
    fetchDashboardStats();
  }, []);

  const fetchDashboardStats = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/dashboard-stats`);
      const data = await response.json();
      setDashboardStats(data);
    } catch (err) {
      console.error('Error fetching dashboard stats:', err);
      setError('Failed to load dashboard statistics');
    }
  };

  const fetchEmployeesData = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_BASE_URL}/api/employees`);
      const data = await response.json();
      
      if (response.ok) {
        setEmployeesData(data);
        setError(null);
      } else {
        throw new Error(data.message || 'Failed to fetch employees data');
      }
    } catch (err) {
      console.error('Error fetching employees data:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const generateSampleData = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_BASE_URL}/api/sample-data`);
      const data = await response.json();
      
      if (response.ok) {
        await fetchDashboardStats();
        setError(null);
        alert('Sample data with 100 employees generated successfully!');
      } else {
        throw new Error(data.detail || 'Failed to generate sample data');
      }
    } catch (err) {
      console.error('Error generating sample data:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const analyzeAttendance = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_BASE_URL}/api/analyze-attendance`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      const data = await response.json();
      
      if (response.ok) {
        setAnalysisResults(data);
        await fetchDashboardStats();
        setActiveTab('results');
        setError(null);
      } else {
        throw new Error(data.detail || 'Failed to analyze attendance');
      }
    } catch (err) {
      console.error('Error analyzing attendance:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getAttendanceReport = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_BASE_URL}/api/attendance-report`);
      const data = await response.json();
      
      if (response.ok) {
        setAnalysisResults(data);
        setActiveTab('results');
        setError(null);
      } else {
        throw new Error('Failed to fetch attendance report');
      }
    } catch (err) {
      console.error('Error fetching report:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    return status === 'meets_threshold' ? 'text-green-600' : 'text-red-600';
  };

  const getStatusBadge = (status) => {
    const baseClasses = 'px-3 py-1 rounded-full text-sm font-medium';
    if (status === 'meets_threshold') {
      return `${baseClasses} bg-green-100 text-green-800`;
    }
    return `${baseClasses} bg-red-100 text-red-800`;
  };

  const renderDashboard = () => (
    <div className="space-y-8">
      {/* Hero Section */}
      <div className="text-center bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-2xl p-8">
        <h1 className="text-4xl font-bold mb-4">AI-Powered Attendance Analyzer</h1>
        <p className="text-xl opacity-90 mb-6">
          Automated attendance tracking with intelligent insights and 70% attendance threshold analysis
        </p>
        <div className="flex flex-wrap justify-center gap-4">
          <button
            onClick={generateSampleData}
            disabled={loading}
            className="bg-white text-blue-600 px-6 py-3 rounded-lg font-semibold hover:bg-blue-50 transition-colors disabled:opacity-50"
          >
            {loading ? 'Generating...' : 'Generate Sample Data'}
          </button>
          <button
            onClick={analyzeAttendance}
            disabled={loading || !dashboardStats?.employees_count}
            className="bg-purple-700 text-white px-6 py-3 rounded-lg font-semibold hover:bg-purple-800 transition-colors disabled:opacity-50"
          >
            {loading ? 'Analyzing...' : 'Analyze Attendance'}
          </button>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg">
          <strong>Error:</strong> {error}
        </div>
      )}

      {/* Dashboard Stats */}
      {dashboardStats && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="bg-white rounded-xl shadow-md p-6 border-l-4 border-blue-500">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total Employees</p>
                <p className="text-3xl font-bold text-gray-900">{dashboardStats.employees_count}</p>
              </div>
              <div className="bg-blue-100 p-3 rounded-full">
                <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-md p-6 border-l-4 border-green-500">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Attendance Records</p>
                <p className="text-3xl font-bold text-gray-900">{dashboardStats.records_count}</p>
              </div>
              <div className="bg-green-100 p-3 rounded-full">
                <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
                </svg>
              </div>
            </div>
          </div>

          {dashboardStats.has_analysis && (
            <>
              <div className="bg-white rounded-xl shadow-md p-6 border-l-4 border-yellow-500">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Meeting 70% Threshold</p>
                    <p className="text-3xl font-bold text-gray-900">{dashboardStats.meeting_threshold}</p>
                  </div>
                  <div className="bg-yellow-100 p-3 rounded-full">
                    <svg className="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-xl shadow-md p-6 border-l-4 border-purple-500">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Average Attendance</p>
                    <p className="text-3xl font-bold text-gray-900">{dashboardStats.average_attendance}%</p>
                  </div>
                  <div className="bg-purple-100 p-3 rounded-full">
                    <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                    </svg>
                  </div>
                </div>
              </div>
            </>
          )}
        </div>
      )}

      {/* Action Buttons */}
      <div className="bg-white rounded-xl shadow-md p-6">
        <h3 className="text-xl font-semibold mb-4">Quick Actions</h3>
        <div className="flex flex-wrap gap-4">
          <button
            onClick={generateSampleData}
            disabled={loading}
            className="bg-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors disabled:opacity-50"
          >
            Generate Sample Data
          </button>
          <button
            onClick={analyzeAttendance}
            disabled={loading || !dashboardStats?.employees_count}
            className="bg-green-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-green-700 transition-colors disabled:opacity-50"
          >
            Run AI Analysis
          </button>
          <button
            onClick={getAttendanceReport}
            disabled={loading || !dashboardStats?.has_analysis}
            className="bg-purple-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-purple-700 transition-colors disabled:opacity-50"
          >
            View Latest Report
          </button>
        </div>
      </div>

      {/* Instructions */}
      <div className="bg-blue-50 rounded-xl p-6">
        <h3 className="text-lg font-semibold text-blue-900 mb-3">How to Use</h3>
        <div className="space-y-2 text-blue-800">
          <p><strong>Step 1:</strong> Generate sample data to populate the system with realistic attendance records</p>
          <p><strong>Step 2:</strong> Run AI analysis to process attendance data with 70% threshold rules</p>
          <p><strong>Step 3:</strong> Review detailed results with AI-powered insights and recommendations</p>
        </div>
      </div>
    </div>
  );

  const renderResults = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900">Attendance Analysis Results</h2>
        <button
          onClick={getAttendanceReport}
          disabled={loading}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-blue-700 transition-colors disabled:opacity-50"
        >
          Refresh Report
        </button>
      </div>

      {analysisResults && analysisResults.summary && (
        <div className="bg-white rounded-xl shadow-md p-6">
          <h3 className="text-lg font-semibold mb-4">Summary</h3>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="text-center">
              <p className="text-2xl font-bold text-blue-600">{analysisResults.summary.total_employees}</p>
              <p className="text-sm text-gray-600">Total Employees</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-green-600">{analysisResults.summary.meeting_70_percent_threshold}</p>
              <p className="text-sm text-gray-600">Meeting 70% Threshold</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-red-600">{analysisResults.summary.below_threshold}</p>
              <p className="text-sm text-gray-600">Below Threshold</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-purple-600">{analysisResults.summary.average_attendance_rate}%</p>
              <p className="text-sm text-gray-600">Average Attendance</p>
            </div>
          </div>
        </div>
      )}

      {analysisResults && (analysisResults.detailed_results || analysisResults.results) && (
        <div className="space-y-4">
          {(analysisResults.detailed_results || analysisResults.results).map((result, index) => (
            <div key={index} className="bg-white rounded-xl shadow-md p-6">
              <div className="flex flex-col lg:flex-row lg:justify-between lg:items-start mb-4">
                <div className="flex-1">
                  <div className="flex items-center mb-2">
                    <h3 className="text-lg font-semibold text-gray-900 mr-3">{result.name}</h3>
                    <span className={getStatusBadge(result.status)}>
                      {result.status === 'meets_threshold' ? 'Meets Threshold' : 'Below Threshold'}
                    </span>
                  </div>
                  <p className="text-gray-600 mb-2">{result.employee_id} • {result.department}</p>
                  
                  <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-4">
                    <div>
                      <p className="text-sm text-gray-500">Attendance Rate</p>
                      <p className={`text-xl font-bold ${getStatusColor(result.status)}`}>
                        {result.attendance_percentage.toFixed(1)}%
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500">Present Days</p>
                      <p className="text-lg font-semibold text-gray-900">{result.present_days}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500">Absent Days</p>
                      <p className="text-lg font-semibold text-gray-900">{result.absent_days}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500">Late Days</p>
                      <p className="text-lg font-semibold text-gray-900">{result.late_days}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500">Total Days</p>
                      <p className="text-lg font-semibold text-gray-900">{result.total_days}</p>
                    </div>
                  </div>
                </div>
              </div>
              
              <div className="bg-gray-50 rounded-lg p-4">
                <h4 className="font-semibold text-gray-900 mb-2 flex items-center">
                  <svg className="w-5 h-5 text-blue-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                  AI Insights
                </h4>
                <p className="text-gray-700 leading-relaxed">{result.ai_insights}</p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Navigation */}
      <nav className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <svg className="w-8 h-8 text-blue-600 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
              <span className="text-xl font-bold text-gray-900">AI Attendance Analyzer</span>
            </div>
            <div className="flex space-x-1">
              <button
                onClick={() => setActiveTab('dashboard')}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  activeTab === 'dashboard'
                    ? 'bg-blue-100 text-blue-700'
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                }`}
              >
                Dashboard
              </button>
              <button
                onClick={() => setActiveTab('results')}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  activeTab === 'results'
                    ? 'bg-blue-100 text-blue-700'
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                }`}
              >
                Analysis Results
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
        {loading && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 flex items-center space-x-4">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
              <span className="text-lg font-medium">Processing...</span>
            </div>
          </div>
        )}

        {activeTab === 'dashboard' && renderDashboard()}
        {activeTab === 'results' && renderResults()}
      </main>
    </div>
  );
}

export default App;