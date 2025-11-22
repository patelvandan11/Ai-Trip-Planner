import React, { useEffect, useState } from 'react';

function Profile() {
  const [profile, setProfile] = useState(null);
  const [trips, setTrips] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchData() {
      try {
        const profileRes = await fetch('/api/user/profile');
        if (!profileRes.ok) throw new Error('Failed to fetch profile');
        const profileData = await profileRes.json();
        setProfile(profileData);

        const tripsRes = await fetch('/api/user/trips');
        if (!tripsRes.ok) throw new Error('Failed to fetch trips');
        const tripsData = await tripsRes.json();
        setTrips(tripsData);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!profile) return <div>No profile data.</div>;

  return (
    <div>
      <h2>Welcome, {profile.name}</h2>
      <p>Email: {profile.email}</p>
      <h3>Your Trip History</h3>
      <ul>
        {trips.length === 0 ? (
          <li>No trips found.</li>
        ) : (
          trips.map(trip => (
            <li key={trip.id}>
              {trip.destination} on {trip.date}
            </li>
          ))
        )}
      </ul>
    </div>
  );
}

export default Profile; 