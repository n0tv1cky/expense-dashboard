import "./Header.css";

function Header() {
  return (
    <header className="chat-header">
      <div className="header-content">
        <h1 className="header-title">
          <span className="header-icon">💰</span>
          Expense Tracker Bot
        </h1>
        <p className="header-subtitle">
          Track your expenses with natural language
        </p>
      </div>
    </header>
  );
}

export default Header;
