import "./WelcomeScreen.css";

const EXAMPLE_EXPENSES = [
  { text: "coffee food 50 want today", label: "☕ Coffee Purchase" },
  {
    text: "uber transport 200 essential yesterday hdfc cc",
    label: "🚗 Uber Ride",
  },
  { text: "groceries 1200 essential 15 july icici cc", label: "🛒 Groceries" },
  { text: "haircut general 300 need", label: "✂️ Haircut" },
];

const CATEGORIES = [
  "food",
  "transport",
  "general",
  "entertainment",
  "health",
  "bills",
  "groceries",
  "meds",
  "clothing",
  "gadgets",
];

const IMPORTANCE_LEVELS = [
  { value: "essential", className: "tag--success" },
  { value: "need", className: "tag--warning" },
  { value: "want", className: "tag--info" },
  { value: "extra", className: "" },
  { value: "investment", className: "" },
];

const BANK_ACCOUNTS = [
  "HDFC",
  "ICICI CC 3009",
  "INDUSIND CC 6421",
  "HDFC CC 6409",
  "IND",
];

function WelcomeScreen({ onStartChat, onStartChatWithMessage }) {
  return (
    <div className="welcome-screen">
      <div className="welcome-content">
        <div className="welcome-icon">🤖</div>
        <h2>Welcome to your Personal Expense Tracker!</h2>
        <p className="welcome-description">
          Simply type your expenses in natural language and I'll parse them for
          you.
        </p>

        <div className="info-section">
          <h3>📝 How to use:</h3>
          <div className="example-format">
            <code>item category amount importance date bank</code>
          </div>
          <p className="format-description">
            Example: "coffee food 50 want today" or "uber transport 200
            essential yesterday hdfc cc"
          </p>
        </div>

        <div className="quick-examples">
          <h4>🚀 Try these examples:</h4>
          <div className="example-buttons">
            {EXAMPLE_EXPENSES.map((example, index) => (
              <button
                key={index}
                className="btn btn--outline example-btn"
                onClick={() => onStartChatWithMessage(example.text)}
              >
                {example.label}
              </button>
            ))}
          </div>
        </div>

        <div className="supported-options">
          <div className="option-group">
            <h5>📂 Categories:</h5>
            <div className="tags">
              {CATEGORIES.map((category) => (
                <span key={category} className="tag">
                  {category}
                </span>
              ))}
            </div>
          </div>

          <div className="option-group">
            <h5>⚡ Importance:</h5>
            <div className="tags">
              {IMPORTANCE_LEVELS.map((level) => (
                <span key={level.value} className={`tag ${level.className}`}>
                  {level.value}
                </span>
              ))}
            </div>
          </div>

          <div className="option-group">
            <h5>🏦 Bank Accounts:</h5>
            <div className="tags">
              {BANK_ACCOUNTS.map((bank) => (
                <span key={bank} className="tag">
                  {bank}
                </span>
              ))}
            </div>
          </div>
        </div>

        <button
          className="btn btn--primary start-chat-btn"
          onClick={onStartChat}
        >
          Start Chatting 💬
        </button>
      </div>
    </div>
  );
}

export default WelcomeScreen;
