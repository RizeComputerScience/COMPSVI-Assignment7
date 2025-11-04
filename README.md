# TSP Assignment: Computational Limits

This repository contains implementations for analyzing the Traveling Salesman Problem (TSP) and understanding computational limits.

## Setup

1. Clone this repository
2. Navigate to the repository directory
3. Generate the test datasets:
   ```bash
   python location_generator.py
   ```

This creates a `data/` directory with emergency site datasets of various sizes (5, 8, 10, 12, 15, 20 locations).

## Running the Code

The assignment asks you to run four different commands to analyze the algorithms:

### 1. Test Small Cases (Verify Correctness)
```bash
python tsp_solver.py --test-small
```
Tests both brute force and nearest neighbor on small datasets to verify they produce correct results.

### 2. Time Brute Force Algorithm
```bash
python tsp_solver.py --time-brute-force
```
Times the brute force algorithm on datasets of size 5, 8, 10, 12, and 15.
**Warning:** Larger sizes may take several minutes or timeout after 60 seconds.

### 3. Time Approximation Algorithm
```bash
python tsp_solver.py --time-approximation
```
Times the nearest neighbor approximation on datasets of size 5, 8, 10, 12, 15, and 20.

### 4. Compare Both Algorithms
```bash
python tsp_solver.py --compare-all
```
Compares brute force and approximation side-by-side on small datasets where both can complete.

## File Structure

```
.
├── README.md                  # This file
├── location_generator.py      # Generates test datasets
├── tsp_solver.py             # TSP algorithm implementations and timing utilities
└── data/                     # Generated test datasets
    ├── sites_5.json
    ├── sites_8.json
    ├── sites_10.json
    ├── sites_12.json
    ├── sites_15.json
    └── sites_20.json
```

## Need Help?

If you get an error about missing data files, make sure you've run:
```bash
python location_generator.py
```

If you need to see all available options:
```bash
python tsp_solver.py --help
```