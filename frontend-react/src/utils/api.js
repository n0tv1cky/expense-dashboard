import axios from "axios";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
const API_ENDPOINT = `${API_BASE_URL}/api/v1/chatbot/chat`;

export const sendMessageToAPI = async (message) => {
  try {
    const response = await axios.post(API_ENDPOINT, { text: message });
    return response.data;
  } catch (error) {
    console.error("API Error:", error);
    throw error;
  }
};

export const isGreeting = (message) => {
  const greetings = ["hello", "hi", "hey", "help", "start"];
  const lowerMessage = message.toLowerCase();
  return greetings.some((greeting) => lowerMessage.includes(greeting));
};
