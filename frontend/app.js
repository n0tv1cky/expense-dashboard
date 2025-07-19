// Application State
const state = {
    isWelcomeScreen: true,
    isLoading: false,
    messages: []
};

// DOM Elements
const welcomeScreen = document.getElementById('welcomeScreen');
const chatMessages = document.getElementById('chatMessages');
const chatForm = document.getElementById('chatForm');
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const startChatBtn = document.getElementById('startChatBtn');
const loadingOverlay = document.getElementById('loadingOverlay');
const errorToast = document.getElementById('errorToast');
const toastMessage = document.getElementById('toastMessage');
const toastClose = document.getElementById('toastClose');

// API Configuration
const API_BASE_URL = 'http://localhost:8000';
const API_ENDPOINT = `${API_BASE_URL}/api/v1/chatbot/chat`;

// Initialize Application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    console.log('Initializing Expense Tracker Chatbot...');
    
    // Event Listeners
    startChatBtn.addEventListener('click', handleStartChat);
    chatForm.addEventListener('submit', handleFormSubmit);
    toastClose.addEventListener('click', hideErrorToast);
    
    // Example button listeners
    const exampleBtns = document.querySelectorAll('.example-btn');
    exampleBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const example = this.getAttribute('data-example');
            console.log('Example clicked:', example);
            startChatWithMessage(example);
        });
    });

    // Enter key handling
    messageInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleFormSubmit(e);
        }
    });

    // Initialize chat messages container
    chatMessages.innerHTML = '';
}

function handleStartChat() {
    console.log('Starting chat...');
    startChat();
}

function startChat() {
    console.log('Transitioning to chat interface...');
    
    state.isWelcomeScreen = false;
    
    // Hide welcome screen and show chat interface
    welcomeScreen.classList.add('hidden');
    chatMessages.style.display = 'block';
    chatMessages.classList.add('active');
    
    // Clear existing messages and add welcome message
    chatMessages.innerHTML = '';
    state.messages = [];
    
    // Add welcome message from bot
    setTimeout(() => {
        addBotMessage("👋 Hello! I'm your expense tracker assistant. You can:\n\n• Type expenses like: \"coffee food 50 want today\"\n• Say \"hello\" or \"help\" for instructions\n• Use natural language to describe your expenses\n\nWhat expense would you like to add?");
        messageInput.focus();
    }, 300);
}

function startChatWithMessage(message) {
    console.log('Starting chat with message:', message);
    startChat();
    
    // Set the message after a short delay to ensure chat is ready
    setTimeout(() => {
        messageInput.value = message;
        setTimeout(() => {
            handleFormSubmit({ preventDefault: () => {} });
        }, 200);
    }, 500);
}

async function handleFormSubmit(e) {
    e.preventDefault();
    console.log('Form submitted');
    
    const message = messageInput.value.trim();
    if (!message || state.isLoading) {
        console.log('Empty message or loading, ignoring');
        return;
    }
    
    console.log('Processing message:', message);
    
    // Add user message immediately
    addUserMessage(message);
    messageInput.value = '';
    
    // Show loading
    setLoading(true);
    
    try {
        // Check if it's a greeting first
        if (isGreeting(message)) {
            console.log('Greeting detected');
            setTimeout(() => {
                addBotMessage("👋 Hello! I can help you track your expenses. Here's how:\n\n📝 **Format**: item category amount importance date bank\n\n🔍 **Examples**:\n• \"coffee food 50 want today\"\n• \"uber transport 200 essential yesterday hdfc cc\"\n• \"groceries 1200 essential 15 july icici cc\"\n\n📂 **Categories**: food, transport, general, entertainment, health, bills, groceries, meds, clothing, gadgets\n\n⚡ **Importance**: essential, need, want, extra, investment\n\n🏦 **Banks**: HDFC, ICICI CC 3009, INDUSIND CC 6421, HDFC CC 6409, IND\n\nJust type your expense naturally!");
                setLoading(false);
            }, 1000);
            return;
        }
        
        // Send message to API
        const response = await sendMessageToAPI(message);
        console.log('API response:', response);
        
        if (response.success) {
            addBotResponse(response);
        } else {
            addBotMessage(`❌ Sorry, I couldn't process that expense: ${response.error || 'Unknown error'}\n\nPlease try again with a format like: \"coffee food 50 want today\"`);
        }
    } catch (error) {
        console.error('API Error:', error);
        // Mock response for demo purposes when API is not available
        addMockResponse(message);
    } finally {
        setLoading(false);
    }
}

