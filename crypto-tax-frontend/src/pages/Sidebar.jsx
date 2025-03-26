import React from "react";
import { Link } from "react-router-dom";
import {
  FaTachometerAlt,
  FaExchangeAlt,
  FaUser,
  FaChartPie,
  FaInfoCircle,
} from "react-icons/fa"; // ✅ Import FaInfoCircle for TaxInfo
import "../styles/sidebar.css";

const Sidebar = () => {
  return (
    <div className="sidebar">
      <div className="sidebar-logo">
        <h2>CryptoApp</h2>
      </div>
      <div className="sidebar-menu">
        <ul>
          <li>
            <Link to="/dashboard">
              <FaTachometerAlt className="icon" />
              <span>Dashboard</span>
            </Link>
          </li>
          <li>
            <Link to="/transactions">
              <FaExchangeAlt className="icon" />
              <span>Transactions</span>
            </Link>
          </li>
          <li>
            <Link to="/profile">
              <FaUser className="icon" />
              <span>Profile</span>
            </Link>
          </li>
          <li>
            <Link to="/tax-summary">
              <FaChartPie className="icon" />
              <span>Tax Summary</span>
            </Link>
          </li>
          <li>
            <Link to="/taxinfo">
              <FaInfoCircle className="icon" />
              <span>Tax Info</span> {/* ✅ Added Tax Info */}
            </Link>
          </li>
        </ul>
      </div>
    </div>
  );
};

export default Sidebar;
