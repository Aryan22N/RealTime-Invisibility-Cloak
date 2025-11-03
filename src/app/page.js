"use client";

import { useState } from "react";
import axios from "axios";

export default function HomePage() {
  const [color, setColor] = useState("blue");
  const [status, setStatus] = useState("Idle");
  const [loading, setLoading] = useState(false);
  const [showStream, setShowStream] = useState(false);

  const API_BASE = "http://127.0.0.1:5001";

  const startCloak = async () => {
    try {
      setLoading(true);
      setStatus("Starting...");
      await axios.post(`${API_BASE}/start`, { color });
      setStatus("Running");
      setShowStream(true);
    } catch (error) {
      console.error("Error:", error);
      setStatus("Error Starting Cloak");
      setShowStream(false);
    } finally {
      setLoading(false);
    }
  };

  const stopCloak = async () => {
    try {
      setLoading(true);
      setStatus("Stopping...");
      await axios.post(`${API_BASE}/stop`);
      setStatus("Stopped");
      setShowStream(false);
    } catch (error) {
      console.error("Error:", error);
      setStatus("Error Stopping Cloak");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-950 text-white font-sans p-6">
      <div className="w-full max-w-5xl bg-gray-900 p-8 rounded-2xl shadow-lg text-center space-y-6">
        <h1 className="text-3xl font-bold text-blue-400">
          🧥 Invisibility Cloak Controller
        </h1>

        {/* Color Selector */}
        <div>
          <h2 className="text-lg font-semibold mb-2">Select Cloak Color</h2>
          <select
            value={color}
            onChange={(e) => setColor(e.target.value)}
            className="bg-gray-800 border border-gray-600 rounded-lg p-2 w-1/2"
          >
            <option value="blue">Blue</option>
            <option value="red">Red</option>
            <option value="green">Green</option>
            <option value="black">Black</option>
          </select>
        </div>

        {/* Buttons */}
        <div className="flex justify-center gap-4 mt-4">
          <button
            onClick={startCloak}
            disabled={loading || status === "Running"}
            className="bg-green-600 hover:bg-green-700 px-5 py-2 rounded-lg transition disabled:opacity-50"
          >
            {loading && status === "Starting..." ? "Starting..." : "Start"}
          </button>
          <button
            onClick={stopCloak}
            disabled={loading || status === "Stopped" || status === "Idle"}
            className="bg-red-600 hover:bg-red-700 px-5 py-2 rounded-lg transition disabled:opacity-50"
          >
            {loading && status === "Stopping..." ? "Stopping..." : "Stop"}
          </button>
        </div>

        {/* Dual Video Feeds */}
        {showStream && (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-6">
            <div>
              <h3 className="text-lg font-semibold mb-2">🎥 Original Feed</h3>
              <img
                src={`${API_BASE}/video_feed_original?${Date.now()}`}
                alt="Original Feed"
                className="w-full rounded-xl border border-gray-700"
              />
            </div>
            <div>
              <h3 className="text-lg font-semibold mb-2">🧥 Cloak Output</h3>
              <img
                src={`${API_BASE}/video_feed_output?${Date.now()}`}
                alt="Cloak Output"
                className="w-full rounded-xl border border-gray-700"
              />
            </div>
          </div>
        )}

        {/* Status */}
        <div className="text-lg mt-4">
          <span className="font-semibold">Status:</span>{" "}
          <span
            className={
              status === "Running"
                ? "text-green-400"
                : status === "Stopped"
                ? "text-red-400"
                : status.includes("Error")
                ? "text-yellow-400"
                : "text-gray-400"
            }
          >
            {status}
          </span>
        </div>

        <footer className="text-gray-500 text-sm mt-6">
          Developed using Next.js + Flask + OpenCV
        </footer>
      </div>
    </div>
  );
}
