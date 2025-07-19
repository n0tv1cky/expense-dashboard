# Expense Tracker Chatbot - React Frontend

A modern React frontend for the expense tracking chatbot, built with Vite for fast development and hot module replacement.

## Features

- 🤖 Interactive chatbot interface
- 💰 Natural language expense parsing
- 📱 Responsive design
- ⚡ Real-time expense processing
- 🎨 Modern UI with smooth animations
- 🔄 Auto-scrolling chat messages
- ❌ Error handling with toast notifications

## Technology Stack

- **React 19** - Latest React features
- **Vite** - Fast build tool and dev server
- **Axios** - HTTP client for API calls
- **Lucide React** - Beautiful icons
- **CSS Variables** - Consistent theming

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn
- Backend server running on `http://localhost:8000`

### Installation

1. Navigate to the frontend-react directory:

```bash
cd frontend-react
```

2. Install dependencies:

```bash
npm install
```

3. Start the development server:

```bash
npm run dev
```

4. Open your browser and navigate to `http://localhost:5173`

### Build for Production

```bash
npm run build
```

The built files will be in the `dist/` directory.

## Project Structure

```
src/
├── components/           # React components
│   ├── Header.jsx       # App header
│   ├── WelcomeScreen.jsx # Landing page
│   ├── ChatInterface.jsx # Main chat UI
│   ├── Message.jsx      # Chat message component
│   ├── ExpenseDetails.jsx # Expense details display
│   └── ErrorToast.jsx   # Error notifications
├── utils/
│   └── api.js          # API utilities
├── App.jsx             # Main app component
├── App.css             # Global styles
└── main.jsx            # App entry point
```

## API Integration

The frontend communicates with the FastAPI backend running on `http://localhost:8000`.

**Main endpoint:**

- `POST /api/v1/chatbot/chat` - Process expense messages

### Example Request

```javascript
{
  "text": "coffee food 50 want today"
}
```

### Example Response

```javascript
{
  "success": true,
  "response": "✅ Expense added successfully!",
  "parsed_expense": {
    "expense_name": "coffee",
    "category": "food",
    "amount": 50.0,
    "importance": "want",
    "bank_account": "HDFC",
    "assigned_date": "2025-07-19",
    "expense_type": "expense"
  }
}
```

## Usage

1. **Welcome Screen**: Start with example expenses or begin typing
2. **Chat Interface**: Type natural language expenses like:

   - "coffee food 50 want today"
   - "uber transport 200 essential yesterday hdfc cc"
   - "groceries 1200 essential 15 july icici cc"

3. **Categories**: food, transport, general, entertainment, health, bills, groceries, meds, clothing, gadgets
4. **Importance**: essential, need, want, extra, investment
5. **Banks**: HDFC, ICICI CC 3009, INDUSIND CC 6421, HDFC CC 6409, IND

## Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

### Customization

- **Colors**: Modify CSS variables in `App.css`
- **API Endpoint**: Change `API_BASE_URL` in `utils/api.js`
- **Components**: Add new components in `src/components/`

## Troubleshooting

### Backend Connection Issues

If you see "Demo Mode" messages, ensure:

1. Backend server is running on `http://localhost:8000`
2. CORS is properly configured in the backend
3. API endpoints are accessible

### Build Issues

- Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- Update Node.js to the latest LTS version
- Check for TypeScript errors in console

## Contributing

1. Follow the existing code structure
2. Use functional components with hooks
3. Add CSS modules for component-specific styles
4. Test with both successful and error scenarios
