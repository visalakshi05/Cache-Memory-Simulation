# Cache-Memory-Simulation
## Overview
- This program simulates a multi-level cache system, including L1, L2, and a victim cache, to optimize memory access.
- It manages both load and store operations, ensuring efficient data retrieval and storage.

## Features
- **Cache Levels**: Implements L1 cache, L2 cache, and a victim cache for improved memory access efficiency.
- **Cache Hit and Miss Handling**: 
  - Checks L1 cache first for data retrieval.
  - Falls back to the victim cache if a miss occurs in L1.
  - Checks L2 cache if the victim cache also results in a miss.
- **Dynamic Updates**: 
  - Updates cache lines and handles replacements when caches are full.
  - Transfers data between caches and main memory as required.
- **User Input**: 
  - Allows users to input memory addresses and choose between load and store operations.

## Requirements
- Python IDLE
- prettytable library

## Usage
1. Clone the repository to your local machine.
2. Run the program using Python.
3. Follow the on-screen prompts to interact with the cache simulation.







