# **MindFlux**

A modern twist on the classic Simon Says game. Watch the sequence of arrows, then repeat them using hand gestures. Built with **React**, **TypeScript**, **Chart.js** for analytics, and integrated with a **Python-based Mediapipe script** for gesture recognition and basic emotion tracking.

---

## Table of Contents

1. [Overview](#overview)  
2. [Features](#features)  
3. [Use Cases & Benefits](#use-cases--benefits)  
4. [Challenges](#challenges)  
5. [How It Works](#how-it-works)  
6. [Setup & Installation](#setup--installation)  
7. [Usage](#usage)  
8. [Dashboard & Analytics](#dashboard--analytics)  
9. [Python Requirements](#python-requirements)  
10. [Author Credits](#author-credits)  
11. [License](#license)

---

## Overview

This Simon Says game challenges players to mimic an increasingly longer sequence of directional arrows. When the player’s input matches the displayed sequence, the sequence lengthens; once the input differs, the game ends. Throughout the game, data such as scores, levels, and arrow presses are stored locally for analytics. A **Dashboard** provides a visual overview of the player’s progress over multiple sessions and can also display simulated or real emotion data (captured from a Python script running Mediapipe and DeepFace, if desired).

---

## Features

- **Increasing Sequence Difficulty**  
  Each successful round adds a new random direction to the sequence, upping the challenge.

- **Gesture Detection**  
  Integrate with a Python script that uses [Mediapipe Hands](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker) for capturing hand signals.

- **Emotion Tracking**  
  Integrate with a Python script that uses [DeepFace](https://github.com/serengil/deepface) or other emotion detection libraries.

- **Local Storage**  
  Player results (score, gestures, emotions) are automatically saved in the browser.

- **Analytics Dashboard**  
  View performance over time, distribution of gestures, and aggregated emotion data in user-friendly charts.

---

## Use Cases & Benefits

1. **Assisting People with Disabilities**  
   - By detecting hand gestures (via Mediapipe) or arrow key presses, individuals with limited mobility in one or more limbs can still participate.  
   - The game can be adapted to a range of physical capabilities by supporting multiple input methods (keyboard, clicks, or gestures).

2. **Improving Motor Skills**  
   - The repetitive nature of Simon Says (rapid pressing or gesturing in response to prompts) can enhance hand–eye coordination and fine motor skills.  
   - Hand gesture detection encourages active movement, which can be beneficial in rehabilitative or therapeutic settings.

3. **Recognizing ADHD or Other Attention/Executive Function Challenges**  
   - Simon Says inherently requires focus and recall (short-term memory), which may help identify difficulties in attention span.  
   - The game’s progressive difficulty highlights possible challenges in sustaining mental focus and working memory—useful for early screening or supplemental training.

4. **Cognitive Rehabilitation**  
   - The gradual increase in sequence length encourages sustained attention and working memory practice.  
   - This can be especially helpful for individuals recovering from brain injuries or those with mild cognitive impairments, as it trains sequencing, recall, and attentional control.

---

## Challenges

1. **Accurate Gesture Recognition**  
   - Reliance on real-time hand tracking and landmark detection can lead to false positives or missed gestures if lighting or background conditions are suboptimal.  
   - Ensuring robust detection across different skin tones, hand poses, and user behaviors is crucial for an inclusive experience.

2. **Maintaining Smooth Performance in Real-Time**  
   - Running Mediapipe, DeepFace, or other ML frameworks in parallel with the React app can be resource-intensive.  
   - Optimizations (e.g., limiting the detection frequency, handling frames efficiently) may be required to avoid lagging UI and input delays.

---

## How It Works

### 1. Frontend (React)

- **Gameplay**  
  A random sequence of directions (UP, RIGHT, DOWN, LEFT) is generated and shown to the user.  
  The user repeats the sequence using arrow keys or by clicking on-screen arrows.  
  Success leads to a longer sequence; an incorrect response ends the game.

- **Local Storage**  
  After each game, the score, level, and gesture usage are stored in local storage as a game result.  
  Simulated or real **emotion data** can also be stored.

### 2. Python Script 

- A separate Python script (using Mediapipe and DeepFace) runs in the background:  
  1. **Gesture Detection**: Mediapipe tracks the user’s hand landmarks, interpreting gestures (up, down, left, right), which can be sent to the React app.  
  2. **Emotion Detection**: A face detection model (e.g., DeepFace) extracts the user’s dominant emotion (happy, sad, angry, etc.).

- The data from the Python script is sent to the React frontend (e.g., via an API endpoint like `localhost:5000/submit-data`).  
- The React app merges these gestures with standard keyboard inputs, updating the user’s progress.  
- The Python script can also log/store emotion data locally, or pass it to the React app for display on the **Dashboard**.

---

## Setup & Installation

### Prerequisites

- **Node.js** (v14+ recommended)  
- **npm** or **yarn**  
- **Python 3.7+** if integrating gesture and emotion detection

### Steps

1. **Clone this repository**:
   git clone https://github.com/anastang//mindflux-v2
   We will have two terminals
   
2. **Backend**
   1. cd backend
   2. pip install -r requirements.txt
   3. python script.py
  
3. **Frontend**
   1. cd frontend
   2. npm install
   3. npm run dev
   4. click on link if webpage does not open

Dashboard & Analytics
Score & Level Progress (Line Chart)
Tracks how your score and level evolve across multiple game sessions.

Gesture Distribution (Pie Chart)
Shows how often each direction (UP, RIGHT, DOWN, LEFT) was used across all games.

Emotion Distribution (Bar Chart)
Aggregates the counts of detected emotions (happy, sad, neutral, etc.) across all games.

Author Credits
By:

Anastan Gnanapragasam
Adriel De Vera
Romeo Junior Barbieto
