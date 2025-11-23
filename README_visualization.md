# Spike Neural Network Visualization

This directory contains a Python visualization tool for dynamically viewing the spike neural network connections and states.

## Quick Setup

The easiest way to set up the visualization environment:

```bash
# Option 1: Use the setup script (recommended)
./setup_visualization.sh

# Option 2: Use make
make setup-venv
```

This will:
- Create a Python virtual environment (`venv/`)
- Install all required dependencies (matplotlib, networkx, numpy)
- Verify the installation

## Manual Setup

If you prefer to set up manually:

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt
```

## Requirements

The visualization requires:
- Python 3.6+
- matplotlib >= 3.5.0
- networkx >= 2.6.0
- numpy >= 1.21.0

## Usage

### 1. Export Network State from C++

First, compile and run the export program:
```bash
make export_network
./export_network network_state.json 10
```

This creates JSON files for each simulation step.

### 2. Visualize Network

#### Static Visualization
View a single network state:

**With virtual environment:**
```bash
source venv/bin/activate
python visualize_network.py network_state_step0.json
```

**Without virtual environment:**
```bash
python3 visualize_network.py network_state_step0.json
```

#### Dynamic Time Series Visualization (NEW!)
View connections dynamically as they activate over multiple time steps:
```bash
source venv/bin/activate
python visualize_network.py network_state_step0.json --time-series
```

This will:
- Automatically detect and load all step files (network_state_step0.json, step1.json, etc.)
- Animate through all time steps
- **Highlight active connections** in bright orange when spikes propagate
- Show connection activity in real-time
- Loop continuously (use `--no-loop` to play once)

Options:
```bash
# Customize animation speed
python visualize_network.py network_state_step0.json --time-series --interval 1.0

# Load specific number of steps
python visualize_network.py network_state_step0.json --time-series --steps 10

# Show connection statistics after animation
python visualize_network.py network_state_step0.json --time-series --stats
```

#### Animated Visualization (Single File)
View dynamic updates from a single file that gets updated:
```bash
source venv/bin/activate
python visualize_network.py network_state.json --animate --interval 0.5
```

### 3. Quick Test

Run the complete workflow (includes setup):
```bash
make demo
```

Or just visualize (after setup):
```bash
make visualize
```

## Visualization Features

### Static Visualization
- **Nodes (Neurons)**: 
  - Color intensity represents membrane potential (darker = higher potential)
  - Red color indicates a neuron has just spiked
  - Size increases with potential
  - Labels show: neuron ID, current potential, total spike count

- **Edges (Connections)**:
  - Arrow direction shows signal flow
  - Thickness represents connection weight
  - Labels show weight values

### Dynamic Connection Visualization (NEW!)
- **Active Connections**: 
  - **Bright orange dashed lines** highlight connections that just transmitted spikes
  - Thicker lines for active connections (5x weight)
  - Inactive connections shown in light gray (2x weight, low opacity)
  - Real-time detection of spike propagation through connections

- **Connection Activity Tracking**:
  - Tracks which connections are used most frequently
  - Statistics show most active pathways
  - Helps identify critical connection patterns

- **Time Series Animation**:
  - Automatically loads all step files
  - Smooth animation through time steps
  - Shows how network state evolves
  - Visualizes spike propagation in real-time

- **Layout**: Spring-based layout for optimal node positioning

## Example Workflow

### Basic Workflow
```bash
# 1. Export network state (creates multiple step files)
./export_network my_network.json 10

# 2. View first step (static)
python visualize_network.py my_network_step0.json

# 3. View all steps dynamically (recommended!)
python visualize_network.py my_network_step0.json --time-series
```

### Advanced Workflow
```bash
# 1. Export with many steps
./export_network my_network.json 20

# 2. Animate with custom settings
python visualize_network.py my_network_step0.json --time-series \
    --interval 0.5 --steps 15 --stats

# 3. View connection statistics
# (Statistics shown after animation with --stats flag)
```

### Manual Step-by-Step Viewing
```bash
# View each step individually
for i in {0..9}; do
    python visualize_network.py my_network_step${i}.json
done
```

## Integration with Main Program

You can modify `main.cpp` to export network state at each step:

```cpp
#include <fstream>
// ...
for (int step = 0; step < 10; ++step) {
    network.update();
    
    std::ofstream out("network_step" + std::to_string(step) + ".json");
    network.export_to_json(out);
    out.close();
}
```

