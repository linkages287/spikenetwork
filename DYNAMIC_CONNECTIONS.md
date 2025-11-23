# Dynamic Connection Visualization

## Overview

The visualization now supports **dynamic connection viewing** that shows how connections between neurons activate and propagate spikes in real-time.

## Key Features

### 1. Active Connection Highlighting
- **Bright orange dashed lines** show connections that just transmitted spikes
- **Thicker lines** (5x weight) for active connections vs. inactive (2x weight)
- **Real-time detection** of spike propagation through the network

### 2. Time Series Animation
Automatically loads and animates through multiple time step files:
```bash
python visualize_network.py network_step0.json --time-series
```

### 3. Connection Activity Tracking
Tracks which connections are used most frequently:
```bash
python visualize_network.py network_step0.json --time-series --stats
```

## Usage Examples

### Basic Dynamic View
```bash
# Export network with multiple steps
./export_network network.json 10

# View dynamically
python visualize_network.py network_step0.json --time-series
```

### Customized Animation
```bash
# Slower animation (1 second per step)
python visualize_network.py network_step0.json --time-series --interval 1.0

# Load only first 5 steps
python visualize_network.py network_step0.json --time-series --steps 5

# Play once (no loop)
python visualize_network.py network_step0.json --time-series --no-loop

# Show statistics after animation
python visualize_network.py network_step0.json --time-series --stats
```

## Visual Indicators

### Connection States
- **Active (Orange, Dashed, Thick)**: Connection just transmitted a spike
- **Inactive (Gray, Thin)**: Connection not currently active
- **Node Red**: Neuron just spiked
- **Node Color Intensity**: Membrane potential level

### Connection Detection
The system detects active connections by:
1. Identifying neurons that just spiked
2. Marking all outgoing connections from spiked neurons
3. Detecting potential increases in target neurons (received spikes)
4. Highlighting the connection path

## Benefits

1. **Understand Network Dynamics**: See how information flows through the network
2. **Identify Critical Pathways**: Discover which connections are most important
3. **Debug Network Behavior**: Visualize why certain neurons spike
4. **Optimize Connections**: See which connections are rarely used

## Example Output

When running with `--stats`, you'll see:
```
=== Connection Activity Statistics ===

Most Active Connections (used 10 time steps):
  0 -> 1: 3 activations
  1 -> 2: 2 activations
  2 -> 3: 2 activations
  ...

Total unique connections used: 15
Total activations: 25
```

This helps identify the most important connection pathways in your network!

