import React from "react";
import { Routes, Route } from "react-router-dom";

// Main App
import App from "../App.jsx";

// Components (Fixing incorrect paths)
import CreateTrip from "../components/custom/Create_trip.jsx";
import Features from "../components/custom/Features.jsx";
import Form from "../components/custom/Form.jsx";
import Login from "../components/custom/Login.jsx";
import ResetPassword from "../components/custom/ResetPass.jsx";
import EmailVerify from "../components/custom/EmailVerify.jsx";
import OurStory from "../components/custom/OurStory.jsx";
import Profile from "../components/custom/Profile.jsx";

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<App />} />
      <Route path="/login" element={<Login />} />
      <Route path="/reset-password" element={<ResetPassword />} />
      <Route path="/email-verify" element={<EmailVerify />} />
      <Route path="/our-story" element={<OurStory />} />
      <Route path="/profile" element={<Profile />} />

      {/* Trip */}
      <Route path="/create-trip" element={<CreateTrip />} />
      <Route path="/feature" element={<Features />} />

      {/* Products */}
      <Route path="/form" element={<Form />} />
    </Routes>
  );
};

export default AppRoutes;
