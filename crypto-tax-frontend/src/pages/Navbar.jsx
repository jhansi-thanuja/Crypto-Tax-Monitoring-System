// src/pages/Navbar.jsx
import React from "react";
import { useNavigate } from "react-router-dom";
import "../styles/navbar.css";

const Navbar = () => {
  const navigate = useNavigate();

  // ✅ Handle Logout
  const handleLogout = () => {
    localStorage.removeItem("user_id"); // ✅ Clear user_id
    localStorage.removeItem("token"); // ✅ Clear token (if stored)
    navigate("/"); // ✅ Redirect to login page
  };

  return (
    <div className="navbar">
      <h3>Welcome to CryptoApp 🚀</h3>
      <div className="navbar-right">
  <button onClick={handleLogout} className="logout-btn">
    🚪 Logout
  </button>
</div>

    </div>
  );
};

export default Navbar;