function addMockResponse(message) {
    console.log('Adding mock response for:', message);
    
    // Simple parsing for demo
    const parts = message.toLowerCase().split(' ');
    const hasNumber = parts.some(part => !isNaN(part));
    
    if (hasNumber) {
        // Mock expense parsing
        const mockExpense = {
            expense_name: parts[0] || 'Unknown Item',
            category: parts[1] || 'general',
            amount: parts.find(p => !isNaN(p)) || '0',
            importance: parts.find(p => ['essential', 'need', 'want', 'extra'].includes(p)) || 'need',
            bank_account: parts.includes('hdfc') ? 'HDFC' : parts.includes('icici') ? 'ICICI' : 'Not specified',
            assigned_date: parts.includes('today') ? 'Today' : parts.includes('yesterday') ? 'Yesterday' : 'Today',
            expense_type: 'expense'
        };
        
        const mockResponse = {
            success: true,
            message: "✅ Great! I've parsed your expense (Demo Mode - Backend not connected):",
            expense_details: mockExpense
        };
        
        addBotResponse(mockResponse);
    } else {
        addBotMessage("🔌 I'm running in demo mode since the backend server isn't available.\n\nTry typing an expense like: \"coffee food 50 want today\" to see how it would work!");
    }
}

async function sendMessageToAPI(message) {
    const response = await fetch(API_ENDPOINT, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message })
    });

    if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    return await response.json();
}

function addUserMessage(message) {
    console.log('Adding user message:', message);
    
    const messageObj = {
        type: 'user',
        text: message,
        timestamp: new Date()
    };
    
    state.messages.push(messageObj);
    renderMessage(messageObj);
    scrollToBottom();
}

function addBotMessage(message) {
    console.log('Adding bot message:', message);
    
    const messageObj = {
        type: 'bot',
        text: message,
        timestamp: new Date()
    };
    
    state.messages.push(messageObj);
    renderMessage(messageObj);
    scrollToBottom();
}

function addBotResponse(response) {
    console.log('Adding bot response:', response);
    
    let messageText = response.message || "✅ I've processed your expense!";
    
    const messageObj = {
        type: 'bot',
        text: messageText,
        timestamp: new Date(),
        expenseDetails: response.expense_details || null
    };
    
    state.messages.push(messageObj);
    renderMessage(messageObj);
    scrollToBottom();
}

