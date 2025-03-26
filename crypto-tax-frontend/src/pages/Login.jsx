import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/login.css"; // Ensure your styles are available

const Login = () => {
  const [formData, setFormData] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // Replace with your FastAPI endpoint
      const response = await fetch("http://127.0.0.1:8000/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem("user_id", data.user_id);  // ✅ Correct
        localStorage.setItem("token", data.token);
        localStorage.setItem("isLoggedIn", "true");
        navigate("/dashboard");
        
        const userId = localStorage.getItem("user_id");
        console.log("User ID:", userId);
        
        navigate("/dashboard");  // Redirect to dashboard after successful login
      } else {
        setError("Error logging in.");
      }
    } catch (err) {
      setError("Error connecting to the server.");
    }
  };

  return (
    <div className="container">
      <form className="form-container" onSubmit={handleSubmit}>
        <h2>Login</h2>
        {error && <p className="error">{error}</p>}
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={formData.email}
          onChange={handleChange}
          required
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleChange}
          required
        />
        <button type="submit">Login</button>
        <p>
          Don't have an account?{" "}
          <span onClick={() => navigate("/register")} className="link">
            Register here
          </span>
        </p>
      </form>
    </div>
  );
};

export default Login;
