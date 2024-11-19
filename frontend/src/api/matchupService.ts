import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
});

export const predictMatchup = async (teamA: string, teamB: string) => {
  try {
    const response = await api.post("/api/predict", {
      team_A: teamA,
      team_B: teamB,
    });
    return response.data.prediction;
  } catch (error) {
    console.error("Error predicting matchup:", error);
    return null;
  }
};

export const predictFantasyMatchup = async (
  teamAPlayers: string[],
  teamBPlayers: string[]
) => {
  console.log("Sending to backend:", {
    team_A_players: teamAPlayers,
    team_B_players: teamBPlayers,
  });
  try {
    const response = await api.post("/api/predict-fantasy", {
      team_A_players: teamAPlayers,
      team_B_players: teamBPlayers,
    });
    console.log("Backend response:", response.data);
    return response.data; // Return the full response, not just prediction
  } catch (error) {
    console.error("Error predicting fantasy matchup:", error);
    return null;
  }
};
