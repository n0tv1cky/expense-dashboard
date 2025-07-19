import "./ExpenseDetails.css";

const EXPENSE_FIELDS = [
  { key: "expense_name", label: "📝 Name" },
  { key: "category", label: "📂 Category" },
  { key: "amount", label: "💰 Amount" },
  { key: "importance", label: "⚡ Importance" },
  { key: "bank_account", label: "🏦 Bank Account" },
  { key: "assigned_date", label: "📅 Date" },
  { key: "expense_type", label: "📋 Type" },
];

function ExpenseDetails({ details }) {
  const capitalizeFirst = (str) => {
    if (!str) return str;
    return str.charAt(0).toUpperCase() + str.slice(1);
  };

  const formatValue = (key, value) => {
    if (!value) return "Not specified";

    if (key === "amount") {
      return `₹${value}`;
    } else if (["importance", "category", "expense_type"].includes(key)) {
      return capitalizeFirst(value);
    }

    return value;
  };

  return (
    <div className="expense-details">
      <h4>📊 Expense Details</h4>

      {EXPENSE_FIELDS.map((field) => {
        const value = details[field.key];
        if (value === undefined || value === null) return null;

        return (
          <div key={field.key} className="expense-item">
            <div className="expense-label">{field.label}</div>
            <div className="expense-value">{formatValue(field.key, value)}</div>
          </div>
        );
      })}
    </div>
  );
}

export default ExpenseDetails;
