import { useState } from "react";
import api from "../api";

export default function Dashboard() {
    const [workout, setWorkout] = useState(null);
    const [diet, setDiet] = useState(null);
    const [audio, setAudio] = useState(null);
    const [loading, setLoading] = useState(false);

    const generateWorkout = async () => {
        setLoading(true);
        setDiet(null);
        try {
            const res = await api.post("workout_plan/");
            setWorkout(res.data.workout_plan);
            setAudio(res.data.voice_response || null);
        } finally {
            setLoading(false);
        }
    };

    const generateDiet = async () => {
        setLoading(true);
        setWorkout(null);
        try {
            const res = await api.post("diet_plan/");
            setDiet(res.data.diet_plan);
            setAudio(res.data.voice_response || null);
        } finally {
            setLoading(false);
        }
    };

    return (
        <>
            {/* HERO */}
            <div className="hero">
                <h1>Your AI Health Coach</h1>
                <p>Personalized workout and diet plans generated just for you</p>

                <div className="hero-actions">
                    <button className="btn-primary" onClick={generateWorkout}>
                        Generate Workout Plan
                    </button>
                    <button className="btn-accent" onClick={generateDiet}>
                        Generate Diet Plan
                    </button>
                </div>
            </div>

            {/* LOADING */}
            {loading && (
                <div className="card" style={{ textAlign: "center" }}>
                    <strong>AI is thinking…</strong>
                </div>
            )}

            {/* WORKOUT PLAN */}
            {workout && (
                <div className="card">
                    <h2>Workout Overview</h2>
                    <p>{workout.overview}</p>

                    <h3 style={{ marginTop: 32 }}>Weekly Workout Plan</h3>

                    <div className="grid-2">
                        {Object.entries(workout.weekly_plan).map(([day, plan]) => (
                            <div key={day} className="card" style={{ textAlign: "center" }}>
                                <strong>{day.replace("_", " ").toUpperCase()}</strong>
                                <p style={{ marginTop: 12 }}>{plan}</p>
                            </div>
                        ))}
                    </div>

                    <h3 style={{ marginTop: 32 }}>Safety Notes</h3>
                    <p>{workout.safety_notes}</p>
                </div>
            )}

            {/* DIET PLAN */}
            {diet && (
                <div className="card">
                    <h2>Diet Overview</h2>
                    <p>{diet.overview}</p>

                    <h3 style={{ marginTop: 32 }}>Weekly Diet Plan</h3>

                    <table
                        style={{
                            width: "100%",
                            marginTop: 16,
                            borderCollapse: "collapse",
                            textAlign: "center",
                        }}
                    >
                        <thead>
                            <tr>
                                <th style={{ padding: 12 }}>Day</th>
                                <th style={{ padding: 12 }}>Meals</th>
                            </tr>
                        </thead>
                        <tbody>
                            {Object.entries(diet.weekly_plan).map(([day, meals]) => (
                                <tr key={day}>
                                    <td style={{ padding: 12, fontWeight: 600 }}>
                                        {day.replace("_", " ").toUpperCase()}
                                    </td>
                                    <td style={{ padding: 12 }}>{meals}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>

                    <h3 style={{ marginTop: 32 }}>Safety Notes</h3>
                    <p>{diet.safety_notes}</p>
                </div>
            )}

            {/* AUDIO */}
            {audio && (
                <div className="audio-player">
                    <strong>AI Voice Coach</strong>
                    <audio controls src={audio} style={{ width: "100%", marginTop: 8 }} />
                </div>
            )}
        </>
    );
}