function renderMessage(messageObj) {
    console.log('Rendering message:', messageObj.type, messageObj.text.substring(0, 50) + '...');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message message--${messageObj.type}`;
    
    const bubbleDiv = document.createElement('div');
    bubbleDiv.className = 'message-bubble';
    
    const textDiv = document.createElement('div');
    textDiv.className = 'message-text';
    textDiv.style.whiteSpace = 'pre-line';
    textDiv.textContent = messageObj.text;
    
    const timeDiv = document.createElement('div');
    timeDiv.className = 'message-time';
    timeDiv.textContent = formatTime(messageObj.timestamp);
    
    bubbleDiv.appendChild(textDiv);
    
    // Add expense details if available
    if (messageObj.expenseDetails) {
        const expenseDiv = createExpenseDetailsDiv(messageObj.expenseDetails);
        bubbleDiv.appendChild(expenseDiv);
    }
    
    bubbleDiv.appendChild(timeDiv);
    messageDiv.appendChild(bubbleDiv);
    
    // Add to DOM
    chatMessages.appendChild(messageDiv);
    
    console.log('Message rendered. Total messages in DOM:', chatMessages.children.length);
}

function createExpenseDetailsDiv(details) {
    const expenseDiv = document.createElement('div');
    expenseDiv.className = 'expense-details';
    
    const titleDiv = document.createElement('h4');
    titleDiv.textContent = '📊 Expense Details';
    expenseDiv.appendChild(titleDiv);
    
    const fields = [
        { key: 'expense_name', label: '📝 Name' },
        { key: 'category', label: '📂 Category' },
        { key: 'amount', label: '💰 Amount' },
        { key: 'importance', label: '⚡ Importance' },
        { key: 'bank_account', label: '🏦 Bank Account' },
        { key: 'assigned_date', label: '📅 Date' },
        { key: 'expense_type', label: '📋 Type' }
    ];
    
    fields.forEach(field => {
        if (details[field.key] !== undefined && details[field.key] !== null) {
            const itemDiv = document.createElement('div');
            itemDiv.className = 'expense-item';
            
            const labelDiv = document.createElement('div');
            labelDiv.className = 'expense-label';
            labelDiv.textContent = field.label;
            
            const valueDiv = document.createElement('div');
            valueDiv.className = 'expense-value';
            
            let displayValue = details[field.key];
            
            if (field.key === 'amount' && displayValue) {
                displayValue = `₹${displayValue}`;
            } else if (['importance', 'category', 'expense_type'].includes(field.key) && displayValue) {
                displayValue = capitalizeFirst(displayValue);
            }
            
            valueDiv.textContent = displayValue || 'Not specified';
            
            itemDiv.appendChild(labelDiv);
            itemDiv.appendChild(valueDiv);
            expenseDiv.appendChild(itemDiv);
        }
    });
    
    return expenseDiv;
}

function capitalizeFirst(str) {
    if (!str) return str;
    return str.charAt(0).toUpperCase() + str.slice(1);
}

function formatTime(timestamp) {
    const now = new Date();
    const diff = now - timestamp;
    
    if (diff < 60000) return 'Just now';
    if (diff < 3600000) return `${Math.floor(diff / 60000)}m ago`;
    if (diff < 86400000) return `${Math.floor(diff / 3600000)}h ago`;
    return timestamp.toLocaleDateString();
}

function scrollToBottom() {
    setTimeout(() => {
        chatMessages.scrollTop = chatMessages.scrollHeight;
        console.log('Scrolled to bottom');
    }, 100);
}

function setLoading(loading) {
    state.isLoading = loading;
    console.log('Loading state:', loading);
    
    if (loading) {
        loadingOverlay.classList.add('active');
        sendBtn.disabled = true;
        sendBtn.style.opacity = '0.6';
    } else {
        loadingOverlay.classList.remove('active');
        sendBtn.disabled = false;
        sendBtn.style.opacity = '1';
    }
}

function showErrorToast(message) {
    toastMessage.textContent = message;
    errorToast.classList.add('active');
    setTimeout(hideErrorToast, 5000);
}

function hideErrorToast() {
    errorToast.classList.remove('active');
}

function isGreeting(message) {
    const greetings = ['hello', 'hi', 'hey', 'help', 'start'];
    const lowerMessage = message.toLowerCase();
    return greetings.some(greeting => lowerMessage.includes(greeting));
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') hideErrorToast();
    
    if ((e.ctrlKey || e.metaKey) && e.key === '/') {
        e.preventDefault();
        if (!state.isWelcomeScreen) messageInput.focus();
    }
});

// Online/offline handling
window.addEventListener('offline', () => showErrorToast('You are offline. Please check your internet connection.'));

// Focus management
document.addEventListener('visibilitychange', function() {
    if (!document.hidden && !state.isWelcomeScreen) {
        messageInput.focus();
    }
});

console.log('💰 Expense Tracker Chatbot initialized successfully!');