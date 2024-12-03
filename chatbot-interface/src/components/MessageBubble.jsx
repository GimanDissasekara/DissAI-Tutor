import React from "react";

const MessageBubble = ({ message, sender }) => {
    const isUser = sender === "user";

    return (
        <div
            style={{
                ...styles.bubble,
                backgroundColor: isUser ? "#0084ff" : "#e4e6eb",
                alignSelf: isUser ? "flex-end" : "flex-start",
                color: isUser ? "#fff" : "#000",
            }}
        >
            {message}
        </div>
    );
};

const styles = {
    bubble: {
        maxWidth: "70%",
        padding: "10px",
        margin: "5px 0",
        borderRadius: "15px",
    },
};

export default MessageBubble;
