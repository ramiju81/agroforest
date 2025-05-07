// src/components/Dashboard/Dashboard.js
import { useEffect, useState } from 'react';
import ProgressChart from '../ProgressChart';
import WorkoutCard from '../WorkoutCard';
import './Dashboard.css';

const Dashboard = ({ userId }) => {
  const [userData, setUserData] = useState(null);
  const [workouts, setWorkouts] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const [userRes, workoutsRes] = await Promise.all([
        fetch(`/api/users/${userId}`),
        fetch(`/api/workouts?userId=${userId}`)
      ]);
      setUserData(await userRes.json());
      setWorkouts(await workoutsRes.json());
    };
    fetchData();
  }, [userId]);

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>Bienvenido, {userData?.name || 'Usuario'}</h1>
        <div className="user-progress">
          <ProgressChart data={userData?.progress} />
        </div>
      </header>
      
      <section className="workout-section">
        <h2>Tus Rutinas</h2>
        <div className="workout-grid">
          {workouts.map(workout => (
            <WorkoutCard key={workout.id} workout={workout} />
          ))}
        </div>
      </section>
    </div>
  );
};

export default Dashboard;