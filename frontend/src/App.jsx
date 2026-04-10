import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Attendance from './pages/Attendance';
import AdminDashboard from './pages/AdminDashboard';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token') || '');

  return (
    <div className="app-container">
      <Router>
        <Routes>
          <Route path="/" element={!token ? <Login setToken={setToken} /> : <Navigate to="/attendance" />} />
          <Route path="/attendance" element={token ? <Attendance /> : <Navigate to="/" />} />
          <Route path="/admin" element={token ? <AdminDashboard /> : <Navigate to="/" />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
