// src/App.jsx
import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Transactions from "./pages/Transactions";
import TaxSummary from "./pages/TaxSummary";
import Profile from "./pages/Profile";
import Sidebar from "./pages/Sidebar";
import Navbar from "./pages/Navbar";
import TaxInfo from "./pages/TaxInfo";
import "./styles/app.css";

// ✅ Auth Guard to Protect Routes
const PrivateRoute = ({ element }) => {
  const userId = localStorage.getItem("user_id");
  return userId ? element : <Navigate to="/" />;
};

function App() {
  return (
    <Router>
      <Routes>
        {/* ✅ Login & Register */}
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* ✅ Protect Routes After Login */}
        <Route
          path="/*"
          element={
            <div className="app-container">
              <Sidebar />
              <div className="main-content">
                <Navbar />
                <div className="content-area">
                  <Routes>
                    <Route path="/dashboard" element={<PrivateRoute element={<Dashboard />} />} />
                    <Route path="/transactions" element={<PrivateRoute element={<Transactions />} />} />
                    <Route path="/tax-summary" element={<PrivateRoute element={<TaxSummary />} />} />
                    <Route path="/profile" element={<PrivateRoute element={<Profile />} />} />
                    <Route path="/taxinfo" element={<PrivateRoute element={<TaxInfo />} />} />
                  </Routes>
                </div>
              </div>
            </div>
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
