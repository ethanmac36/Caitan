import random
import numpy as np
from catan_game import CatanGame, ResourceType, BuildingType

class CatanAI:
    def __init__(self, player_id):
        self.player_id = player_id
        self.resource_correlation = {rt: 0.0 for rt in ResourceType}
        self.dev_correlation = {"knight" : 0, "victoryPoint" : 0, "roadBuilding" : 0, "yearOfPlenty" : 0, "monopoly" : 0}
        self.games_played = 0
        self.games_won = 0
    
    def make_move(self, game):
        """Make a random move in the game."""
        # This is a simple random strategy
        game.play_turn(self.player_id)
    
    def update_correlation(self, game_state, won):
        """Update resource correlation based on game outcome."""
        self.games_played += 1
        if won:
            self.games_won += 1
            
            # Get the player's resources at the end of the game
            player_data = game_state["players"][self.player_id]
            resources = player_data["legacyResources"]
            devs = player_data["upDevs"]

            for devName, count in devs.items():
                self.dev_correlation[devName] += count
            
            # Update correlation for each resource
            for resource_name, count in resources.items():
                resource_type = ResourceType(resource_name)
                # Simple correlation: more resources = more correlation with winning
                self.resource_correlation[resource_type] += count
    
    def get_resource_values(self):
        """Get the normalized resource values based on correlation with winning."""
        if self.games_played == 0:
            return {rt: 1.0 for rt in ResourceType}
        
        # Normalize the correlation values
        total_correlation = sum(self.resource_correlation.values())
        if total_correlation == 0:
            return {rt: 1.0 for rt in ResourceType}
        
        return {rt: corr / total_correlation for rt, corr in self.resource_correlation.items()}
    
    def get_dev_card_values(self):
        """Get normalized dev card values based on correlation with winning."""
        total = sum(self.dev_correlation.values())
        if total == 0:
            return {k: 1.0 for k in self.dev_correlation}
        
        return {k: v / total for k, v in self.dev_correlation.items()}

class CatanSimulation:
    def __init__(self, num_players=2, num_games=100, verbose=False):
        self.num_players = num_players
        self.num_games = num_games
        self.agents = [CatanAI(i) for i in range(num_players)]
        self.verbose = verbose
    
    def run_simulation(self):
        """Run the simulation for the specified number of games."""
        for game_num in range(self.num_games):
            if game_num % 1000 == 0:
                print(f"Finished Game {game_num}")
            # Create a new game
            game = CatanGame(self.num_players)
            
            if self.verbose:
                print(f"\nStarting Game {game_num + 1}/{self.num_games}")
                game.print_board()
            
            # Play until game is over
            while not game.game_over:
                for agent in self.agents:
                    agent.make_move(game)
                    
                    if self.verbose and game.turn_number % 5 == 0:  # Print every 5 turns
                        print(f"\nTurn {game.turn_number} - Player {agent.player_id}'s move:")
                        game.print_board()
            
            # Update correlations for all agents
            game_state = game.get_game_state()
            winner_id = game_state["winner"]
            
            for agent in self.agents:
                agent.update_correlation(game_state, agent.player_id == winner_id)
            
            if self.verbose:
                print(f"\nGame {game_num + 1} finished! Winner: Player {winner_id}")
                game.print_board()
    
    def print_results(self):
        """Print the simulation results."""
        print(f"Simulation Results ({self.num_games} games):")
        print("-" * 50)
        
        for agent in self.agents:
            win_rate = agent.games_won / agent.games_played * 100
            print(f"Agent {agent.player_id}: {agent.games_won} wins ({win_rate:.1f}%)")
            
            resource_values = agent.get_resource_values()
            print("Resource Values:")
            for resource_type, value in resource_values.items():
                print(f"  {resource_type.value}: {value:.4f}")
            print("-" * 50)
    
    def get_resource_values(self):
        """Get the average resource values across all agents, adjusted for resource availability."""
        # Step 1: Gather each agent’s normalized resource values
        all_values = [agent.get_resource_values() for agent in self.agents]

        # Step 2: Average across agents
        avg_values = {}
        for resource_type in ResourceType:
            values = [agent_vals[resource_type] for agent_vals in all_values]
            avg_values[resource_type] = sum(values) / len(values)

        # Step 3: Normalize by number of tiles (availability)
        RESOURCE_TILE_COUNTS = {
            ResourceType.LUMBER: 4,
            ResourceType.BRICK: 3,
            ResourceType.WOOL: 4,
            ResourceType.GRAIN: 4,
            ResourceType.ORE: 3,
        }

        # Step 4: Divide by tile count, then re-normalize to sum to 1
        weighted = {
            rt: avg_values[rt] / RESOURCE_TILE_COUNTS[rt]
            for rt in ResourceType
        }
        total_weighted = sum(weighted.values())
        final_values = {
            rt: value / total_weighted
            for rt, value in weighted.items()
        }

        return final_values
    
    def get_dev_card_values(self):
        """Get the average dev card values across all agents, weighted by card frequency."""
        all_values = [agent.get_dev_card_values() for agent in self.agents]

        # Step 1: Average across agents
        avg_values = {}
        for card in self.agents[0].dev_correlation:
            values = [agent_vals[card] for agent_vals in all_values]
            avg_values[card] = sum(values) / len(values)

        # Step 2: Weight by dev card frequency
        DEV_CARD_COUNTS = {
            "knight": 14,
            "victoryPoint": 5,
            "roadBuilding": 2,
            "yearOfPlenty": 2,
            "monopoly": 2,
        }

        weighted = {
            card: avg_values[card] / DEV_CARD_COUNTS[card]
            for card in avg_values
        }

        # Step 3: Re-normalize to sum to 1
        total_weighted = sum(weighted.values())
        final_values = {
            card: value / total_weighted
            for card, value in weighted.items()
        }

        return final_values
