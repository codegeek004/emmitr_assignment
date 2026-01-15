import { Link, useNavigate } from "react-router-dom";

export default function Navbar() {
    const navigate = useNavigate();
    const logout = () => {
        localStorage.clear();
        navigate("/login");
    };

    return (
        <nav className="navbar">
            <div className="nav-inner">
                <strong>EmmitrFit</strong>
                <div className="nav-links">
                    <Link to="/">Dashboard</Link>
                    <Link to="/setup">Profile</Link>
                    <button onClick={logout}>Logout</button>
                </div>
            </div>
        </nav>
    );
}

