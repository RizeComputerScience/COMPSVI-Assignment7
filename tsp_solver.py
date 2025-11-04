"""
TSP Solver implementing brute force and nearest neighbor approximation algorithms.
Includes timing and comparison utilities for analyzing computational limits.
"""

import json
import time
import itertools
import sys
from pathlib import Path

# ============================================================================
# BRUTE FORCE SOLUTION
# ============================================================================

def tsp_brute_force(distances, timeout=60):
    """
    Find optimal TSP route by checking all possible permutations.
    
    Args:
        distances: 2D list where distances[i][j] is distance from location i to j
        timeout: Maximum seconds to run before stopping (default 60)
        
    Returns:
        Tuple of (best_route, best_distance) or (None, None) if timeout
    """
    n = len(distances)
    locations = list(range(n))
    
    # Start at location 0 (dispatch center)
    start = 0
    other_locations = [i for i in locations if i != start]
    
    best_distance = float('inf')
    best_route = None
    start_time = time.time()
    routes_checked = 0
    
    # Check all permutations of locations (excluding start)
    for perm in itertools.permutations(other_locations):
        # Check if we've exceeded timeout
        if time.time() - start_time > timeout:
            print(f"    TIMEOUT after checking {routes_checked:,} routes")
            return None, None
        
        # Build full route: start -> permutation -> back to start
        route = [start] + list(perm) + [start]
        
        # Calculate total distance for this route
        distance = 0
        for i in range(len(route) - 1):
            distance += distances[route[i]][route[i + 1]]
        
        # Update best if this is better
        if distance < best_distance:
            best_distance = distance
            best_route = route[:-1]  # Remove duplicate start at end
        
        routes_checked += 1
    
    return best_route, best_distance

# ============================================================================
# NEAREST NEIGHBOR APPROXIMATION
# ============================================================================

def tsp_nearest_neighbor(distances, start=0):
    """
    Find approximate TSP route using nearest neighbor heuristic.
    Always travels to the nearest unvisited location.
    
    Args:
        distances: 2D list where distances[i][j] is distance from location i to j
        start: Starting location index (default 0 for dispatch center)
        
    Returns:
        Tuple of (route, total_distance)
    """
    n = len(distances)
    
    # Track which locations we've visited
    unvisited = set(range(n))
    current = start
    route = [current]
    unvisited.remove(current)
    total_distance = 0
    
    # Visit each location
    while unvisited:
        # Find nearest unvisited location
        nearest = min(unvisited, key=lambda x: distances[current][x])
        
        # Travel to nearest location
        total_distance += distances[current][nearest]
        current = nearest
        route.append(current)
        unvisited.remove(current)
    
    # Return to start
    total_distance += distances[current][start]
    
    return route, total_distance

# ============================================================================
# TESTING AND TIMING UTILITIES
# ============================================================================

def load_dataset(size):
    """Load emergency site dataset of given size."""
    filename = f'data/sites_{size}.json'
    if not Path(filename).exists():
        print(f"Error: {filename} not found. Run location_generator.py first.")
        sys.exit(1)
    
    with open(filename, 'r') as f:
        return json.load(f)

def test_small_cases():
    """Test both algorithms on small datasets with known correct results."""
    print("\n" + "="*70)
    print("TESTING: Small Cases (Verifying Correctness)")
    print("="*70)
    
    test_sizes = [5, 8, 10]
    
    for size in test_sizes:
        print(f"\nTesting {size} locations...")
        data = load_dataset(size)
        distances = data['distances']
        
        # Test brute force
        route_bf, dist_bf = tsp_brute_force(distances)
        print(f"  Brute Force: Distance = {dist_bf:.2f}")
        
        # Test nearest neighbor
        route_nn, dist_nn = tsp_nearest_neighbor(distances)
        print(f"  Nearest Neighbor: Distance = {dist_nn:.2f}")
        print(f"  Approximation Quality: {(dist_nn/dist_bf)*100:.1f}% of optimal")

