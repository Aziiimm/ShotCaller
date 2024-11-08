import React, { useState } from "react";
import logo from "../assets/logo.png";

interface NavbarProps {
  onSwitch: (predictor: "nba" | "fantasy") => void;
  activePredictor: "nba" | "fantasy";
  toggleTheme: () => void;
  isDarkMode: boolean;
}

const Navbar: React.FC<NavbarProps> = ({
  onSwitch,
  activePredictor,
  toggleTheme,
  isDarkMode,
}) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const handleMenuToggle = () => {
    setIsMenuOpen((prev) => !prev);
  };

  return (
    <nav className="bg-white pt-4 bg-slate-200 dark:bg-gray-900">
      <div className="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
        <a href="/" className="flex items-center space-x-3">
          <img src={logo} className="h-8 " alt="ShotCaller Logo" />
          <span className="self-center text-2xl underline font-semibold whitespace-nowrap transition ease-in-out hover:-translate-y-2 duration-300 dark:text-white">
            ShotCaller
          </span>
        </a>
        <button
          type="button"
          className="inline-flex items-center p-2 w-10 h-10 justify-center text-sm text-gray-500 rounded-lg md:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600"
          aria-controls="navbar-default"
          aria-expanded={isMenuOpen}
          onClick={handleMenuToggle}
        >
          <span className="sr-only">Open main menu</span>
          <svg
            className="w-5 h-5"
            aria-hidden="true"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 17 14"
          >
            <path
              stroke="currentColor"
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M1 1h15M1 7h15M1 13h15"
            />
          </svg>
        </button>
        <div
          className={`${
            isMenuOpen ? "block" : "hidden"
          } w-full md:block md:w-auto`}
          id="navbar-default"
        >
          <ul className="font-medium flex flex-col mt-4 gap-x-8 gap-y-4 md:flex-row md:mt-0">
            <li>
              <button
                onClick={() => onSwitch("nba")}
                className={`block p-2 rounded transition ease-in-out duration-300 rounded-lg ${
                  activePredictor === "nba"
                    ? "text-white md:-translate-y-2 bg-blue-700 dark:bg-red-500"
                    : "text-black md:hover:-translate-y-2 hover:bg-slate-200 dark:text-white dark:hover:bg-slate-600"
                }`}
              >
                NBA Match Predictor
              </button>
            </li>
            <li>
              <button
                onClick={() => onSwitch("fantasy")}
                className={`block p-2 rounded transition ease-in-out duration-300 rounded-lg ${
                  activePredictor === "fantasy"
                    ? "text-white md:-translate-y-2 bg-blue-700 dark:bg-red-500"
                    : "text-black md:hover:-translate-y-2 hover:bg-slate-200 dark:text-white dark:hover:bg-slate-600"
                }`}
              >
                Fantasy League Predictor
              </button>
            </li>
            <li>
              <button
                onClick={toggleTheme}
                className="text-black transition ease-in-out md:hover:-translate-y-2 p-2 duration-300 hover:bg-slate-300 rounded-lg dark:text-white dark:hover:bg-slate-600"
              >
                {isDarkMode ? "Mode 🌙" : "Mode 🌞"}
              </button>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
