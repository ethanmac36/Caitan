from catan_ai import CatanSimulation
import argparse

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run Catan AI simulation')
    parser.add_argument('--players', type=int, default=4, help='Number of players (default: 2)')
    parser.add_argument('--games', type=int, default=10000, help='Number of games to simulate (default: 100)')
    parser.add_argument('--verbose', action='store_true', help='Print detailed game information')
    args = parser.parse_args()
    
    # Create a simulation with the specified parameters
    simulation = CatanSimulation(num_players=args.players, num_games=args.games, verbose=args.verbose)
    
    # Run the simulation
    print(f"Running Catan AI simulation with {args.players} players for {args.games} games...")
    simulation.run_simulation()
    
    # Print the results
    simulation.print_results()
    
    # Get and print the average resource values
    avg_values = simulation.get_resource_values()
    print("\nAverage Resource Values Across All Agents:")
    print("-" * 50)
    for resource_type, value in avg_values.items():
        print(f"{resource_type.value}: {value:.4f}")

if __name__ == "__main__":
    main() 