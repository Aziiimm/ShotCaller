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
