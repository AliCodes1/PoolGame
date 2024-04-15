# Interactive Pool Game Application

## Overview

This interactive pool game is a web-based application designed to simulate a realistic pool game using advanced physics calculations and a responsive web interface. The project is structured into three main components: the game physics engine written in C, the server-side logic in Python using `http.server`, and the front-end using HTML, CSS, and JavaScript.

## Architecture

### Physics Engine

The core of the game's realism lies in its physics engine, developed in C for high-performance computation. This engine handles:
- **Collision detection and response:** Determines when and how balls collide with each other and the pool table boundaries.
- **Motion simulation:** Calculates the trajectory and speed of each ball on the table using physical laws of motion.
- **Velocity and acceleration:** Manages changes in velocity and acceleration due to impacts and table friction.

### Server

The server-side of the application is implemented using Python’s built-in `http.server` module, facilitating a lightweight and extensible framework for handling HTTP requests. Key functionalities include:
- **API endpoints:** Serve game state, process game actions like shots, and manage game sessions.
- **Database interaction:** Utilizes SQLite to persist game data such as player scores, ball positions, and game outcomes, enabling session recovery and history tracking.
- **Real-time communication:** Sends updated game states to the client, ensuring that the game display is synchronized with the physics engine's output.

### Front-end

The front-end is crafted using HTML5, CSS3, and JavaScript to provide a dynamic and interactive user experience:
- **SVG Rendering:** Uses Scalable Vector Graphics (SVG) to render the pool table and balls, allowing for precise and smooth graphical representations.
- **Game Control Interface:** Includes controls for game settings, shot power, angle adjustments, and a reset game feature.
- **AJAX:** Leverages AJAX for asynchronous data fetching to update the game state without reloading the webpage, enhancing user interaction and responsiveness.

## Features

- **Interactive Gameplay:** Players can interact directly with the game interface, selecting the direction and strength of each shot.
- **Real-Time Updates:** Game state updates are displayed in real-time, thanks to efficient communication between the front-end and server.
- **Persistence and Recovery:** Player progress and game states are saved, allowing sessions to be paused and resumed at any time.
- **Multiplayer Capability:** Supports multiple players in a competitive format, tracking scores and turns.

## Technologies Used

- **C:** For implementing the physics engine.
- **Python:** For server-side application logic.
- **SQLite:** For database management.
- **HTML/CSS/JavaScript:** For building the interactive front-end.
- **SVG:** For rendering game elements dynamically on the web page.

