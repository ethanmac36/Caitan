# Catan AI Framework

A simple framework for simulating Catan games with AI agents that make random moves and analyze resource correlations with winning.

## Features

- Basic Catan game engine with core mechanics
- AI agents that make random moves
- Simulation of multiple games
- Resource correlation analysis with winning
- Win rate statistics for each agent
- Visual board representation

## Installation

1. Clone this repository
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the main script to start a simulation with 2 players and 100 games:
```bash
python main.py
```

### Command Line Options

The simulation can be customized with the following command line arguments:

- `--players N`: Set the number of players (default: 2)
- `--games N`: Set the number of games to simulate (default: 100)
- `--verbose`: Enable detailed output including board visualization

Example:
```bash
python main.py --players 3 --games 50 --verbose
```

### Understanding the Results

The simulation will output:
1. Win rates for each agent
2. Resource correlation values for each agent
3. Average resource values across all agents

The resource values indicate how strongly each resource type is correlated with winning games. Higher values suggest that resource is more important for winning.

## Project Structure

- `catan_game.py`: Core game engine with game state and rules
- `catan_ai.py`: AI agent framework and simulation runner
- `main.py`: Main script to run the simulation
- `requirements.txt`: Required Python packages

## Extending the Framework

You can extend this framework by:
1. Implementing more sophisticated AI strategies in the `CatanAI` class
2. Adding more game mechanics to the `CatanGame` class
3. Enhancing the correlation analysis with more sophisticated metrics 