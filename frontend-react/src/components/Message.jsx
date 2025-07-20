import ReactMarkdown from "react-markdown";
import ExpenseDetails from "./ExpenseDetails";
import "./Message.css";

function Message({ message }) {
  const formatTime = (timestamp) => {
    const now = new Date();
    const diff = now - timestamp;

    if (diff < 60000) return "Just now";
    if (diff < 3600000) return `${Math.floor(diff / 60000)}m ago`;
    if (diff < 86400000) return `${Math.floor(diff / 3600000)}h ago`;
    return timestamp.toLocaleDateString();
  };

  return (
    <div className={`message message--${message.type}`}>
      <div className="message-bubble">
        <div className="message-text">
          <ReactMarkdown>{message.text}</ReactMarkdown>
        </div>

        {message.expenseDetails && (
          <ExpenseDetails details={message.expenseDetails} />
        )}

        <div className="message-time">{formatTime(message.timestamp)}</div>
      </div>
    </div>
  );
}

export default Message;
