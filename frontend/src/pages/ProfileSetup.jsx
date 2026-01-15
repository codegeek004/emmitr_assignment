import { useEffect, useState } from "react";
import api from "../api";

export default function ProfileSetup() {
    /* ---------------- Fitness Info ---------------- */
    const [fitness, setFitness] = useState({
        fitness_goal: "",
        current_fitness_level: "beginner",
        workout_location: "home",
    });

    /* ---------------- Additional Info ---------------- */
    const [info, setInfo] = useState({
        smoking: false,
        drinking: false,
        stress_level: "low",
        injuries: "",
    });

    /* ---------------- Diseases ---------------- */
    const [diseases, setDiseases] = useState([]);
    const [newDisease, setNewDisease] = useState({
        name: "",
        level: "low",
        duration: "",
    });

    /* ---------------- Fetch existing data ---------------- */
    useEffect(() => {
        api.get("fitness_info/")
            .then(res => {
                if (res.data) setFitness(res.data);
            })
            .catch(() => { });

        api.get("user_info/")
            .then(res => {
                if (res.data) {
                    setInfo({
                        smoking: res.data.smoking,
                        drinking: res.data.drinking,
                        stress_level: res.data.stress_level,
                        injuries: res.data.injuries || "",
                    });
                }
            })
            .catch(() => { });

        api.get("diseases/")
            .then(res => setDiseases(res.data || []))
            .catch(() => { });
    }, []);

    /* ---------------- Save Profile ---------------- */
    const saveProfile = async () => {
        await api.put("fitness_info/", fitness);
        await api.put("user_info/", info);
        alert("Profile saved successfully");
    };

    /* ---------------- Add Disease ---------------- */
    const addDisease = async () => {
        if (!newDisease.name || !newDisease.duration) return;

        await api.post("diseases/", {
            name: newDisease.name,
            level: newDisease.level,
            duration: Number(newDisease.duration)
        });

        const res = await api.get("diseases/");
        setDiseases(res.data);

        setNewDisease({ name: "", level: "low", duration: "" });
    };

    /* ---------------- Delete Disease ---------------- */
    const deleteDisease = async (id) => {
        await api.delete("diseases/", {
            data: { id }
        });

        setDiseases(prev => prev.filter(d => d.id !== id));
    };


    return (
        <>
            {/* ---------------- Fitness Info ---------------- */}
            <div className="card">
                <h2>Fitness Information</h2>

                <div className="grid-2">
                    <input
                        placeholder="Fitness goal"
                        value={fitness.fitness_goal}
                        onChange={e =>
                            setFitness({ ...fitness, fitness_goal: e.target.value })
                        }
                    />

                    <select
                        value={fitness.current_fitness_level}
                        onChange={e =>
                            setFitness({
                                ...fitness,
                                current_fitness_level: e.target.value,
                            })
                        }
                    >
                        <option value="beginner">Beginner</option>
                        <option value="intermediate">Intermediate</option>
                        <option value="advanced">Advanced</option>
                    </select>

                    <select
                        value={fitness.workout_location}
                        onChange={e =>
                            setFitness({
                                ...fitness,
                                workout_location: e.target.value,
                            })
                        }
                    >
                        <option value="home">Home</option>
                        <option value="gym">Gym</option>
                        <option value="outdoor">Outdoor</option>
                    </select>
                </div>
            </div>

            {/* ---------------- Lifestyle ---------------- */}
            <div className="card">
                <h2>Lifestyle & Health</h2>

                <label>
                    <input
                        type="checkbox"
                        checked={info.smoking}
                        onChange={e =>
                            setInfo({ ...info, smoking: e.target.checked })
                        }
                    />{" "}
                    Smoking
                </label>

                <br /><br />

                <label>
                    <input
                        type="checkbox"
                        checked={info.drinking}
                        onChange={e =>
                            setInfo({ ...info, drinking: e.target.checked })
                        }
                    />{" "}
                    Drinking
                </label>

                <br /><br />

                <label>Stress Level</label>
                <select
                    value={info.stress_level}
                    onChange={e =>
                        setInfo({ ...info, stress_level: e.target.value })
                    }
                >
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                </select>

                <br /><br />

                <label>Injuries (optional)</label>
                <textarea
                    rows="3"
                    value={info.injuries}
                    onChange={e =>
                        setInfo({ ...info, injuries: e.target.value })
                    }
                    style={{
                        width: "100%",
                        padding: "12px",
                        borderRadius: "12px",
                    }}
                />
            </div>

            {/* ---------------- Diseases ---------------- */}
            <div className="card">
                <h2>Medical History (Optional)</h2>

                {diseases.length === 0 && (
                    <p style={{ color: "#64748b" }}>
                        No medical conditions added.
                    </p>
                )}

                {diseases.map(d => (
                    <div key={d.id} className="disease-row">
                        <span>
                            <strong>{d.name}</strong> • {d.duration} yrs • {d.level}
                        </span>
                        <button
                            className="btn-danger"
                            onClick={() => deleteDisease(d.id)}
                        >
                            Delete
                        </button>
                    </div>
                ))}

                <div className="grid-3" style={{ marginTop: 20 }}>
                    <input
                        placeholder="Disease name"
                        value={newDisease.name}
                        onChange={e =>
                            setNewDisease({ ...newDisease, name: e.target.value })
                        }
                    />

                    <input
                        type="number"
                        placeholder="Duration (years)"
                        value={newDisease.duration}
                        onChange={e =>
                            setNewDisease({
                                ...newDisease,
                                duration: e.target.value,
                            })
                        }
                    />

                    <select
                        value={newDisease.level}
                        onChange={e =>
                            setNewDisease({ ...newDisease, level: e.target.value })
                        }
                    >
                        <option value="low">Low</option>
                        <option value="medium">Medium</option>
                        <option value="high">High</option>
                    </select>
                </div>

                <div style={{ textAlign: "center", marginTop: 16 }}>
                    <button className="btn-accent" onClick={addDisease}>
                        Add Disease
                    </button>
                </div>
            </div>

            {/* ---------------- Save ---------------- */}
            <div style={{ textAlign: "center", marginBottom: 40 }}>
                <button className="btn-primary" onClick={saveProfile}>
                    Save Profile
                </button>
            </div>
        </>
    );
}

