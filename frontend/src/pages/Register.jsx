import { useState } from "react";
import api from "../api";
import { useNavigate, Link } from "react-router-dom";

export default function Register() {
    const navigate = useNavigate();
    const [form, setForm] = useState({
        username: "",
        password: "",
        email: "",
        age: "",
        gender: "M",
        contact: "",
        height: "",
        weight: "",
        diet_preference: "veg",
    });

    const handleChange = (e) =>
        setForm({ ...form, [e.target.name]: e.target.value });

    const submit = async (e) => {
        e.preventDefault();
        try {
            await api.post("register/", form);
            navigate("/login");
        } catch (err) {
            alert("Registration failed");
        }
    };

    return (
        <div className="card" style={{ maxWidth: 900, margin: "40px auto" }}>
            <h2>Create your account</h2>
            <p style={{ color: "var(--muted)" }}>
                Basic information required to personalize your health plans.
            </p>

            <form onSubmit={submit}>
                <div className="grid-2">
                    <input name="username" placeholder="Username" onChange={handleChange} required />
                    <input name="email" type="email" placeholder="Email" onChange={handleChange} required />

                    <input name="password" type="password" placeholder="Password" onChange={handleChange} required />
                    <input name="age" type="number" placeholder="Age" onChange={handleChange} required />

                    <select name="gender" onChange={handleChange}>
                        <option value="M">Male</option>
                        <option value="F">Female</option>
                        <option value="OTHERS">Prefer not to say</option>
                    </select>

                    <input name="contact" placeholder="Contact number" onChange={handleChange} required />
                    <input name="height" type="number" step="0.01" placeholder="Height (cm)" onChange={handleChange} required />
                    <input name="weight" type="number" step="0.01" placeholder="Weight (kg)" onChange={handleChange} required />

                    <select name="diet_preference" onChange={handleChange}>
                        <option value="veg">Vegetarian</option>
                        <option value="non-veg">Non-Vegetarian</option>
                        <option value="vegan">Vegan</option>
                        <option value="keto">Keto</option>
                    </select>
                </div>

                <button className="btn-primary" style={{ marginTop: 28 }}>
                    Create Account
                </button>
            </form>

            <p style={{ marginTop: 20 }}>
                Already have an account? <Link to="/login">Login</Link>
            </p>
        </div>
    );
}

