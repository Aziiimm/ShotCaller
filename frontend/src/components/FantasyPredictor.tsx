import React, { useState } from "react";
import { predictMatchup } from "../api/matchupService";
import { ToastProvider, Toast } from "@/components/ui/toast";
import { useToast } from "@/hooks/use-toast";
import SelectPlayer from "./selectplayers";

const FantasyPredictor: React.FC = () => {
  const [teamAPlayerCount, setTeamAPlayerCount] = useState(0);
  const [teamBPlayerCount, setTeamBPlayerCount] = useState(0);
  const [prediction, setPrediction] = useState("");

  const { toast } = useToast();

  const handlePredict = async () => {
    if (teamAPlayerCount < 10 || teamBPlayerCount < 10) {
      toast({
        title: "Selection Error",
        description: "Each team must have at least 10 players.",
        duration: 2000,
      });
      return;
    }

    try {
      const result = await predictMatchup("Team A", "Team B");
      setPrediction(result || "Error predicting the outcome");
    } catch (error) {
      toast({
        title: "Prediction Error",
        description: "An error occurred. Please try again later.",
        duration: 2000,
      });
    }
  };

  const handlePlayerCountChange = (team: string, count: number) => {
    if (team === "A") setTeamAPlayerCount(count);
    if (team === "B") setTeamBPlayerCount(count);
  };

  const handleLimitReached = (team: string) => {
    toast({
      title: "Selection Limit Reached",
      description: `Team ${team} cannot have more than 13 players.`,
      duration: 2000,
    });
  };

  return (
    <ToastProvider>
      <div className="bg-transparent border-2 dark:border-gray-900 rounded-3xl p-6 max-w-7xl h-86 mx-auto">
        <h2 className="text-xl font-semibold mb-4 justify-self-center">
          Predict Fantasy Match Outcome
        </h2>
        <SelectPlayer
          onPlayerCountChange={handlePlayerCountChange}
          onLimitReached={handleLimitReached}
        />

        <button
          onClick={handlePredict}
          className="bg-blue-700 transition ease-in-out duration-300 text-white px-4 py-2 rounded-md hover:bg-blue-900 dark:bg-red-500 dark:hover:bg-red-800"
        >
          Predict
        </button>
        {prediction && (
          <h3 className="mt-4 text-xl font-bold underline">{`Prediction: ${prediction}`}</h3>
        )}
      </div>
      <Toast />
    </ToastProvider>
  );
};

export default FantasyPredictor;
