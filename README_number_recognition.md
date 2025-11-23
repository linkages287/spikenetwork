# Number Recognition with Spike Neural Network

This system implements a spike neural network that can be trained to recognize digits (0-9) using STDP (Spike-Timing Dependent Plasticity) learning.

## Features

- **STDP Learning**: Implements Spike-Timing Dependent Plasticity for unsupervised/supervised learning
- **Number Recognition**: Trains on synthetic digit patterns (0-9)
- **3D Visualization**: Visualize the network structure in 3D space
- **Data Generation**: Automatically generates synthetic digit patterns for training

## Building

```bash
make train_numbers
```

This will compile the training program.

## Training the Network

### Basic Training

```bash
./train_numbers
```

This will train the network with default parameters:
- 10 epochs
- Learning rate: 0.01
- 20 samples per digit

### Custom Training

```bash
./train_numbers <epochs> <learning_rate>
```

Example:
```bash
./train_numbers 20 0.02
```

### Training Process

The training program will:
1. Create a network with:
   - 49 input neurons (7x7 grid for digit images)
   - 50 hidden neurons
   - 10 output neurons (one for each digit 0-9)

2. Generate synthetic digit patterns for training

3. Train using STDP learning rule:
   - Pre-synaptic spike before post-synaptic → strengthen connection (LTP)
   - Post-synaptic spike before pre-synaptic → weaken connection (LTD)

4. Save the trained network to `trained_network.json`

5. Test on sample examples and show accuracy

## Visualizing the Network

### 3D Visualization

After training, visualize the network structure in 3D:

```bash
python3 visualize_3d.py trained_network.json
```

Or using the Makefile:
```bash
make visualize-3d
```

### 3D Layout Options

```bash
# Layered layout (default - shows input/hidden/output layers)
python3 visualize_3d.py trained_network.json --layout layered

# Spring layout (force-directed)
python3 visualize_3d.py trained_network.json --layout spring

# Circular layout
python3 visualize_3d.py trained_network.json --layout circular

# Spherical layout
python3 visualize_3d.py trained_network.json --layout spherical
```

### Visualization Options

```bash
# Hide labels
python3 visualize_3d.py trained_network.json --no-labels

# Adjust node size
python3 visualize_3d.py trained_network.json --node-size 200

# Adjust edge width
python3 visualize_3d.py trained_network.json --edge-width 3

# Save to file instead of displaying
python3 visualize_3d.py trained_network.json --save network_3d.png
```

## Network Architecture

The network has a feed-forward architecture:

```
Input Layer (49 neurons) → Hidden Layer (50 neurons) → Output Layer (10 neurons)
```

- **Input Layer**: Receives pixel values from 7x7 digit images
- **Hidden Layer**: Processes features through weighted connections
- **Output Layer**: Each neuron represents one digit (0-9)

## STDP Learning Rule

The network uses Spike-Timing Dependent Plasticity:

- **Long-Term Potentiation (LTP)**: If pre-synaptic neuron spikes before post-synaptic neuron, the connection weight increases
- **Long-Term Depression (LTD)**: If post-synaptic neuron spikes before pre-synaptic neuron, the connection weight decreases

The weight update follows:
- LTP: Δw = learning_rate × exp(-Δt / τ_plus)
- LTD: Δw = -learning_rate × exp(Δt / τ_minus)

Where Δt is the time difference between spikes.

## Output

After training, the program will:
1. Display training progress for each epoch
2. Show accuracy and loss metrics
3. Save the trained network to `trained_network.json`
4. Test on sample digits and show predictions

## Example Output

```
=== Epoch 1/10 ===
  Sample 10/200 - Label: 3, Predicted: 3 ✓
  Sample 20/200 - Label: 7, Predicted: 7 ✓
  ...

Epoch 1 Results:
  Accuracy: 45.50% (91/200)
  Average Loss: 0.8234
```

## Files

- `train_numbers.cpp`: Training program
- `load_numbers.cpp`: Data loader (can be used separately)
- `visualize_3d.py`: 3D visualization script
- `trained_network.json`: Saved network after training (generated)

## Requirements

- C++11 compiler (g++)
- Python 3 with matplotlib and networkx
- Make (for building)

## Tips

1. **More epochs**: Increase epochs for better accuracy (may take longer)
2. **Learning rate**: Lower learning rates (0.001-0.01) for more stable training
3. **Network size**: Adjust hidden layer size in `train_numbers.cpp` for different capacity
4. **3D visualization**: Try different layouts to see the network from different perspectives

## Troubleshooting

- **Compilation errors**: Make sure you have C++11 support
- **Python errors**: Install required packages: `pip install matplotlib networkx numpy`
- **Low accuracy**: Try more epochs or adjust learning rate
- **Visualization not showing**: Make sure you have a display (or use --save option)

