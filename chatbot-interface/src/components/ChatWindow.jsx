import React, { useState } from 'react';
import axios from 'axios';

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState("");

  const handleSendMessage = async () => {
    if (userInput.trim()) {
      const newMessages = [...messages, { text: userInput, sender: 'user' }];
      setMessages(newMessages);
      setUserInput("");  // Clear input field

      try {
        // Sending user input to FastAPI backend
        const response = await axios.post('http://localhost:8000/chatbot/', {
          message: userInput
        });

        const botResponse = response.data.response;
        setMessages([...newMessages, { text: botResponse, sender: 'bot' }]);
      } catch (error) {
        console.error("Error sending message to FastAPI:", error);
      }
    }
  };

  return (
    <div style={{ padding: "20px", maxWidth: "400px", margin: "0 auto", border: "1px solid #ccc", borderRadius: "8px" }}>
      <div style={{ height: "300px", overflowY: "scroll", marginBottom: "10px" }}>
        {messages.map((msg, index) => (
          <div key={index} style={{ padding: "10px", marginBottom: "10px", backgroundColor: msg.sender === "user" ? "#0084ff" : "#e4e6eb", borderRadius: "8px", color: msg.sender === "user" ? "#fff" : "#000", textAlign: msg.sender === "user" ? "right" : "left" }}>
            {msg.text}
          </div>
        ))}
      </div>
      <input 
        type="text" 
        value={userInput} 
        onChange={(e) => setUserInput(e.target.value)} 
        placeholder="Type a message..." 
        style={{ padding: "10px", width: "80%" }} 
      />
      <button onClick={handleSendMessage} style={{ padding: "10px", width: "15%" }}>
        Send
      </button>
    </div>
  );
};

export default Chatbot;
