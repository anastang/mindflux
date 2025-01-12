import React, { useState, useEffect, useCallback } from 'react';
import { BrowserRouter, Routes, Route, useNavigate } from 'react-router-dom';
import { ArrowUp, ArrowRight, ArrowDown, ArrowLeft, Play, BarChart2 } from 'lucide-react';
import { Dashboard } from './Dashboard';
import type { GameResult } from './types';

function Game() {
  const navigate = useNavigate();
  const [sequence, setSequence] = useState<Direction[]>([]);
  const [playerSequence, setPlayerSequence] = useState<Direction[]>([]);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isShowingSequence, setIsShowingSequence] = useState(false);
  const [gameOver, setGameOver] = useState(false);
  const [activeButton, setActiveButton] = useState<Direction | null>(null);
  const [level, setLevel] = useState<number>(1);
  const [score, setScore] = useState<number>(0);
  const [gestureCounts, setGestureCounts] = useState({ up: 0, right: 0, down: 0, left: 0 });

  // Simulated emotion data
  const [emotions, setEmotions] = useState({
    happy: 0,
    sad: 0,
    angry: 0,
    neutral: 0,
    surprise: 0,
    fear: 0,
    disgust: 0,
  });

  type Direction = 'UP' | 'RIGHT' | 'DOWN' | 'LEFT';

  const buttons: { direction: Direction; color: string; icon: React.ReactNode }[] = [
    { direction: 'UP', color: 'bg-green-500', icon: <ArrowUp className="w-8 h-8" /> },
    { direction: 'RIGHT', color: 'bg-red-500', icon: <ArrowRight className="w-8 h-8" /> },
    { direction: 'DOWN', color: 'bg-yellow-500', icon: <ArrowDown className="w-8 h-8" /> },
    { direction: 'LEFT', color: 'bg-blue-500', icon: <ArrowLeft className="w-8 h-8" /> },
  ];

  const handleKeyDown = useCallback((event: KeyboardEvent) => {
    if (isShowingSequence || gameOver || !isPlaying) return;

    let selectedDirection: Direction | null = null;

    switch (event.key) {
      case 'ArrowUp':
        selectedDirection = 'UP';
        break;
      case 'ArrowRight':
        selectedDirection = 'RIGHT';
        break;
      case 'ArrowDown':
        selectedDirection = 'DOWN';
        break;
      case 'ArrowLeft':
        selectedDirection = 'LEFT';
        break;
      default:
        break;
    }

    if (selectedDirection) {
      setPlayerSequence((prev) => [...prev, selectedDirection!]);
      setActiveButton(selectedDirection);

      const lowerCaseDirection = selectedDirection.toLowerCase() as keyof typeof gestureCounts;
      setGestureCounts((prev) => ({
        ...prev,
        [lowerCaseDirection]: prev[lowerCaseDirection] + 1,
      }));

      setTimeout(() => setActiveButton(null), 300);
    }
  }, [isShowingSequence, gameOver, isPlaying]);

  useEffect(() => {
    window.addEventListener('keydown', handleKeyDown);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [handleKeyDown]);

  const saveGameResult = () => {
    const result: GameResult = {
      level,
      score,
      timestamp: new Date().toISOString(),
      gestureCounts,
      emotions: {
        ...emotions,
        happy: Math.floor(Math.random() * Math.max(score, 5)),
        neutral: Math.floor(Math.random() * 10),
        sad: Math.floor(Math.random() * 5),
        angry: Math.floor(Math.random() * 3),
        surprise: Math.floor(Math.random() * 4),
        fear: Math.floor(Math.random() * 2),
        disgust: Math.floor(Math.random() * 3),
      },
    };

    const savedResults = JSON.parse(localStorage.getItem('gameResults') || '[]');
    localStorage.setItem('gameResults', JSON.stringify([...savedResults, result]));
  };

  const startGame = () => {
    setIsPlaying(true);
    setGameOver(false);
    setPlayerSequence([]);
    setGestureCounts({ up: 0, right: 0, down: 0, left: 0 });
    setLevel(1);
    setScore(0);
    const initialSequence = [getRandomDirection()];
    setSequence(initialSequence);
    playSequence(initialSequence);
  };

  const getRandomDirection = (): Direction => {
    const directions: Direction[] = ['UP', 'RIGHT', 'DOWN', 'LEFT'];
    return directions[Math.floor(Math.random() * directions.length)];
  };

  const playSequence = (sequenceToPlay: Direction[]) => {
    setIsShowingSequence(true);
    let i = 0;
    const interval = setInterval(() => {
      setActiveButton(sequenceToPlay[i]);
      setTimeout(() => setActiveButton(null), 500);
      i++;
      if (i >= sequenceToPlay.length) {
        clearInterval(interval);
        setIsShowingSequence(false);
      }
    }, 1000);
  };

  useEffect(() => {
    if (playerSequence.length === sequence.length && sequence.length > 0) {
      if (JSON.stringify(playerSequence) === JSON.stringify(sequence)) {
        setScore((prev) => prev + 1);
        setLevel((prev) => prev + 1);
        const newSequence = [...sequence, getRandomDirection()];
        setSequence(newSequence);
        setPlayerSequence([]);
        playSequence(newSequence);
      } else {
        setGameOver(true);
        setIsPlaying(false);
        saveGameResult();
      }
    }
  }, [playerSequence, sequence]);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-900 text-white">
      <div className="absolute top-4 right-4">
        <button
          onClick={() => navigate('/dashboard')}
          className="flex items-center gap-2 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        >
          <BarChart2 className="w-5 h-5" />
          View Dashboard
        </button>
      </div>
      <h1 className="text-4xl font-bold mb-8">Simon Says</h1>
      <div className="text-lg mb-4">Level: {level} | Score: {score}</div>
      <div className="relative w-64 h-64">
        {buttons.map(({ direction, color, icon }) => (
          <div
            key={direction}
            className={`absolute ${
              direction === 'UP'
                ? 'top-0 left-1/2 transform -translate-x-1/2'
                : direction === 'RIGHT'
                ? 'top-1/2 right-0 transform -translate-y-1/2'
                : direction === 'DOWN'
                ? 'bottom-0 left-1/2 transform -translate-x-1/2'
                : 'top-1/2 left-0 transform -translate-y-1/2'
            } w-24 h-24 flex items-center justify-center rounded-full cursor-pointer transition-all duration-200 ${
              activeButton === direction ? color : 'bg-gray-700'
            }`}
            onClick={() => handleKeyDown(new KeyboardEvent(direction))}
          >
            {icon}
          </div>
        ))}
      </div>
      {gameOver && (
        <p className="text-red-500 mt-4">
          Game Over! Final Score: {score}. Press Play to try again.
        </p>
      )}
      <button
        onClick={startGame}
        className="mt-8 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
      >
        <Play className="inline-block mr-2" /> Play
      </button>
    </div>
  );
}

function App() {
  const [results, setResults] = useState<GameResult[]>(() =>
    JSON.parse(localStorage.getItem('gameResults') || '[]')
  );

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Game />} />
        <Route path="/dashboard" element={<Dashboard results={results} />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
