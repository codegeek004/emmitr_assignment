import { useState } from "react";
import api from "../api";
import { useNavigate, Link } from "react-router-dom";

export default function Login() {
    const navigate = useNavigate();
    const [form, setForm] = useState({ username: "", password: "" });

    const submit = async (e) => {
        e.preventDefault();
        try {
            const res = await api.post("login/", form);
            localStorage.setItem("access_token", res.data.access_token);
            localStorage.setItem("refresh_token", res.data.refresh_token);
            navigate("/setup");
        } catch {
            alert("Invalid credentials");
        }
    };

    return (
        <div className="card" style={{ maxWidth: 420, margin: "80px auto" }}>
            <h2>Welcome back</h2>
            <p style={{ color: "var(--muted)" }}>
                Login to access your personalized health dashboard.
            </p>

            <form onSubmit={submit}>
                <input
                    placeholder="Username"
                    onChange={(e) => setForm({ ...form, username: e.target.value })}
                    required
                />
                <br /><br />
                <input
                    type="password"
                    placeholder="Password"
                    onChange={(e) => setForm({ ...form, password: e.target.value })}
                    required
                />

                <button className="btn-primary" style={{ marginTop: 24 }}>
                    Login
                </button>
            </form>

            <p style={{ marginTop: 20 }}>
                New here? <Link to="/register">Create an account</Link>
            </p>
        </div>
    );
}

