import React, { useRef, useState, useCallback } from 'react';
import Webcam from 'react-webcam';
import { useNavigate } from 'react-router-dom';

function Attendance() {
  const webcamRef = useRef(null);
  const [status, setStatus] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const captureAndSend = useCallback(async () => {
    setLoading(true);
    setStatus('Capturing and verifying...');
    const imageSrc = webcamRef.current.getScreenshot();

    try {
      const res = await fetch('http://localhost:8000/api/attendance/mark', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({ image_base64: imageSrc }),
      });

      const data = await res.json();
      if (res.ok) {
        setStatus(`✅ ${data.message} (Confidence: ${(data.confidence_score*100).toFixed(1)}%)`);
      } else {
        setStatus(`❌ Error: ${data.detail || 'Network or Recognition failed'}`);
      }
    } catch (err) {
      setStatus('❌ Please ensure you are on the Hostel Network.');
    } finally {
      setLoading(false);
    }
  }, [webcamRef]);

  return (
    <div className="dashboard-container">
      <h2>Mark Your Attendance</h2>
      <div className="webcam-wrapper">
        <Webcam
          audio={false}
          ref={webcamRef}
          screenshotFormat="image/jpeg"
          width="100%"
          videoConstraints={{ facingMode: "user" }}
        />
      </div>
      <button onClick={captureAndSend} disabled={loading}>
        {loading ? 'Verifying...' : 'Capture Face'}
      </button>
      
      {status && <p style={{ marginTop: '20px', fontWeight: 'bold', color: status.includes('✅') ? 'var(--success)' : 'var(--error)' }}>{status}</p>}

      <button onClick={() => {
        localStorage.removeItem('token');
        window.location.reload();
      }} style={{ marginTop: '20px', background: 'transparent', border: '1px solid var(--primary)' }}>
        Logout
      </button>
    </div>
  );
}

export default Attendance;
