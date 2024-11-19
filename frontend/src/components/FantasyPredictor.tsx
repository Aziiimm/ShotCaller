import React, { useState } from "react";
import { predictFantasyMatchup } from "../api/matchupService";
import { ToastProvider, Toast } from "@/components/ui/toast";
import { useToast } from "@/hooks/use-toast";
import SelectPlayer from "./selectplayers";

const FantasyPredictor: React.FC = () => {
  const [teamAPlayers, setTeamAPlayers] = useState<string[]>([]);
  const [teamBPlayers, setTeamBPlayers] = useState<string[]>([]);
  const [teamAPlayerCount, setTeamAPlayerCount] = useState(0);
  const [teamBPlayerCount, setTeamBPlayerCount] = useState(0);
  const [prediction, setPrediction] = useState("");

  const [teamAScore, setTeamAScore] = useState<number | null>(null);
  const [teamBScore, setTeamBScore] = useState<number | null>(null);
  const [statDifferentials, setStatDifferentials] = useState<{
    PTS_diff?: number;
    AST_diff?: number;
    TRB_diff?: number;
    STL_diff?: number;
    BLK_diff?: number;
  }>({});

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
      const result = await predictFantasyMatchup(teamAPlayers, teamBPlayers);

      if (result) {
        setPrediction(result.prediction || "Error predicting the outcome");
        setTeamAScore(result.team_A_score || null);
        setTeamBScore(result.team_B_score || null);
        setStatDifferentials(result.stat_differentials || {});
      } else {
        setPrediction("Error predicting the outcome");
      }
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

  const handlePlayerSelection = (team: string, players: string[]) => {
    if (team === "A") setTeamAPlayers(players);
    if (team === "B") setTeamBPlayers(players);
  };

  return (
    <ToastProvider>
      <div className="bg-transparent border-2 dark:border-gray-900 rounded-3xl p-6 max-h-max max-w-7xl mx-auto">
        <h2 className="text-xl font-semibold mb-4 justify-self-center">
          Predict Fantasy Match Outcome
        </h2>
        <SelectPlayer
          onPlayerCountChange={handlePlayerCountChange}
          onLimitReached={handleLimitReached}
          onPlayerSelection={handlePlayerSelection}
        />

        <button
          onClick={handlePredict}
          className="bg-blue-700 transition ease-in-out duration-300 text-white px-4 py-2 rounded-md hover:bg-blue-900 dark:bg-red-500 dark:hover:bg-red-800"
        >
          Predict
        </button>
        {prediction && (
          <>
            <h3 className="mt-4 text-xl font-bold underline">{`Prediction: ${prediction}`}</h3>
            {teamAScore !== null && teamBScore !== null && (
              <p className="mt-2 text-m">{`Team A Score: ${teamAScore}, Team B Score: ${teamBScore}`}</p>
            )}
            {statDifferentials && (
              <div className="mt-4">
                <h4 className="font-semibold underline">Stat Differentials:</h4>
                <ul className="list-disc pl-4 grid grid-cols-3 text-sm text-gray-800 dark:text-gray-200 break-words">
                  {Object.entries(statDifferentials).map(([key, value]) => (
                    <li key={key} className="whitespace-normal">
                      {key.replace("_diff", "")}: {value.toPrecision(3)}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </>
        )}
      </div>
      <Toast />
    </ToastProvider>
  );
};

export default FantasyPredictor;
