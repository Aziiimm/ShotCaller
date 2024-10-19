import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:5000", // Flask backend URL
});

export const predictMatchup = async (teamA: string, teamB: string) => {
  try {
    const response = await api.post("/predict", {
      team_A: teamA,
      team_B: teamB,
    });
    return response.data.prediction;
  } catch (error) {
    console.error("Error predicting matchup:", error);
    return null;
  }
};
