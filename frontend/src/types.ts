export type GameResult = {
    level: number;
    score: number;
    timestamp: string;
    gestureCounts: {
      up: number;
      right: number;
      down: number;
      left: number;
    };
    emotions: {
      happy: number;
      sad: number;
      angry: number;
      neutral: number;
      surprise: number;
      fear: number;
      disgust: number;
    };
  };
  