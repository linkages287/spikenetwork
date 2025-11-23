# MNIST Dataset Training Guide

## Network Architecture Recommendations

For MNIST (28x28 = 784 pixels, 10 classes), here are recommended architectures:

### Architecture Options:

#### 1. **Simple Architecture** (784 → 300 → 10)
- **Input**: 784 neurons (one per pixel)
- **Hidden**: 300 neurons (single layer)
- **Output**: 10 neurons (one per digit)
- **Total**: 1,094 neurons
- **Connections**: ~245,700 connections
- **Best for**: Quick testing, faster training, lower memory

#### 2. **Medium Architecture** (784 → 400 → 200 → 10) **[RECOMMENDED]**
- **Input**: 784 neurons
- **Hidden 1**: 400 neurons
- **Hidden 2**: 200 neurons
- **Output**: 10 neurons
- **Total**: 1,394 neurons
- **Connections**: ~415,400 connections
- **Best for**: Balanced performance and accuracy

#### 3. **Complex Architecture** (784 → 512 → 256 → 128 → 10)
- **Input**: 784 neurons
- **Hidden 1**: 512 neurons
- **Hidden 2**: 256 neurons
- **Hidden 3**: 128 neurons
- **Output**: 10 neurons
- **Total**: 1,690 neurons
- **Connections**: ~591,360 connections
- **Best for**: Maximum accuracy, more training time

## Why These Architectures?

1. **Input Layer (784 neurons)**: One neuron per pixel in 28x28 MNIST images
2. **Hidden Layers**: Extract features from pixel patterns
   - First hidden layer: Detects edges, basic patterns
   - Second hidden layer: Combines features, detects shapes
   - Third hidden layer: High-level digit patterns
3. **Output Layer (10 neurons)**: One neuron for each digit (0-9)

## Number of Layers

- **2 layers** (input + output): Too simple, poor feature extraction
- **3 layers** (input + hidden + output): Good for simple tasks
- **4 layers** (input + 2 hidden + output): **[RECOMMENDED]** Best balance
- **5+ layers** (input + 3+ hidden + output): Can work but diminishing returns for MNIST

## Usage

### Training with Different Architectures:

```bash
# Simple architecture
./train_mnist simple 0.01 10

# Medium architecture (recommended)
./train_mnist medium 0.01 10

# Complex architecture
./train_mnist complex 0.01 10

# With real MNIST CSV file
./train_mnist medium 0.01 10 mnist_train.csv
```

### Downloading MNIST Data:

**Quick Start** - Use the download helper script:
```bash
make download-mnist
# or
./download_mnist.sh
```

This script will:
- Check if files already exist
- Use Kaggle CLI if installed (automatic download)
- Provide manual download instructions if needed

**Manual Download** - From Kaggle (CSV format, easiest):
1. Visit: https://www.kaggle.com/datasets/oddrationale/mnist-in-csv
2. Click 'Download' (requires free Kaggle account)
3. Extract the ZIP file
4. Place `mnist_train.csv` and `mnist_test.csv` in the project directory
5. Then use: `./train_mnist medium 0.01 10 mnist_train.csv`

2. **From Yann LeCun's website** (Original binary format):
   ```bash
   # Download from: http://yann.lecun.com/exdb/mnist/
   # Requires binary loader (more complex)
   ```

### Parameters:

```bash
./train_mnist [architecture] [learning_rate] [epochs] [mnist_file]
```

- **architecture**: `simple`, `medium`, or `complex` (default: medium)
- **learning_rate**: STDP learning rate (default: 0.01)
- **epochs**: Number of training epochs (default: 5)
- **mnist_file**: Path to MNIST CSV file (optional, uses synthetic if omitted)

## Recommended Settings

### For Quick Testing:
```bash
./train_mnist simple 0.01 5
```
- Architecture: Simple (784→300→10)
- Training time: ~5-10 minutes
- Expected accuracy: 60-70%

### For Best Results:
```bash
./train_mnist medium 0.01 20 mnist_train.csv
```
- Architecture: Medium (784→400→200→10)
- Training time: ~30-60 minutes
- Expected accuracy: 75-85% (with real MNIST)

### For Maximum Accuracy:
```bash
./train_mnist complex 0.01 30 mnist_train.csv
```
- Architecture: Complex (784→512→256→128→10)
- Training time: ~1-2 hours
- Expected accuracy: 80-90% (with real MNIST)

## Memory Requirements

- **Simple**: ~2-4 GB RAM
- **Medium**: ~4-8 GB RAM
- **Complex**: ~8-16 GB RAM

## Training Tips

1. **Start with Simple**: Test with simple architecture first
2. **Use Real MNIST**: Synthetic data is for testing only
3. **More Epochs**: Increase epochs for better accuracy (10-30 recommended)
4. **Learning Rate**: Lower (0.001-0.01) for stable training
5. **Batch Processing**: The code processes in batches for progress updates

## Expected Performance

| Architecture | Neurons | Connections | Training Time | Accuracy* |
|-------------|---------|-------------|---------------|-----------|
| Simple      | 1,094   | ~246K       | ~5-10 min     | 60-70%    |
| Medium      | 1,394   | ~415K       | ~30-60 min    | 75-85%    |
| Complex     | 1,690   | ~591K       | ~1-2 hours    | 80-90%    |

*Accuracy with real MNIST dataset and sufficient training

## Building

Add to Makefile:
```makefile
MNIST_TARGET = train_mnist
MNIST_SOURCES = train_mnist.cpp neuron.cpp network.cpp
MNIST_OBJECTS = $(MNIST_SOURCES:.cpp=.o)

$(MNIST_TARGET): train_mnist.o neuron.o network.o
	$(CXX) $(CXXFLAGS) -o $(MNIST_TARGET) train_mnist.o neuron.o network.o
```

Then:
```bash
make train_mnist
```


