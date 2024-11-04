import React, { useState, useEffect } from "react";
import MatchPredictor from "./components/MatchPredictor";
import FantasyPredictor from "./components/FantasyPredictor";
import Navbar from "./components/navbar";
import { Toaster } from "./components/ui/toaster";

const App: React.FC = () => {
  const [activePredictor, setActivePredictor] = useState<"nba" | "fantasy">(
    "nba"
  );
  const [isDarkMode, setIsDarkMode] = useState<boolean>(true);

  const handleSwitch = (predictor: "nba" | "fantasy") => {
    setActivePredictor(predictor);
  };

  const toggleTheme = () => {
    setIsDarkMode((prev) => !prev);
  };

  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  }, [isDarkMode]);

  return (
    <div className="h-screen w-screen bg-slate-100 dark:bg-gray-950">
      <Navbar
        onSwitch={handleSwitch}
        activePredictor={activePredictor}
        toggleTheme={toggleTheme}
        isDarkMode={isDarkMode}
      />

      <div className="flex justify-center mt-32 space-x-4 mb-6"></div>
      {activePredictor === "nba" && <MatchPredictor />}
      {activePredictor === "fantasy" && <FantasyPredictor />}
      <Toaster />
    </div>
  );
};

export default App;
