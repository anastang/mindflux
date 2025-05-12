# **MindFlux**

A modern twist on the classic Simon Says game. Watch the sequence of arrows, then repeat them using hand gestures. Built with **React**, **TypeScript**, **Chart.js** for analytics, and integrated with a **Python-based Mediapipe script** for gesture recognition and basic emotion tracking.

![Untitled](https://github.com/user-attachments/assets/bd4a8b3b-5570-4219-a1bc-5db6cd12e7ef)

---

## Table of Contents

1. [Overview](#overview)  
2. [Features](#features)  
3. [Use Cases & Benefits](#use-cases--benefits)  
4. [Challenges](#challenges)  
5. [How It Works](#how-it-works)  
6. [Setup & Installation](#setup--installation)  
   - [Prerequisites](#prerequisites)
   - [Installation Steps](#installation-steps)  
7. [Usage](#usage)  
8. [Dashboard & Analytics](#dashboard--analytics)  
9. [Python Requirements](#python-requirements)  
10. [Author Credits](#author-credits)  

---

## Overview

**MindFlux** is a Simon Says-inspired game that challenges players to replicate an increasingly longer sequence of directional arrows. Players can input responses using hand gestures, arrow keys, or on-screen buttons. Each successful round increases the sequence length; an incorrect response ends the game. 

The game also includes:

- **Analytics Dashboard** to track scores, gesture distribution, and emotion data over time.
- **Emotion Tracking** via a Python script using Mediapipe and DeepFace, enhancing the gameplay experience and providing insights into player behavior.

---

## Features

### Core Features
- **Dynamic Difficulty**
  - Each successful round adds a new direction to the sequence, increasing complexity.

- **Gesture-Based Input**
  - Uses [Mediapipe Hands](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker) to detect hand signals for game controls.

- **Emotion Tracking**
  - Integrates with [DeepFace](https://github.com/serengil/deepface) for emotion detection, enriching analytics.

- **Local Data Storage**
  - Automatically saves player scores, gesture usage, and emotions in the browser for future analysis.

- **Interactive Analytics Dashboard**
  - Displays performance metrics and emotion trends in user-friendly charts.

### Additional Features
- **Cross-Platform Support**
  - Playable on devices with keyboards, touchscreens, or cameras for hand gesture recognition.
- **Customizable Backend**
  - Python backend allows for easy integration of new gesture models or emotion recognition features.

---

## Use Cases & Benefits

### 1. Accessibility
- **Inclusive Gameplay:** Supports multiple input methods (gesture, keyboard, or on-screen buttons) to cater to players with varying physical abilities.
- **Adaptive Features:** Adjustable difficulty levels and gesture recognition make the game accessible to individuals with mobility challenges.

### 2. Cognitive and Motor Skill Development
- **Memory and Focus:** Enhances short-term memory, recall, and attentional control through repetitive pattern recognition.
- **Motor Skills:** Encourages active hand movements, aiding in fine motor skill development and rehabilitation.

### 3. Attention and Behavioral Screening
- **Focus Testing:** Highlights attention span and working memory challenges, potentially aiding in ADHD or executive function assessments.
- **Therapeutic Benefits:** Offers structured activities for cognitive rehabilitation, particularly for individuals recovering from brain injuries.

### 4. Emotional Insights
- Tracks and visualizes emotional responses during gameplay, providing valuable data for user behavior analysis or therapeutic applications.

---

## Challenges

### 1. Gesture Recognition Accuracy
- Real-time tracking may falter in suboptimal lighting or with complex backgrounds.
- Ensuring accurate detection across diverse hand shapes, sizes, and skin tones is a priority.

### 2. Performance Optimization
- Running Mediapipe and DeepFace alongside the React app can be resource-intensive.
- Efficient frame handling and reduced detection frequency are critical to maintaining smooth gameplay.

---

## How It Works

### Frontend (React)
1. **Gameplay Logic**
   - Generates a random sequence of directions (UP, RIGHT, DOWN, LEFT) for the player to mimic.
   - Handles inputs via keyboard, on-screen buttons, or hand gestures.

2. **Local Data Storage**
   - Saves session data (score, level, gestures, emotions) in the browser.

3. **Dashboard**
   - Visualizes player progress and behavior metrics using Chart.js.

### Backend (Python)
1. **Gesture Detection**
   - Uses Mediapipe to track hand landmarks and interpret gestures.
2. **Emotion Detection**
   - Employs DeepFace to analyze facial expressions and identify emotions (happy, sad, neutral, etc.).
3. **Data Transmission**
   - Sends gesture and emotion data to the React frontend via an API endpoint.

---

## Setup & Installation

### Prerequisites
- **Node.js** (v14+ recommended)
- **npm** or **yarn**
- **Python 3.7+**

### Installation Steps

#### Clone the Repository
```bash
git clone https://github.com/anastang/mindflux-v2.git
cd mindflux-v2
```

#### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python script.py
```

#### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Open the provided URL to access the app.

---

## Usage

1. Start the Python script to enable gesture and emotion detection.
2. Launch the React frontend to play the game.
3. Monitor performance and analytics via the Dashboard.

---

## Dashboard & Analytics

### Visualizations
- **Score & Level Progress (Line Chart):** Tracks how your score and level evolve across sessions.
- **Gesture Distribution (Pie Chart):** Displays frequency of each directional gesture.
- **Emotion Distribution (Bar Chart):** Aggregates detected emotions over gameplay.
![image](https://github.com/user-attachments/assets/c193fd4a-c01f-4dab-992a-380551ae4880)

---

## Python Requirements

Ensure the following Python libraries are installed:
- `mediapipe`
- `deepface`
- `flask`

Install dependencies using:
```bash
pip install -r requirements.txt
```

---

## Author Credits

- Anastan Gnanapragasam
- Adriel De Vera
- Romeo Junior Barbieto

---


