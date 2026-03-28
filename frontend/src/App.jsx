import { useState, useEffect, useCallback } from 'react'
import './index.css'

function App() {
  const [rooms, setRooms] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  
  // New state for user input
  const [jNumber, setJNumber] = useState("J00741314")
  const [actionLoading, setActionLoading] = useState(false)

  const fetchRooms = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await fetch('http://localhost:5000/rooms')
      if (!response.ok) {
        throw new Error('Failed to fetch rooms')
      }
      const data = await response.json()
      setRooms(data)
    } catch (err) {
      console.error("Error fetching rooms:", err)
      setError("Could not connect to the server. Make sure the Flask API is running on port 5000.")
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchRooms()
  }, [fetchRooms])

  const handleRoomAction = async (roomId, endpoint) => {
    if (!jNumber || !jNumber.toUpperCase().startsWith('J')) {
      setError("Please enter a valid JagID (e.g., J00741314)")
      return
    }

    setActionLoading(true)
    setError(null)
    
    try {
      const response = await fetch(`http://localhost:5000/${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          jNumber: jNumber,
          roomId: roomId
        })
      })

      if (!response.ok) {
        const data = await response.json()
        throw new Error(data.error || `Failed to ${endpoint}`)
      }

      // Action succeeded, refresh the room list
      await fetchRooms()
    } catch (err) {
      console.error(`Error during ${endpoint}:`, err)
      setError(err.message)
    } finally {
      setActionLoading(false)
    }
  }

  return (
    <>
      <h1>Marx Library Room Tracker</h1>
      
      <div className="user-input">
        <label htmlFor="jNumber">JagID (J-Number):</label>
        <input 
          id="jNumber"
          type="text" 
          value={jNumber} 
          onChange={(e) => setJNumber(e.target.value)}
          placeholder="e.g. J00741314"
        />
      </div>

      <div className="controls">
        <button onClick={fetchRooms} disabled={loading || actionLoading}>
          {loading ? 'Refreshing...' : 'Refresh Rooms'}
        </button>
      </div>

      {error && (
        <div style={{ color: '#f87171', background: 'rgba(239,68,68,0.1)', padding: '1rem', borderRadius: '8px', marginBottom: '2rem', border: '1px solid rgba(239,68,68,0.2)'}}>
          {error}
        </div>
      )}

      {loading && !rooms.length ? (
        <div className="loader"></div>
      ) : (
        <div className="room-grid">
          {rooms.map((room) => (
            <div key={room.room_id} className="room-card">
              <div>
                <h2>Room {room.room_number}</h2>
                <p>Floor: {room.floor_level}</p>
                <div className={`status ${room.status === 'Available' ? 'available' : 'occupied'}`}>
                  {room.status}
                </div>
              </div>
              
              <div className="room-actions">
                {room.status === 'Available' ? (
                  <button 
                    className="action-btn check-in"
                    disabled={actionLoading}
                    onClick={() => handleRoomAction(room.room_id, 'occupy-room')}
                  >
                    Check In
                  </button>
                ) : (
                  <button 
                    className="action-btn check-out"
                    disabled={actionLoading}
                    onClick={() => handleRoomAction(room.room_id, 'checkout')}
                  >
                    Check Out
                  </button>
                )}
              </div>
            </div>
          ))}
          {rooms.length === 0 && !loading && !error && (
            <p style={{ color: '#94a3b8' }}>No rooms found. Please initialize the database with test data.</p>
          )}
        </div>
      )}
    </>
  )
}

export default App
