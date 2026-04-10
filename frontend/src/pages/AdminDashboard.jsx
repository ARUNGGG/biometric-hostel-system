import React, { useState, useEffect, useRef } from 'react';
import Webcam from 'react-webcam';

function AdminDashboard() {
  const [logs, setLogs] = useState([]);
  const [students, setStudents] = useState([]);
  const [error, setError] = useState('');
  const [successMsg, setSuccessMsg] = useState('');
  const [selectedStudentId, setSelectedStudentId] = useState('');
  const [newStudentName, setNewStudentName] = useState('');
  const [newStudentRoll, setNewStudentRoll] = useState('');
  const [newStudentEmail, setNewStudentEmail] = useState('');
  const [newStudentPass, setNewStudentPass] = useState('');
  const [createMsg, setCreateMsg] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [networks, setNetworks] = useState([]);
  const [newNetworkSubnet, setNewNetworkSubnet] = useState('');
  const [newNetworkDesc, setNewNetworkDesc] = useState('');
  const [myIp, setMyIp] = useState('');
  const webcamRef = useRef(null);

  const fetchNetworks = async () => {
    try {
      const res = await fetch('https://biometric-hostel-system.onrender.com/api/admin/networks', {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
      });
      if (res.ok) setNetworks(await res.json());
    } catch (err) {}
  };

  const fetchMyIp = async () => {
    try {
      const res = await fetch('https://biometric-hostel-system.onrender.com/api/admin/my-ip');
      if (res.ok) {
        const data = await res.json();
        setMyIp(data.ip);
      }
    } catch (err) {}
  };

  const fetchLogs = async () => {
    try {
      const res = await fetch('https://biometric-hostel-system.onrender.com/api/admin/attendance', {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
      });
      if (res.ok) setLogs(await res.json());
      else setError('Failed to fetch logs. Are you an admin?');
    } catch (err) {
      setError('Network error accessing admin logs');
    }
  };

  const fetchStudents = async () => {
    try {
      const res = await fetch('https://biometric-hostel-system.onrender.com/api/admin/students', {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
      });
      if (res.ok) setStudents(await res.json());
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchLogs();
    fetchStudents();
    fetchNetworks();
    fetchMyIp();
  }, []);

  const handleAddNetwork = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch('https://biometric-hostel-system.onrender.com/api/admin/add-network', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${localStorage.getItem('token')}` },
        body: JSON.stringify({ subnet: newNetworkSubnet, description: newNetworkDesc })
      });
      if (res.ok) {
        setNewNetworkSubnet(''); setNewNetworkDesc('');
        fetchNetworks();
      }
    } catch (err) {}
  };

  const handleRemoveNetwork = async (id) => {
    if (!window.confirm('Are you sure you want to remove this network security layer completely?')) return;
    try {
      await fetch(`https://biometric-hostel-system.onrender.com/api/admin/remove-network/${id}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
      });
      fetchNetworks();
    } catch (err) {}
  };

  const handleCreateStudent = async (e) => {
    e.preventDefault();
    setCreateMsg('');
    try {
      const res = await fetch('https://biometric-hostel-system.onrender.com/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: newStudentName,
          roll_number: newStudentRoll,
          email: newStudentEmail,
          password: newStudentPass,
          role: 'student'
        })
      });
      if (res.ok) {
        setCreateMsg('Student created successfully!');
        setNewStudentName(''); setNewStudentRoll(''); setNewStudentEmail(''); setNewStudentPass('');
        fetchStudents();
      } else {
        const d = await res.json();
        setCreateMsg(`Failed: ${d.detail || 'Error'}`);
      }
    } catch (err) {
      setCreateMsg('Network error');
    }
  };

  const handleRegisterFace = async () => {
    if (!selectedStudentId) {
      setError('Please select a student first');
      return;
    }
    setError('');
    setSuccessMsg('');
    const imageSrc = webcamRef.current.getScreenshot();
    
    try {
      const res = await fetch(`https://biometric-hostel-system.onrender.com/api/admin/add-embedding/${selectedStudentId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({ image_base64: imageSrc }),
      });

      if (res.ok) setSuccessMsg('Face successfully registered for student!');
      else {
        const d = await res.json();
        setError(d.detail || 'Failed to extract face embedding');
      }
    } catch (err) {
      setError('Network error mapping face');
    }
  };

  const handleRemoveStudent = async () => {
    if (!selectedStudentId) {
      setError('Please select a student first');
      return;
    }
    if (!window.confirm('Are you sure you want to permanently delete this student, their facial mappings, and their logs?')) return;
    
    setError('');
    setSuccessMsg('');
    try {
      const res = await fetch(`https://biometric-hostel-system.onrender.com/api/admin/remove-student/${selectedStudentId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
      });
      if (res.ok) {
        setSuccessMsg('Student and dependencies completely wiped!');
        setSelectedStudentId('');
        fetchStudents();
        fetchLogs();
      } else {
        const d = await res.json();
        setError(d.detail || 'Failed to remove student');
      }
    } catch (err) {
      setError('Network error');
    }
  };

  return (
    <div className="dashboard-container" style={{ maxWidth: '900px', display: 'flex', gap: '30px', flexWrap: 'wrap' }}>
      
      {/* Left Column: Register Face */}
      <div style={{ flex: '1 1 300px', textAlign: 'left' }}>
        <h2>Admin Management</h2>

        <div style={{ background: 'rgba(0,0,0,0.2)', padding: '15px', borderRadius: '8px', marginTop: '20px' }}>
          <h3>Create New Student</h3>
          {createMsg && <p style={{ fontSize: '14px', color: createMsg.includes('Failed') ? 'var(--error)' : 'var(--success)' }}>{createMsg}</p>}
          <form onSubmit={handleCreateStudent}>
            <input type="text" placeholder="Name" value={newStudentName} onChange={e => setNewStudentName(e.target.value)} required style={{ padding: '8px', marginBottom: '10px' }} />
            <input type="text" placeholder="Roll Number" value={newStudentRoll} onChange={e => setNewStudentRoll(e.target.value)} required style={{ padding: '8px', marginBottom: '10px' }} />
            <input type="email" placeholder="Email" value={newStudentEmail} onChange={e => setNewStudentEmail(e.target.value)} required style={{ padding: '8px', marginBottom: '10px' }} />
            <input type="password" placeholder="Password" value={newStudentPass} onChange={e => setNewStudentPass(e.target.value)} required style={{ padding: '8px', marginBottom: '10px' }} />
            <button type="submit" style={{ padding: '8px' }}>Create Student</button>
          </form>
        </div>
        
        <div style={{ background: 'rgba(0,0,0,0.2)', padding: '15px', borderRadius: '8px', marginTop: '20px' }}>
          <h3>Register Student Face</h3>
          {error && <p style={{ color: 'var(--error)', fontSize: '14px' }}>{error}</p>}
          {successMsg && <p style={{ color: 'var(--success)', fontSize: '14px' }}>{successMsg}</p>}
          
          <input 
            type="text" 
            placeholder="Search student by name or roll..." 
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            style={{ width: '100%', boxSizing: 'border-box', padding: '10px', marginBottom: '10px', borderRadius: '6px', background: 'rgba(0,0,0,0.3)', color: 'white', border: '1px solid var(--text-muted)' }}
          />
          <select 
            value={selectedStudentId} 
            onChange={(e) => setSelectedStudentId(e.target.value)}
            style={{ width: '100%', padding: '10px', marginBottom: '15px', borderRadius: '6px', background: 'transparent', color: 'var(--text-main)', border: '1px solid var(--primary)' }}
          >
            <option value="" style={{ color: 'black' }}>-- Select Student --</option>
            {students.filter(s => s.name.toLowerCase().includes(searchQuery.toLowerCase()) || s.roll_number.toLowerCase().includes(searchQuery.toLowerCase())).map(s => <option key={s.id} value={s.id} style={{ color: 'black' }}>{s.name} ({s.roll_number})</option>)}
          </select>
          <button onClick={handleRemoveStudent} style={{ width: '100%', padding: '10px', marginBottom: '15px', background: 'var(--error)', borderColor: 'var(--error)' }}>
            Remove Selected Student
          </button>

          <div className="webcam-wrapper" style={{ border: '1px solid var(--primary)' }}>
            <Webcam
              audio={false}
              ref={webcamRef}
              screenshotFormat="image/jpeg"
              width="100%"
              videoConstraints={{ facingMode: "user" }}
            />
          </div>
          <button onClick={handleRegisterFace} style={{ padding: '10px', marginTop: '10px' }}>
            Capture & Registry Face
          </button>
        </div>

        {/* Network Security Manager */}
        <div style={{ background: 'rgba(0,0,0,0.2)', padding: '15px', borderRadius: '8px', marginTop: '20px' }}>
          <h3>Network Security Layers</h3>
          <p style={{ fontSize: '13px', color: 'var(--text-muted)' }}>Your Global Host IP: <strong>{myIp || 'Detecting...'}</strong></p>
          
          <form onSubmit={handleAddNetwork}>
            <input type="text" placeholder="CIDR (e.g. 192.168.1.0/24 or 0.0.0.0/0)" value={newNetworkSubnet} onChange={e => setNewNetworkSubnet(e.target.value)} required style={{ padding: '8px', marginBottom: '10px' }} />
            <input type="text" placeholder="Description (e.g. Hostel Primary Wi-Fi)" value={newNetworkDesc} onChange={e => setNewNetworkDesc(e.target.value)} required style={{ padding: '8px', marginBottom: '10px' }} />
            <button type="submit" style={{ padding: '8px', background: 'var(--success)' }}>Add Allowed Subnet</button>
          </form>

          <div style={{ marginTop: '15px' }}>
            {networks.map(net => (
              <div key={net.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '10px', background: 'rgba(0,0,0,0.3)', marginBottom: '5px', borderRadius: '4px' }}>
                <span style={{ fontSize: '14px', textAlign: 'left' }}><strong>{net.subnet}</strong> <br/> <small style={{color:'var(--text-muted)'}}>{net.description}</small></span>
                <button onClick={() => handleRemoveNetwork(net.id)} style={{ width: 'auto', padding: '5px 10px', background: 'var(--error)', fontSize: '12px' }}>Revoke</button>
              </div>
            ))}
          </div>
        </div>
        
        <button onClick={() => {
          localStorage.removeItem('token');
          window.location.reload();
        }} style={{ marginTop: '30px', background: 'transparent', border: '1px solid var(--primary)' }}>
          Logout
        </button>
      </div>

      {/* Right Column: Logs */}
      <div style={{ flex: '2 1 400px', textAlign: 'left' }}>
        <h3>Recent Attendance Logs</h3>
        <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '10px', fontSize: '14px' }}>
          <thead>
            <tr style={{ borderBottom: '2px solid var(--primary)', textAlign: 'left' }}>
              <th style={{ padding: '8px' }}>User ID</th>
              <th style={{ padding: '8px' }}>Time</th>
              <th style={{ padding: '8px' }}>IP</th>
              <th style={{ padding: '8px' }}>Status</th>
            </tr>
          </thead>
          <tbody>
            {logs.map((log) => (
              <tr key={log.id} style={{ borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
                <td style={{ padding: '8px' }}>{log.student_id}</td>
                <td style={{ padding: '8px' }}>{new Date(log.timestamp).toLocaleString()}</td>
                <td style={{ padding: '8px' }}>{log.ip_address}</td>
                <td style={{ padding: '8px', color: log.status === 'success' ? 'var(--success)' : 'var(--error)' }}>
                  {log.status}
                </td>
              </tr>
            ))}
            {logs.length === 0 && <tr><td colSpan="4" style={{ padding: '8px', textAlign: 'center' }}>No logs found</td></tr>}
          </tbody>
        </table>
      </div>
      
    </div>
  );
}

export default AdminDashboard;
