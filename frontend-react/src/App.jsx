import { useState } from "react";
import "./App.css";
import Header from "./components/Header";
import WelcomeScreen from "./components/WelcomeScreen";
import ChatInterface from "./components/ChatInterface";
import ErrorToast from "./components/ErrorToast";

function App() {
  const [isWelcomeScreen, setIsWelcomeScreen] = useState(true);
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const startChat = () => {
    setIsWelcomeScreen(false);
    // Add welcome message from bot
    setTimeout(() => {
      const welcomeMessage = {
        id: Date.now(),
        type: "bot",
        text: '👋 Hello! I\'m your expense tracker assistant. You can:\n\n• Type expenses like: "coffee food 50 want today"\n• Say "hello" or "help" for instructions\n• Use natural language to describe your expenses\n\nWhat expense would you like to add?',
        timestamp: new Date(),
      };
      setMessages([welcomeMessage]);
    }, 300);
  };

  const startChatWithMessage = (message) => {
    startChat();
    // Process the message after a short delay
    setTimeout(() => {
      addMessage(message, "user");
    }, 500);
  };

  const addMessage = (text, type, expenseDetails = null) => {
    const newMessage = {
      id: Date.now() + Math.random(),
      type,
      text,
      timestamp: new Date(),
      expenseDetails,
    };
    setMessages((prev) => [...prev, newMessage]);
  };

  const showError = (message) => {
    setError(message);
    setTimeout(() => setError(null), 5000);
  };

  return (
    <div className="app">
      <Header />

      {isWelcomeScreen ? (
        <WelcomeScreen
          onStartChat={startChat}
          onStartChatWithMessage={startChatWithMessage}
        />
      ) : (
        <ChatInterface
          messages={messages}
          isLoading={isLoading}
          setIsLoading={setIsLoading}
          addMessage={addMessage}
          showError={showError}
        />
      )}

      {error && <ErrorToast message={error} onClose={() => setError(null)} />}
    </div>
  );
}

export default App;
