import React, { useState } from "react";
import { predictMatchup } from "../api/matchupService"; // Import the existing API service

const MatchPredictor: React.FC = () => {
  const [teamA, setTeamA] = useState("");
  const [teamB, setTeamB] = useState("");
  const [prediction, setPrediction] = useState("");

  const handlePredict = async () => {
    if (teamA && teamB) {
      const result = await predictMatchup(teamA, teamB);
      setPrediction(result || "Error predicting the outcome");
    } else {
      alert("Please select both teams");
    }
  };

  return (
    <div className="bg-white shadow-md rounded-md p-6 max-w-lg mx-auto">
      <h2 className="text-xl font-semibold mb-4">Predict NBA Match Outcome</h2>
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700">
          Team A:
        </label>
        <input
          type="text"
          value={teamA}
          onChange={(e) => setTeamA(e.target.value)}
          className="mt-1 p-2 border border-gray-300 rounded-md w-full"
        />
      </div>
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700">
          Team B:
        </label>
        <input
          type="text"
          value={teamB}
          onChange={(e) => setTeamB(e.target.value)}
          className="mt-1 p-2 border border-gray-300 rounded-md w-full"
        />
      </div>
      <button
        onClick={handlePredict}
        className="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600"
      >
        Predict
      </button>
      {prediction && (
        <h3 className="mt-4 text-lg">{`Prediction: ${prediction}`}</h3>
      )}
    </div>
  );
};

export default MatchPredictor;
