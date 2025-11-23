# Full Process Script

The `run_full_process.sh` script automates the complete workflow for the Spike Neural Network project.

## Usage

### Basic (default settings):
```bash
./run_full_process.sh
```

### Custom parameters:
```bash
./run_full_process.sh [epochs] [learning_rate] [test_digit] [simulation_steps]
```

### Examples:

**Quick test (3 epochs, digit 5):**
```bash
./run_full_process.sh 3 0.01 5 20
```

**Full training (10 epochs, digit 0, 50 steps):**
```bash
./run_full_process.sh 10 0.01 0 50
```

## What the Script Does

1. **Build** - Cleans and compiles all C++ programs
2. **Setup** - Checks/creates Python virtual environment
3. **Train** - Trains the network for number recognition
4. **Simulate** - Runs spiking simulation with test digit
5. **Visualize** - Generates all visualization diagrams
6. **Summary** - Shows generated files and next steps

## Generated Outputs

After running, you'll have:

- **Trained Network**: `data/json/trained_network.json`
- **Animation Frames**: `data/json/spike_animation_step*.json`
- **Visualizations**:
  - `network_3d_structure.png` - 3D network structure
  - `project_structure.png` - Complete project file structure
  - `neuron_structure.png` - Neuron component diagram
  - `neuron_code_structure.png` - Neuron code structure

## Parameters

- **epochs**: Number of training epochs (default: 5)
- **learning_rate**: Learning rate for STDP (default: 0.01)
- **test_digit**: Digit to test (0-9, default: 0)
- **simulation_steps**: Number of simulation time steps (default: 30)

## Troubleshooting

If the script fails:
1. Check that `make` works: `make clean && make`
2. Ensure Python dependencies: `make setup-venv`
3. Check file permissions: `chmod +x run_full_process.sh`

## Quick Commands After Running

```bash
# View 3D spiking animation
python animate_3d_spiking.py data/json/spike_animation_step0.json

# View 2D animation
python visualize_network.py data/json/spike_animation_step0.json --time-series

# View 3D network structure
python visualize_3d.py data/json/trained_network.json
```



