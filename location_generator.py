"""
Generates test datasets of emergency site locations for TSP analysis.
Creates JSON files with locations of varying sizes (5, 8, 10, 12, 15, 20 sites).
"""

import json
import random
import math
from pathlib import Path

def generate_locations(num_locations, seed=42):
    """
    Generate random emergency site locations in a 100x100 grid.
    
    Args:
        num_locations: Number of emergency sites to generate
        seed: Random seed for reproducibility
        
    Returns:
        Dictionary containing locations and distance matrix
    """
    random.seed(seed)
    
    # Generate random coordinates for emergency sites
    locations = []
    site_types = ['Hospital', 'Fire Station', 'Emergency Shelter', 'Police Station']
    
    for i in range(num_locations):
        x = random.uniform(0, 100)
        y = random.uniform(0, 100)
        site_type = random.choice(site_types)
        locations.append({
            'id': i,
            'name': f'{site_type} {i+1}',
            'x': round(x, 2),
            'y': round(y, 2)
        })
    
    # Calculate distance matrix
    distances = []
    for i in range(num_locations):
        row = []
        for j in range(num_locations):
            if i == j:
                distance = 0
            else:
                dx = locations[i]['x'] - locations[j]['x']
                dy = locations[i]['y'] - locations[j]['y']
                distance = math.sqrt(dx**2 + dy**2)
            row.append(round(distance, 2))
        distances.append(row)
    
    return {
        'num_locations': num_locations,
        'locations': locations,
        'distances': distances
    }

def main():
    """Generate all test datasets."""
    # Create data directory if it doesn't exist
    Path('data').mkdir(exist_ok=True)
    
    # Generate datasets of various sizes
    sizes = [5, 8, 10, 12, 15, 20]
    
    print("Generating emergency site datasets...")
    for size in sizes:
        data = generate_locations(size)
        filename = f'data/sites_{size}.json'
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"  Created {filename} with {size} locations")
    
    print("\nDataset generation complete!")
    print("Files created in 'data/' directory")

if __name__ == '__main__':
    main()