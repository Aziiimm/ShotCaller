import React, { useState } from "react";
import { ComboboxDemo } from "./ui/playersComboBox";

interface SelectPlayerProps {
  onPlayerCountChange: (team: string, count: number) => void;
  onLimitReached: (team: string) => void;
}

const SelectPlayer: React.FC<SelectPlayerProps> = ({
  onPlayerCountChange,
  onLimitReached,
}) => {
  const [teamAPlayers, setTeamAPlayers] = useState<string[]>([]);
  const [teamBPlayers, setTeamBPlayers] = useState<string[]>([]);

  const handleTeamASelect = (player: string) => {
    setTeamAPlayers((prevPlayers) => {
      if (prevPlayers.includes(player)) {
        const updatedPlayers = prevPlayers.filter((p) => p !== player);
        onPlayerCountChange("A", updatedPlayers.length);
        return updatedPlayers;
      } else if (prevPlayers.length < 13) {
        const updatedPlayers = [...prevPlayers, player];
        onPlayerCountChange("A", updatedPlayers.length);
        return updatedPlayers;
      } else {
        onLimitReached("A");
        return prevPlayers;
      }
    });
  };

  const handleTeamBSelect = (player: string) => {
    setTeamBPlayers((prevPlayers) => {
      if (prevPlayers.includes(player)) {
        const updatedPlayers = prevPlayers.filter((p) => p !== player);
        onPlayerCountChange("B", updatedPlayers.length);
        return updatedPlayers;
      } else if (prevPlayers.length < 13) {
        const updatedPlayers = [...prevPlayers, player];
        onPlayerCountChange("B", updatedPlayers.length);
        return updatedPlayers;
      } else {
        onLimitReached("B");
        return prevPlayers;
      }
    });
  };

  const handleRemoveTeamAPlayer = (player: string) => {
    setTeamAPlayers((prevPlayers) => {
      const updatedPlayers = prevPlayers.filter((p) => p !== player);
      onPlayerCountChange("A", updatedPlayers.length);
      return updatedPlayers;
    });
  };

  const handleRemoveTeamBPlayer = (player: string) => {
    setTeamBPlayers((prevPlayers) => {
      const updatedPlayers = prevPlayers.filter((p) => p !== player);
      onPlayerCountChange("B", updatedPlayers.length);
      return updatedPlayers;
    });
  };
  return (
    <div>
      <div className="mb-16">
        <p className="text-m font-medium text-black flex flex-col dark:text-white">
          <label className="mb-1">Selected Players for Team A:</label>
          <span>
            {teamAPlayers.map((player) => (
              <span
                key={player}
                className="cursor-pointer hover:text-red-500"
                onClick={() => handleRemoveTeamAPlayer(player)}
              >
                {player}
                {", "}
              </span>
            ))}
          </span>
        </p>
        <label className="block text-m font-medium underline my-2 text-black dark:text-white">
          Team A (Select up to 13 players):
        </label>
        <ComboboxDemo
          selectedPlayers={teamAPlayers}
          onSelectPlayer={handleTeamASelect}
        />
      </div>

      <div className="mb-16">
        <p className="text-m font-medium text-black flex flex-col dark:text-white">
          <label className="mb-1">Selected Players for Team B:</label>
          <span>
            {teamBPlayers.map((player) => (
              <span
                key={player}
                className="cursor-pointer hover:text-red-500"
                onClick={() => handleRemoveTeamBPlayer(player)}
              >
                {player}
                {", "}
              </span>
            ))}
          </span>
        </p>
        <label className="block text-m font-medium underline my-2 text-black dark:text-white">
          Team B (Select up to 13 players):
        </label>
        <ComboboxDemo
          selectedPlayers={teamBPlayers}
          onSelectPlayer={handleTeamBSelect}
        />
      </div>
    </div>
  );
};

export default SelectPlayer;
