import { useState, useEffect, useRef } from "react";
import { Send, Loader2 } from "lucide-react";
import Message from "./Message";
import { sendMessageToAPI, isGreeting } from "../utils/api";
import "./ChatInterface.css";

function ChatInterface({
  messages,
  isLoading,
  setIsLoading,
  addMessage,
  showError,
}) {
  const [inputValue, setInputValue] = useState("");
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Focus input when component mounts
    inputRef.current?.focus();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    const message = inputValue.trim();
    if (!message || isLoading) return;

    // Add user message
    addMessage(message, "user");
    setInputValue("");
    setIsLoading(true);

    try {
      // Handle greetings
      if (isGreeting(message)) {
        setTimeout(() => {
          const greetingResponse =
            '👋 Hello! I can help you track your expenses. Here\'s how:\n\n📝 **Format**: item category amount importance date bank\n\n🔍 **Examples**:\n• "coffee food 50 want today"\n• "uber transport 200 essential yesterday hdfc cc"\n• "groceries 1200 essential 15 july icici cc"\n\n📂 **Categories**: food, transport, general, entertainment, health, bills, groceries, meds, clothing, gadgets\n\n⚡ **Importance**: essential, need, want, extra, investment\n\n🏦 **Banks**: HDFC, ICICI CC 3009, INDUSIND CC 6421, HDFC CC 6409, IND\n\nJust type your expense naturally!';
          addMessage(greetingResponse, "bot");
          setIsLoading(false);
        }, 1000);
        return;
      }

      // Send to API
      const response = await sendMessageToAPI(message);

      if (response.success) {
        let botMessage =
          response.response ||
          response.message ||
          "✅ Expense processed successfully!";

        // Extract expense details if available
        let expenseDetails = null;
        if (response.parsed_expense || response.expense_details) {
          expenseDetails = response.parsed_expense || response.expense_details;
        }

        addMessage(botMessage, "bot", expenseDetails);
      } else {
        addMessage(
          `❌ Sorry, I couldn't process that expense: ${
            response.error || response.message || "Unknown error"
          }\n\nPlease try again with a format like: \"coffee food 50 want today\"`,
          "bot"
        );
      }
    } catch (error) {
      console.error("API Error:", error);
      showError(`Failed to connect to server: ${error.message}`);

      // Add mock response for demo
      addMockResponse(message);
    } finally {
      setIsLoading(false);
    }
  };

  const addMockResponse = (message) => {
    const parts = message.toLowerCase().split(" ");
    const hasNumber = parts.some((part) => !isNaN(part));

    if (hasNumber) {
      const mockExpense = {
        expense_name: parts[0] || "Unknown Item",
        category: parts[1] || "general",
        amount: parts.find((p) => !isNaN(p)) || "0",
        importance:
          parts.find((p) =>
            ["essential", "need", "want", "extra"].includes(p)
          ) || "need",
        bank_account: parts.includes("hdfc")
          ? "HDFC"
          : parts.includes("icici")
          ? "ICICI"
          : "Not specified",
        assigned_date: parts.includes("today")
          ? "Today"
          : parts.includes("yesterday")
          ? "Yesterday"
          : "Today",
        expense_type: "expense",
      };

      addMessage(
        "✅ Great! I've parsed your expense (Demo Mode - Backend not connected):",
        "bot",
        mockExpense
      );
    } else {
      addMessage(
        "🔌 I'm running in demo mode since the backend server isn't available.\n\nTry typing an expense like: \"coffee food 50 want today\" to see how it would work!",
        "bot"
      );
    }
  };

  return (
    <div className="chat-interface">
      <div className="chat-messages">
        {messages.map((message) => (
          <Message key={message.id} message={message} />
        ))}
        {isLoading && (
          <div className="message message--bot">
            <div className="message-bubble">
              <div className="loading-indicator">
                <Loader2 className="loading-spinner" />
                <span>Processing...</span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form className="chat-form" onSubmit={handleSubmit}>
        <div className="input-container">
          <input
            ref={inputRef}
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Type your expense... e.g., 'coffee food 50 want today'"
            className="message-input"
            disabled={isLoading}
          />
          <button
            type="submit"
            className="send-button"
            disabled={!inputValue.trim() || isLoading}
          >
            <Send className="send-icon" />
          </button>
        </div>
      </form>
    </div>
  );
}

export default ChatInterface;
