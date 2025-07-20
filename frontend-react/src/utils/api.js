import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
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

export function isGreeting(message) {
  const greetings = ["help"];
  const normalized = message.trim().toLowerCase();
  // Only match if the message starts with a greeting word
  return greetings.some((greet) => normalized.startsWith(greet));
}
