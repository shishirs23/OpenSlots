import React, { useState } from "react";

function App() {
  const [slots, setSlots] = useState([]);

  const getSlots = async () => {
    try {
      const res = await fetch("http://192.168.1.4:8000/free-slots");
      const data = await res.json();
      setSlots(data);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>OpenSlots</h1>

      <button onClick={getSlots}>Get Free Slots</button>

      {slots.map((dayData, index) => (
        <div key={index}>
          <h2>{dayData.day}</h2>

          {dayData.free_slots.map((slot, i) => (
            <p key={i}>
              {slot.start} - {slot.end}
            </p>
          ))}
        </div>
      ))}
    </div>
  );
}

export default App;