import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Navbar from "./components/Navbar";
import Login from "./pages/Login";
import Register from "./pages/Register";
import ProfileSetup from "./pages/ProfileSetup";
import Dashboard from "./pages/Dashboard";
import "./App.css";

const PrivateRoute = ({ children }) =>
    localStorage.getItem("access_token") ? children : <Navigate to="/login" />;

export default function App() {
    return (
        <BrowserRouter>
            <Navbar />
            <div className="page">
                <div className="container centered">
                    <Routes>
                        <Route path="/login" element={<Login />} />
                        <Route path="/register" element={<Register />} />
                        <Route path="/setup" element={<PrivateRoute><ProfileSetup /></PrivateRoute>} />
                        <Route path="/" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
                    </Routes>
                </div>
            </div>

        </BrowserRouter>
    );
}

