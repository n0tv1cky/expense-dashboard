import React, { useState, useEffect } from "react";
import {
  PlusCircle,
  Trash2,
  RotateCcw,
  Calendar,
  TrendingUp,
  DollarSign,
  PieChart,
  Edit,
  Save,
  X,
  Filter,
  Search,
} from "lucide-react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart as RechartsPieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
} from "recharts";

const ExpenditureForecastApp = () => {
  // Sample data based on your Excel structure
  const [expenses, setExpenses] = useState([
    {
      id: 1,
      done: false,
      expenseDetails: "Parekatta Donation",
      category: "Essential",
      occurrence: 1,
      budget: 25000,
      totalSpend: 25000,
      month: "Dec",
      essential: "Must Do",
      deleted: false,
    },
    {
      id: 2,
      done: true,
      expenseDetails: "Maamu Gift",
      category: "Essential",
      occurrence: 1,
      budget: 2000,
      totalSpend: 2000,
      month: "Jun",
      essential: "Must Do",
      deleted: false,
    },
    {
      id: 3,
      done: false,
      expenseDetails: "Ather EMI",
      category: "Needs",
      occurrence: 12,
      budget: 7000,
      totalSpend: 42000,
      month: "",
      essential: "Essential",
      deleted: false,
    },
    {
      id: 4,
      done: false,
      expenseDetails: "Food (227 / day)",
      category: "Needs",
      occurrence: 12,
      budget: 5000,
      totalSpend: 60000,
      month: "",
      essential: "",
      deleted: false,
    },
    {
      id: 5,
      done: false,
      expenseDetails: "Netflix Subscription",
      category: "Wants",
      occurrence: 12,
      budget: 800,
      totalSpend: 9600,
      month: "",
      essential: "",
      deleted: false,
    },
  ]);

  const [trashedExpenses, setTrashedExpenses] = useState([]);
  const [editingId, setEditingId] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [filterCategory, setFilterCategory] = useState("All");
  const [activeTab, setActiveTab] = useState("dashboard");
  const [showAddForm, setShowAddForm] = useState(false);

  const [newExpense, setNewExpense] = useState({
    expenseDetails: "",
    category: "Needs",
    occurrence: 1,
    budget: 0,
    month: "",
    essential: "",
  });

  // Constants
  const categories = ["Essential", "Needs", "Wants", "Invest"];
  const essentialTypes = ["Must Do", "Essential", ""];
  const months = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
  ];
  const yearlyEarning = 1000000;
  const monthlyEarning = yearlyEarning / 12;

  // Filter expenses
  const filteredExpenses = expenses.filter(
    (expense) =>
      !expense.deleted &&
      expense.expenseDetails.toLowerCase().includes(searchTerm.toLowerCase()) &&
      (filterCategory === "All" || expense.category === filterCategory)
  );

  // Calculate summary data
  const summaryData = {
    totalBudget: expenses
      .filter((e) => !e.deleted)
      .reduce((sum, e) => sum + e.budget * e.occurrence, 0),
    totalSpent: expenses
      .filter((e) => !e.deleted && e.done)
      .reduce((sum, e) => sum + e.totalSpend, 0),
    monthlyExpenses: expenses
      .filter((e) => !e.deleted && e.occurrence === 12)
      .reduce((sum, e) => sum + e.budget, 0),
    oneTimeExpenses: expenses
      .filter((e) => !e.deleted && e.occurrence === 1)
      .reduce((sum, e) => sum + e.budget, 0),
  };

  // Chart data
  const categoryData = categories.map((category) => {
    const categoryExpenses = expenses.filter(
      (e) => !e.deleted && e.category === category
    );
    const total = categoryExpenses.reduce(
      (sum, e) => sum + e.budget * e.occurrence,
      0
    );
    return { name: category, value: total, count: categoryExpenses.length };
  });

  const monthlyTrendData = months.map((month) => {
    const monthExpenses = expenses.filter(
      (e) => !e.deleted && e.month === month
    );
    const total = monthExpenses.reduce((sum, e) => sum + e.budget, 0);
    return { month, expenses: total, budget: monthlyEarning * 0.4 };
  });

  const COLORS = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7"];

  // CRUD Operations
  const addExpense = () => {
    if (!newExpense.expenseDetails.trim()) return;

    const expense = {
      id: Date.now(),
      done: false,
      ...newExpense,
      budget: parseFloat(newExpense.budget) || 0,
      totalSpend: parseFloat(newExpense.budget) * newExpense.occurrence || 0,
      deleted: false,
    };

    setExpenses([...expenses, expense]);
    setNewExpense({
      expenseDetails: "",
      category: "Needs",
      occurrence: 1,
      budget: 0,
      month: "",
      essential: "",
    });
    setShowAddForm(false);
  };

  const updateExpense = (id, updates) => {
    setExpenses(
      expenses.map((expense) =>
        expense.id === id
          ? {
              ...expense,
              ...updates,
              totalSpend:
                (updates.budget || expense.budget) *
                (updates.occurrence || expense.occurrence),
            }
          : expense
      )
    );
    setEditingId(null);
  };

  const deleteExpense = (id) => {
    setExpenses(
      expenses.map((expense) =>
        expense.id === id ? { ...expense, deleted: true } : expense
      )
    );
    const deletedExpense = expenses.find((e) => e.id === id);
    setTrashedExpenses([
      ...trashedExpenses,
      { ...deletedExpense, deletedAt: new Date() },
    ]);
  };

  const restoreExpense = (id) => {
    setExpenses(
      expenses.map((expense) =>
        expense.id === id ? { ...expense, deleted: false } : expense
      )
    );
    setTrashedExpenses(trashedExpenses.filter((e) => e.id !== id));
  };

  const toggleDone = (id) => {
    setExpenses(
      expenses.map((expense) =>
        expense.id === id ? { ...expense, done: !expense.done } : expense
      )
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Header */}
      <header className="bg-white shadow-lg border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center space-x-3">
              <div className="bg-gradient-to-r from-blue-600 to-purple-600 p-3 rounded-xl">
                <TrendingUp className="h-8 w-8 text-white" />
              </div>
              <div>
                <h1 className="text-3xl font-bold text-gray-900">
                  Expenditure Forecast
                </h1>
                <p className="text-gray-600">
                  Smart expense tracking and financial planning
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-right">
                <p className="text-sm text-gray-600">Annual Earning</p>
                <p className="text-2xl font-bold text-green-600">
                  ₹{yearlyEarning.toLocaleString()}
                </p>
              </div>
            </div>
          </div>

          {/* Navigation */}
          <nav className="flex space-x-8 pb-4">
            {["dashboard", "expenses", "trash"].map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`px-4 py-2 font-medium capitalize transition-all ${
                  activeTab === tab
                    ? "text-blue-600 border-b-2 border-blue-600"
                    : "text-gray-600 hover:text-blue-600"
                }`}
              >
                {tab}
              </button>
            ))}
          </nav>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Dashboard Tab */}
        {activeTab === "dashboard" && (
          <div className="space-y-8">
            {/* Summary Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="bg-white rounded-xl shadow-lg p-6 border border-slate-200">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">
                      Total Budget
                    </p>
                    <p className="text-2xl font-bold text-gray-900">
                      ₹{summaryData.totalBudget.toLocaleString()}
                    </p>
                  </div>
                  <DollarSign className="h-8 w-8 text-blue-500" />
                </div>
                <p className="text-xs text-gray-500 mt-2">
                  {((summaryData.totalBudget / yearlyEarning) * 100).toFixed(1)}
                  % of annual income
                </p>
              </div>

              <div className="bg-white rounded-xl shadow-lg p-6 border border-slate-200">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">
                      Total Spent
                    </p>
                    <p className="text-2xl font-bold text-green-600">
                      ₹{summaryData.totalSpent.toLocaleString()}
                    </p>
                  </div>
                  <TrendingUp className="h-8 w-8 text-green-500" />
                </div>
                <p className="text-xs text-gray-500 mt-2">
                  {summaryData.totalBudget > 0
                    ? (
                        (summaryData.totalSpent / summaryData.totalBudget) *
                        100
                      ).toFixed(1)
                    : 0}
                  % of budget used
                </p>
              </div>

              <div className="bg-white rounded-xl shadow-lg p-6 border border-slate-200">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">
                      Monthly Expenses
                    </p>
                    <p className="text-2xl font-bold text-orange-600">
                      ₹{summaryData.monthlyExpenses.toLocaleString()}
                    </p>
                  </div>
                  <Calendar className="h-8 w-8 text-orange-500" />
                </div>
                <p className="text-xs text-gray-500 mt-2">
                  {(
                    (summaryData.monthlyExpenses / monthlyEarning) *
                    100
                  ).toFixed(1)}
                  % of monthly income
                </p>
              </div>

              <div className="bg-white rounded-xl shadow-lg p-6 border border-slate-200">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">
                      One-time Expenses
                    </p>
                    <p className="text-2xl font-bold text-purple-600">
                      ₹{summaryData.oneTimeExpenses.toLocaleString()}
                    </p>
                  </div>
                  <PieChart className="h-8 w-8 text-purple-500" />
                </div>
                <p className="text-xs text-gray-500 mt-2">
                  Annual special expenses
                </p>
              </div>
            </div>

            {/* Charts */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* Category Distribution */}
              <div className="bg-white rounded-xl shadow-lg p-6 border border-slate-200">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                  Expense by Category
                </h3>
                <ResponsiveContainer width="100%" height={300}>
                  <RechartsPieChart>
                    <Pie
                      data={categoryData}
                      cx="50%"
                      cy="50%"
                      outerRadius={100}
                      fill="#8884d8"
                      dataKey="value"
                      label={({ name, value }) =>
                        `${name}: ₹${value.toLocaleString()}`
                      }
                    >
                      {categoryData.map((entry, index) => (
                        <Cell
                          key={`cell-${index}`}
                          fill={COLORS[index % COLORS.length]}
                        />
                      ))}
                    </Pie>
                    <Tooltip
                      formatter={(value) => [
                        `₹${value.toLocaleString()}`,
                        "Amount",
                      ]}
                    />
                  </RechartsPieChart>
                </ResponsiveContainer>
              </div>

              {/* Monthly Trend */}
              <div className="bg-white rounded-xl shadow-lg p-6 border border-slate-200">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                  Monthly Expense Trend
                </h3>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={monthlyTrendData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis />
                    <Tooltip
                      formatter={(value) => [
                        `₹${value.toLocaleString()}`,
                        "Amount",
                      ]}
                    />
                    <Line
                      type="monotone"
                      dataKey="expenses"
                      stroke="#8884d8"
                      strokeWidth={2}
                    />
                    <Line
                      type="monotone"
                      dataKey="budget"
                      stroke="#82ca9d"
                      strokeWidth={2}
                      strokeDasharray="5 5"
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Category Breakdown */}
            <div className="bg-white rounded-xl shadow-lg p-6 border border-slate-200">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Category Breakdown
              </h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={categoryData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip
                    formatter={(value) => [
                      `₹${value.toLocaleString()}`,
                      "Amount",
                    ]}
                  />
                  <Bar dataKey="value" fill="#8884d8" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}

        {/* Expenses Tab */}
        {activeTab === "expenses" && (
          <div className="space-y-6">
            {/* Controls */}
            <div className="bg-white rounded-xl shadow-lg p-6 border border-slate-200">
              <div className="flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
                <div className="flex flex-col sm:flex-row gap-4 flex-1">
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                    <input
                      type="text"
                      placeholder="Search expenses..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>

                  <div className="relative">
                    <Filter className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                    <select
                      value={filterCategory}
                      onChange={(e) => setFilterCategory(e.target.value)}
                      className="pl-10 pr-8 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent appearance-none bg-white"
                    >
                      <option value="All">All Categories</option>
                      {categories.map((cat) => (
                        <option key={cat} value={cat}>
                          {cat}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>

                <button
                  onClick={() => setShowAddForm(true)}
                  className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  <PlusCircle className="h-4 w-4" />
                  <span>Add Expense</span>
                </button>
              </div>
            </div>

            {/* Add Form */}
            {showAddForm && (
              <div className="bg-white rounded-xl shadow-lg p-6 border border-slate-200">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                  Add New Expense
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  <input
                    type="text"
                    placeholder="Expense details"
                    value={newExpense.expenseDetails}
                    onChange={(e) =>
                      setNewExpense({
                        ...newExpense,
                        expenseDetails: e.target.value,
                      })
                    }
                    className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />

                  <select
                    value={newExpense.category}
                    onChange={(e) =>
                      setNewExpense({ ...newExpense, category: e.target.value })
                    }
                    className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    {categories.map((cat) => (
                      <option key={cat} value={cat}>
                        {cat}
                      </option>
                    ))}
                  </select>

                  <input
                    type="number"
                    placeholder="Budget amount"
                    value={newExpense.budget}
                    onChange={(e) =>
                      setNewExpense({ ...newExpense, budget: e.target.value })
                    }
                    className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />

                  <input
                    type="number"
                    placeholder="Occurrence"
                    value={newExpense.occurrence}
                    onChange={(e) =>
                      setNewExpense({
                        ...newExpense,
                        occurrence: parseInt(e.target.value) || 1,
                      })
                    }
                    className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />

                  <select
                    value={newExpense.month}
                    onChange={(e) =>
                      setNewExpense({ ...newExpense, month: e.target.value })
                    }
                    className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="">Select Month</option>
                    {months.map((month) => (
                      <option key={month} value={month}>
                        {month}
                      </option>
                    ))}
                  </select>

                  <select
                    value={newExpense.essential}
                    onChange={(e) =>
                      setNewExpense({
                        ...newExpense,
                        essential: e.target.value,
                      })
                    }
                    className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="">Not Essential</option>
                    <option value="Essential">Essential</option>
                    <option value="Must Do">Must Do</option>
                  </select>
                </div>

                <div className="flex justify-end space-x-3 mt-4">
                  <button
                    onClick={() => setShowAddForm(false)}
                    className="px-4 py-2 text-gray-600 hover:text-gray-800 transition-colors"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={addExpense}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                  >
                    Add Expense
                  </button>
                </div>
              </div>
            )}

            {/* Expenses List */}
            <div className="bg-white rounded-xl shadow-lg border border-slate-200 overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Status
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Expense
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Category
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Budget
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Occurrence
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Total
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Month
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Priority
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Actions
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {filteredExpenses.map((expense) => (
                      <ExpenseRow
                        key={expense.id}
                        expense={expense}
                        editingId={editingId}
                        setEditingId={setEditingId}
                        updateExpense={updateExpense}
                        deleteExpense={deleteExpense}
                        toggleDone={toggleDone}
                        categories={categories}
                        essentialTypes={essentialTypes}
                        months={months}
                      />
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* Trash Tab */}
        {activeTab === "trash" && (
          <div className="space-y-6">
            <div className="bg-white rounded-xl shadow-lg p-6 border border-slate-200">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Deleted Expenses
              </h3>
              {trashedExpenses.length === 0 ? (
                <div className="text-center py-8">
                  <Trash2 className="mx-auto h-12 w-12 text-gray-400" />
                  <h3 className="mt-2 text-sm font-medium text-gray-900">
                    No deleted expenses
                  </h3>
                  <p className="mt-1 text-sm text-gray-500">
                    Your trash is empty.
                  </p>
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Expense
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Category
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Budget
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Deleted On
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Actions
                        </th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {trashedExpenses.map((expense) => (
                        <tr key={expense.id}>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            {expense.expenseDetails}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <span
                              className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getCategoryColor(
                                expense.category
                              )}`}
                            >
                              {expense.category}
                            </span>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            ₹{expense.budget.toLocaleString()}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {expense.deletedAt
                              ? new Date(expense.deletedAt).toLocaleDateString()
                              : "Unknown"}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                            <button
                              onClick={() => restoreExpense(expense.id)}
                              className="text-blue-600 hover:text-blue-900 flex items-center space-x-1"
                            >
                              <RotateCcw className="h-4 w-4" />
                              <span>Restore</span>
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

// Expense Row Component
const ExpenseRow = ({
  expense,
  editingId,
  setEditingId,
  updateExpense,
  deleteExpense,
  toggleDone,
  categories,
  essentialTypes,
  months,
}) => {
  const [editData, setEditData] = useState(expense);
  const isEditing = editingId === expense.id;

  const handleSave = () => {
    updateExpense(expense.id, editData);
  };

  const handleCancel = () => {
    setEditData(expense);
    setEditingId(null);
  };

  const getCategoryColor = (category) => {
    const colors = {
      Essential: "bg-red-100 text-red-800",
      Needs: "bg-blue-100 text-blue-800",
      Wants: "bg-green-100 text-green-800",
      Invest: "bg-purple-100 text-purple-800",
    };
    return colors[category] || "bg-gray-100 text-gray-800";
  };

  const getPriorityColor = (essential) => {
    const colors = {
      "Must Do": "bg-red-100 text-red-800",
      Essential: "bg-orange-100 text-orange-800",
      "": "bg-gray-100 text-gray-800",
    };
    return colors[essential] || "bg-gray-100 text-gray-800";
  };

  return (
    <tr className={expense.done ? "bg-green-50" : ""}>
      <td className="px-6 py-4 whitespace-nowrap">
        <button
          onClick={() => toggleDone(expense.id)}
          className={`w-5 h-5 rounded border-2 flex items-center justify-center ${
            expense.done
              ? "bg-green-500 border-green-500 text-white"
              : "border-gray-300 hover:border-green-500"
          }`}
        >
          {expense.done && <span className="text-xs">✓</span>}
        </button>
      </td>

      <td className="px-6 py-4">
        {isEditing ? (
          <input
            type="text"
            value={editData.expenseDetails}
            onChange={(e) =>
              setEditData({ ...editData, expenseDetails: e.target.value })
            }
            className="w-full px-2 py-1 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
          />
        ) : (
          <div className="text-sm text-gray-900">{expense.expenseDetails}</div>
        )}
      </td>

      <td className="px-6 py-4 whitespace-nowrap">
        {isEditing ? (
          <select
            value={editData.category}
            onChange={(e) =>
              setEditData({ ...editData, category: e.target.value })
            }
            className="px-2 py-1 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
          >
            {categories.map((cat) => (
              <option key={cat} value={cat}>
                {cat}
              </option>
            ))}
          </select>
        ) : (
          <span
            className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getCategoryColor(
              expense.category
            )}`}
          >
            {expense.category}
          </span>
        )}
      </td>

      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
        {isEditing ? (
          <input
            type="number"
            value={editData.budget}
            onChange={(e) =>
              setEditData({
                ...editData,
                budget: parseFloat(e.target.value) || 0,
              })
            }
            className="w-20 px-2 py-1 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
          />
        ) : (
          `₹${expense.budget.toLocaleString()}`
        )}
      </td>

      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
        {isEditing ? (
          <input
            type="number"
            value={editData.occurrence}
            onChange={(e) =>
              setEditData({
                ...editData,
                occurrence: parseInt(e.target.value) || 1,
              })
            }
            className="w-16 px-2 py-1 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
          />
        ) : (
          expense.occurrence
        )}
      </td>

      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
        ₹{(expense.budget * expense.occurrence).toLocaleString()}
      </td>

      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
        {isEditing ? (
          <select
            value={editData.month}
            onChange={(e) =>
              setEditData({ ...editData, month: e.target.value })
            }
            className="px-2 py-1 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Select Month</option>
            {months.map((month) => (
              <option key={month} value={month}>
                {month}
              </option>
            ))}
          </select>
        ) : (
          expense.month || "-"
        )}
      </td>

      <td className="px-6 py-4 whitespace-nowrap">
        {isEditing ? (
          <select
            value={editData.essential}
            onChange={(e) =>
              setEditData({ ...editData, essential: e.target.value })
            }
            className="px-2 py-1 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Not Essential</option>
            <option value="Essential">Essential</option>
            <option value="Must Do">Must Do</option>
          </select>
        ) : (
          <span
            className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getPriorityColor(
              expense.essential
            )}`}
          >
            {expense.essential || "Normal"}
          </span>
        )}
      </td>

      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
        <div className="flex items-center space-x-2">
          {isEditing ? (
            <>
              <button
                onClick={handleSave}
                className="text-green-600 hover:text-green-900"
              >
                <Save className="h-4 w-4" />
              </button>
              <button
                onClick={handleCancel}
                className="text-gray-600 hover:text-gray-900"
              >
                <X className="h-4 w-4" />
              </button>
            </>
          ) : (
            <>
              <button
                onClick={() => setEditingId(expense.id)}
                className="text-blue-600 hover:text-blue-900"
              >
                <Edit className="h-4 w-4" />
              </button>
              <button
                onClick={() => deleteExpense(expense.id)}
                className="text-red-600 hover:text-red-900"
              >
                <Trash2 className="h-4 w-4" />
              </button>
            </>
          )}
        </div>
      </td>
    </tr>
  );
};

// Helper function for category colors
const getCategoryColor = (category) => {
  const colors = {
    Essential: "bg-red-100 text-red-800",
    Needs: "bg-blue-100 text-blue-800",
    Wants: "bg-green-100 text-green-800",
    Invest: "bg-purple-100 text-purple-800",
  };
  return colors[category] || "bg-gray-100 text-gray-800";
};

export default ExpenditureForecastApp;
