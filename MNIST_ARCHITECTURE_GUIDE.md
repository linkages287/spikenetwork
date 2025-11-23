# MNIST Architecture Guide

## Recommended Network Architectures for MNIST

MNIST dataset: **28×28 = 784 pixels**, **10 classes (digits 0-9)**

## Architecture Recommendations

### 1. Simple Architecture (784 → 300 → 10) **[Quick Test]**
```
Layers: 3 (Input + 1 Hidden + Output)
Total Neurons: 1,094
Connections: ~245,700
Training Time: ~5-10 minutes
Expected Accuracy: 60-70%
```

**Best for:**
- Quick testing and prototyping
- Limited computational resources
- Understanding the basic workflow

**Usage:**
```bash
./train_mnist simple 0.01 5
```

---

### 2. Medium Architecture (784 → 400 → 200 → 10) **[RECOMMENDED]**
```
Layers: 4 (Input + 2 Hidden + Output)
Total Neurons: 1,394
Connections: ~415,400
Training Time: ~30-60 minutes
Expected Accuracy: 75-85%
```

**Best for:**
- Best balance of accuracy and training time
- Production use
- Good feature extraction

**Usage:**
```bash
./train_mnist medium 0.01 10
```

---

### 3. Complex Architecture (784 → 512 → 256 → 128 → 10) **[Maximum Accuracy]**
```
Layers: 5 (Input + 3 Hidden + Output)
Total Neurons: 1,690
Connections: ~591,360
Training Time: ~1-2 hours
Expected Accuracy: 80-90%
```

**Best for:**
- Maximum accuracy
- Research experiments
- When training time is not critical

**Usage:**
```bash
./train_mnist complex 0.01 20
```

## Layer-by-Layer Explanation

### Input Layer (784 neurons)
- **Purpose**: Receives pixel values from 28×28 MNIST images
- **Encoding**: Rate coding (pixel intensity → input current)
- **One neuron per pixel**

### Hidden Layer 1 (300-512 neurons)
- **Purpose**: Detect edges, lines, and basic patterns
- **Extracts**: Local features from pixels
- **Size**: 300 (simple) to 512 (complex)

### Hidden Layer 2 (200-256 neurons)
- **Purpose**: Combine features, detect shapes and curves
- **Extracts**: Mid-level features (circles, lines combinations)
- **Size**: 200 (medium) to 256 (complex)

### Hidden Layer 3 (128 neurons) - Complex only
- **Purpose**: High-level digit patterns
- **Extracts**: Complete digit representations
- **Size**: 128 neurons

### Output Layer (10 neurons)
- **Purpose**: Classify into digit classes (0-9)
- **One neuron per digit**
- **Prediction**: Neuron with most spikes = predicted digit

## Number of Layers Recommendation

| Layers | Neurons | Best For | Accuracy |
|--------|---------|----------|----------|
| 2 (input+output) | 794 | Too simple | Poor |
| 3 (input+1 hidden+output) | 1,094 | Quick tests | 60-70% |
| **4 (input+2 hidden+output)** | **1,394** | **Recommended** | **75-85%** |
| 5 (input+3 hidden+output) | 1,690 | Maximum accuracy | 80-90% |
| 6+ layers | 2,000+ | Diminishing returns | 80-92% |

**Recommendation: 4 layers (1 input + 2 hidden + 1 output)**

## Number of Neurons Recommendation

### Input Layer: **784 neurons** (fixed - one per pixel)
### Hidden Layers:
- **Hidden 1**: 300-512 neurons (400 recommended)
- **Hidden 2**: 200-256 neurons (200 recommended)
- **Hidden 3**: 128 neurons (optional, for complex architecture)

### Output Layer: **10 neurons** (fixed - one per digit)

## Memory Requirements

- **Simple**: ~2-4 GB RAM
- **Medium**: ~4-8 GB RAM
- **Complex**: ~8-16 GB RAM

## Training Tips

1. **Start with Medium Architecture** - Best balance
2. **Epochs**: 10-30 recommended (more epochs = better accuracy)
3. **Learning Rate**: 0.001-0.01 (lower = more stable)
4. **Simulation Steps**: 30-50 time steps per sample
5. **Use Real MNIST**: Synthetic data is for testing only

## Getting MNIST Data

### Option 1: CSV Format (Easiest)
Download from Kaggle:
```
https://www.kaggle.com/datasets/oddrationale/mnist-in-csv
```
Then use:
```bash
./train_mnist medium 0.01 10 mnist_train.csv
```

### Option 2: Original Binary Format
Download from:
```
http://yann.lecun.com/exdb/mnist/
```

## Example Training Commands

```bash
# Quick test with simple architecture
./train_mnist simple 0.01 5

# Recommended training
./train_mnist medium 0.01 20

# Maximum accuracy (longer training)
./train_mnist complex 0.01 30

# With real MNIST data
./train_mnist medium 0.01 20 mnist_train.csv
```

## Performance Expectations

With real MNIST dataset:

| Architecture | Training Time | Test Accuracy* |
|-------------|---------------|----------------|
| Simple      | 5-10 min      | 60-70%         |
| Medium      | 30-60 min     | 75-85%         |
| Complex     | 1-2 hours     | 80-90%         |

*Accuracy depends on training epochs, learning rate, and data quality

## Summary

**For MNIST:**
- **Recommended Layers**: 4 (1 input + 2 hidden + 1 output)
- **Recommended Neurons**: 784 → 400 → 200 → 10 (total: 1,394)
- **Total Connections**: ~415,400
- **This architecture provides the best balance of accuracy and training time**