def time_brute_force():
    """Time brute force algorithm on increasing dataset sizes."""
    print("\n" + "="*70)
    print("TIMING: Brute Force Algorithm")
    print("="*70)
    print("\nWARNING: Larger sizes may take several minutes or timeout at 60 seconds")
    
    sizes = [5, 8, 10, 12, 15]
    
    print(f"\n{'Size':<6} {'Routes':<15} {'Time (s)':<12} {'Distance':<12} {'Status'}")
    print("-" * 70)
    
    for size in sizes:
        data = load_dataset(size)
        distances = data['distances']
        
        # Calculate number of routes to check
        import math
        num_routes = math.factorial(size - 1)  # (n-1)! for fixed start
        
        # Time the algorithm
        start_time = time.time()
        route, distance = tsp_brute_force(distances, timeout=60)
        elapsed = time.time() - start_time
        
        if route is None:
            print(f"{size:<6} {num_routes:<15,} {elapsed:<12.3f} {'N/A':<12} TIMEOUT")
        else:
            print(f"{size:<6} {num_routes:<15,} {elapsed:<12.3f} {distance:<12.2f} Complete")

def time_approximation():
    """Time nearest neighbor approximation on increasing dataset sizes."""
    print("\n" + "="*70)
    print("TIMING: Nearest Neighbor Approximation")
    print("="*70)
    
    sizes = [5, 8, 10, 12, 15, 20]
    
    print(f"\n{'Size':<6} {'Time (s)':<12} {'Distance':<12}")
    print("-" * 40)
    
    for size in sizes:
        data = load_dataset(size)
        distances = data['distances']
        
        # Time the algorithm
        start_time = time.time()
        route, distance = tsp_nearest_neighbor(distances)
        elapsed = time.time() - start_time
        
        print(f"{size:<6} {elapsed:<12.6f} {distance:<12.2f}")

def compare_all_approaches():
    """Compare brute force and approximation side-by-side."""
    print("\n" + "="*70)
    print("COMPARISON: Brute Force vs Nearest Neighbor")
    print("="*70)
    print("\nThis compares both algorithms on datasets where brute force completes.")
    
    sizes = [5, 8, 10]
    
    print(f"\n{'Size':<6} {'Optimal':<12} {'Approx':<12} {'% of Optimal':<14} {'BF Time (s)':<14} {'NN Time (s)':<12}")
    print("-" * 90)
    
    for size in sizes:
        data = load_dataset(size)
        distances = data['distances']
        
        # Brute force
        start_time = time.time()
        route_bf, dist_bf = tsp_brute_force(distances, timeout=60)
        time_bf = time.time() - start_time
        
        # Nearest neighbor
        start_time = time.time()
        route_nn, dist_nn = tsp_nearest_neighbor(distances)
        time_nn = time.time() - start_time
        
        if route_bf is None:
            print(f"{size:<6} {'TIMEOUT':<12} {dist_nn:<12.2f} {'N/A':<14} {'TIMEOUT':<14} {time_nn:<12.6f}")
        else:
            quality = (dist_nn / dist_bf) * 100
            print(f"{size:<6} {dist_bf:<12.2f} {dist_nn:<12.2f} {quality:<14.1f} {time_bf:<14.3f} {time_nn:<12.6f}")
    
    print("\n" + "="*70)
    print("Note: Approximation runs in polynomial time, handling larger sizes easily.")
    print("Brute force becomes impractical beyond 12-15 locations.")
    print("="*70)

# ============================================================================
# MAIN INTERFACE
# ============================================================================

def print_usage():
    """Print usage instructions."""
    print("\nUsage: python tsp_solver.py [option]")
    print("\nOptions:")
    print("  --test-small        Test correctness on small datasets")
    print("  --time-brute-force  Time brute force on increasing sizes")
    print("  --time-approximation Time approximation on increasing sizes")
    print("  --compare-all       Compare both algorithms side-by-side")
    print("  --help              Show this help message")
    print("\nFor the assignment, run these commands in order:")
    print("  1. python tsp_solver.py --test-small")
    print("  2. python tsp_solver.py --time-brute-force")
    print("  3. python tsp_solver.py --time-approximation")
    print("  4. python tsp_solver.py --compare-all")

def main():
    """Main entry point for running timing experiments."""
    if len(sys.argv) < 2:
        print_usage()
        return
    
    option = sys.argv[1]
    
    # Check if data files exist
    if not Path('data/sites_5.json').exists():
        print("\nError: Data files not found!")
        print("Please run: python location_generator.py")
        print("This will create the required test datasets.")
        sys.exit(1)
    
    if option == '--test-small':
        test_small_cases()
    elif option == '--time-brute-force':
        time_brute_force()
    elif option == '--time-approximation':
        time_approximation()
    elif option == '--compare-all':
        compare_all_approaches()
    elif option == '--help':
        print_usage()
    else:
        print(f"\nError: Unknown option '{option}'")
        print_usage()

if __name__ == '__main__':
    main()