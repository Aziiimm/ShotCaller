import React, { useState } from "react";
import MatchPredictor from "./components/MatchPredictor";
import FantasyPredictor from "./components/FantasyPredictor";

const App: React.FC = () => {
  const [activePredictor, setActivePredictor] = useState<"nba" | "fantasy">(
    "nba"
  );

  const handleSwitch = (predictor: "nba" | "fantasy") => {
    setActivePredictor(predictor);
  };

  return (
    <div className="min-h-screen bg-gray-500 p-4">
      <h1 className="text-3xl font-bold text-center mb-6">
        NBA & Fantasy Predictor
      </h1>

      <div className="flex justify-center space-x-4 mb-6">
        <button
          className={`px-4 py-2 rounded-md ${
            activePredictor === "nba" ? "bg-blue-500 text-white" : "bg-gray-300"
          }`}
          onClick={() => handleSwitch("nba")}
        >
          NBA Match Predictor
        </button>
        <button
          className={`px-4 py-2 rounded-md ${
            activePredictor === "fantasy"
              ? "bg-blue-500 text-white"
              : "bg-gray-300"
          }`}
          onClick={() => handleSwitch("fantasy")}
        >
          Fantasy League Predictor
        </button>
      </div>

      {activePredictor === "nba" && <MatchPredictor />}
      {activePredictor === "fantasy" && <FantasyPredictor />}
    </div>
  );
};

export default App;
