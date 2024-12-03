import React, { useState } from "react";
import ChatInput from "./ChatInput";
import MessageBubble from "./MessageBubble";

const ChatWindow = () => {
    const [messages, setMessages] = useState([]);

    const handleSendMessage = (message) => {
        setMessages([...messages, { text: message, sender: "user" }]);

        // Simulate bot response (replace with API call)
        setTimeout(() => {
            setMessages((prevMessages) => [
                ...prevMessages,
                { text: `Bot says: ${message}`, sender: "bot" },
            ]);
        }, 1000);
    };

    return (
        <div style={styles.chatWindow}>
            <div style={styles.messageContainer}>
                {messages.map((msg, index) => (
                    <MessageBubble key={index} message={msg.text} sender={msg.sender} />
                ))}
            </div>
            <ChatInput onSendMessage={handleSendMessage} />
        </div>
    );
};

const styles = {
    chatWindow: {
        display: "flex",
        flexDirection: "column",
        height: "80vh",
        width: "400px",
        border: "1px solid #ccc",
        borderRadius: "8px",
        overflow: "hidden",
    },
    messageContainer: {
        flex: 1,
        overflowY: "auto",
        padding: "10px",
    },
};

export default ChatWindow;
