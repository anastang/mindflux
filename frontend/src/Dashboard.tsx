import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar, Line, Pie } from 'react-chartjs-2';
import { ArrowLeftCircle } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import type { GameResult } from './types';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

type Props = {
  results: GameResult[];
};

export function Dashboard({ results }: Props) {
  const navigate = useNavigate();

  if (results.length === 0) {
    return (
      <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center justify-center">
        <p className="text-lg">No game results to display. Play a game to see analytics.</p>
        <button
          onClick={() => navigate('/')}
          className="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        >
          Back to Game
        </button>
      </div>
    );
  }

  // Prepare data for charts
  const progressData = {
    labels: results.map((_, index) => `Game ${index + 1}`),
    datasets: [
      {
        label: 'Score Progress',
        data: results.map((result) => result.score),
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1,
      },
      {
        label: 'Level Progress',
        data: results.map((result) => result.level),
        borderColor: 'rgb(255, 99, 132)',
        tension: 0.1,
      },
    ],
  };

  const totalGestures = results.reduce(
    (acc, result) => ({
      up: acc.up + result.gestureCounts.up,
      right: acc.right + result.gestureCounts.right,
      down: acc.down + result.gestureCounts.down,
      left: acc.left + result.gestureCounts.left,
    }),
    { up: 0, right: 0, down: 0, left: 0 }
  );

  const gestureData = {
    labels: ['Up', 'Right', 'Down', 'Left'],
    datasets: [
      {
        data: [totalGestures.up, totalGestures.right, totalGestures.down, totalGestures.left],
        backgroundColor: [
          'rgba(75, 192, 192, 0.6)',
          'rgba(255, 99, 132, 0.6)',
          'rgba(255, 206, 86, 0.6)',
          'rgba(153, 102, 255, 0.6)',
        ],
      },
    ],
  };

  const totalEmotions = results.reduce(
    (acc, result) => ({
      happy: acc.happy + result.emotions.happy,
      sad: acc.sad + result.emotions.sad,
      angry: acc.angry + result.emotions.angry,
      neutral: acc.neutral + result.emotions.neutral,
      surprise: acc.surprise + result.emotions.surprise,
      fear: acc.fear + result.emotions.fear,
      disgust: acc.disgust + result.emotions.disgust,
    }),
    { happy: 0, sad: 0, angry: 0, neutral: 0, surprise: 0, fear: 0, disgust: 0 }
  );

  const emotionData = {
    labels: Object.keys(totalEmotions),
    datasets: [
      {
        label: 'Emotion Distribution',
        data: Object.values(totalEmotions),
        backgroundColor: 'rgba(54, 162, 235, 0.6)',
      },
    ],
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-4xl font-bold">Game Analytics Dashboard</h1>
          <button
            onClick={() => navigate('/')}
            className="flex items-center gap-2 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          >
            <ArrowLeftCircle className="w-5 h-5" />
            Back to Game
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="bg-gray-800 p-6 rounded-lg">
            <h2 className="text-xl font-semibold mb-4">Progress Over Time</h2>
            <Line data={progressData} options={{ responsive: true }} />
          </div>

          <div className="bg-gray-800 p-6 rounded-lg">
            <h2 className="text-xl font-semibold mb-4">Gesture Distribution</h2>
            <Pie data={gestureData} options={{ responsive: true }} />
          </div>

          <div className="bg-gray-800 p-6 rounded-lg md:col-span-2">
            <h2 className="text-xl font-semibold mb-4">Emotion Distribution</h2>
            <Bar data={emotionData} options={{ responsive: true }} />
          </div>
        </div>
      </div>
    </div>
  );
}
