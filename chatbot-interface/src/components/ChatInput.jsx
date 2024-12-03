import React, { useState } from "react";

const ChatInput = ({ onSendMessage }) => {
    const [input, setInput] = useState("");

    const handleSend = () => {
        if (input.trim() !== "") {
            onSendMessage(input);
            setInput("");
        }
    };

    return (
        <div style={styles.container}>
            <input
                style={styles.input}
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Type a message..."
            />
            <button style={styles.button} onClick={handleSend}>
                Send
            </button>
        </div>
    );
};

const styles = {
    container: {
        display: "flex",
        padding: "10px",
        borderTop: "1px solid #ccc",
    },
    input: {
        flex: 1,
        padding: "10px",
        fontSize: "16px",
        borderRadius: "5px",
        border: "1px solid #ccc",
    },
    button: {
        marginLeft: "10px",
        padding: "10px 15px",
        fontSize: "16px",
        backgroundColor: "#0084ff",
        color: "#fff",
        border: "none",
        borderRadius: "5px",
        cursor: "pointer",
    },
};

export default ChatInput;
