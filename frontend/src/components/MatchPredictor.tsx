import React, { useState } from "react";
import { predictMatchup } from "../api/matchupService";
import { ComboboxDemo } from "./ui/teamsCombobox";
import { ToastProvider, Toast } from "@/components/ui/toast";
import { useToast } from "@/hooks/use-toast";

const MatchPredictor: React.FC = () => {
  const [teamA, setTeamA] = useState("");
  const [teamB, setTeamB] = useState("");
  const [prediction, setPrediction] = useState("");

  const { toast } = useToast();

  const handlePredict = async () => {
    if (teamA && teamB) {
      if (teamA === teamB) {
        toast({
          title: "Selection Error",
          description: "Please Select Two Different Teams",
          duration: 2000,
        });
      } else {
        try {
          const result = await predictMatchup(teamA, teamB);
          setPrediction(result || "Error predicting the outcome");
        } catch (error) {
          toast({
            title: "Prediction Error",
            description: "An Error Occured. Please Try Again Later.",
            duration: 2000,
          });
        }
      }
    } else {
      toast({
        title: "Selection Error",
        description: "Please Select Both Teams",
        duration: 2000,
      });
    }
  };

  return (
    <ToastProvider>
      <div className="bg-transparent border-2 dark:border-gray-900 rounded-3xl p-6 max-w-2xl h-86 mx-auto">
        <h2 className="text-xl font-semibold mb-4 justify-self-center">
          Predict NBA Match Outcome
        </h2>
        <div className="mb-4">
          <label className="block text-m underline font-medium text-black mb-2 dark:text-white">
            Team A:
          </label>
          <ComboboxDemo onSelect={setTeamA} />
        </div>
        <div className="mb-4">
          <label className="block text-m underline font-medium text-black mb-2 dark:text-white">
            Team B:
          </label>

          <ComboboxDemo onSelect={setTeamB} />
        </div>
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

export default MatchPredictor;
