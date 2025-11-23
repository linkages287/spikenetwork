# MNIST Network Testing Guide

This guide explains how to test your trained MNIST spike neural network.

## Overview

The `test_mnist` program evaluates a trained network on MNIST test data, providing:
- Overall accuracy
- Per-digit accuracy
- Confusion matrix
- Error analysis

## Prerequisites

1. **Train the network first**:
   ```bash
   ./train_mnist medium 0.01 5
   ```
   This creates `data/json/mnist_trained_network.json` with the trained weights.

2. **Download MNIST test data** (optional, but recommended):
   - Download from: https://www.kaggle.com/datasets/oddrationale/mnist-in-csv
   - Extract `mnist_test.csv`
   - Place it in your project directory

## Usage

### Basic Syntax
```bash
./test_mnist [architecture] [test_file] [num_samples] [simulation_steps]
```

### Parameters

- **architecture**: Network architecture type
  - `simple`: 784 → 300 → 10
  - `medium`: 784 → 400 → 200 → 10 (recommended)
  - `complex`: 784 → 512 → 256 → 128 → 10

- **test_file**: Path to MNIST test CSV file (optional)
  - If not provided, uses synthetic MNIST-like data
  - Format: `label,pixel1,pixel2,...,pixel784`
  - Each pixel value: 0.0 to 1.0

- **num_samples**: Number of test samples to evaluate (default: 100)
  - For full test set, use 10000
  - Use smaller numbers for quick testing

- **simulation_steps**: Number of simulation time steps per sample (default: 30)
  - More steps = more accurate but slower
  - Recommended: 30-50 for testing

## Examples

### 1. Quick Test with Synthetic Data
```bash
./test_mnist medium
```
- Uses 100 synthetic samples
- 30 simulation steps per sample
- Good for quick verification

### 2. Test with Real MNIST Data
```bash
./test_mnist medium mnist_test.csv
```
- Uses first 100 samples from real MNIST
- Loads trained weights from `data/json/mnist_trained_network.json`

### 3. Full Test Set Evaluation
```bash
./test_mnist medium mnist_test.csv 10000 50
```
- Tests all 10,000 MNIST test samples
- 50 simulation steps per sample
- Provides comprehensive accuracy metrics

### 4. Custom Architecture Testing
```bash
./test_mnist complex mnist_test.csv 500 40
```
- Tests complex architecture
- 500 samples, 40 steps each

## Output

The program provides detailed test results:

### 1. Network Information
```
Architecture: medium
  Input: 784 neurons
  Hidden 1: 400 neurons
  Hidden 2: 200 neurons
  Output: 10 neurons
  Total: 1394 neurons
```

### 2. Loading Status
- ✅ Shows if trained network was loaded successfully
- ⚠️ Warns if file not found (uses random weights)
- ⚠️ Warns if architecture doesn't match loaded network

### 3. Progress Updates
```
  Tested: 10/100 | Accuracy: 80.00% (8/10)
  Tested: 20/100 | Accuracy: 75.00% (15/20)
  ...
```

### 4. Test Results
```
=== Test Results ===
Total test samples: 100
Correct predictions: 82
Incorrect predictions: 18

Overall Accuracy: 82.00% (82/100)
```

### 5. Per-Digit Accuracy
```
Per-Digit Accuracy:
Digit | Correct | Total | Accuracy
------|---------|-------|----------
    0 |       8 |    10 | 80.00%
    1 |      10 |    10 | 100.00%
    ...
```

### 6. Confusion Matrix
Shows actual vs predicted labels:
```
Confusion Matrix (rows=actual, cols=predicted):
      0   1   2   3   4   5   6   7   8   9
------|----|----|----|----|----|----|----|----|----|----
   0 | ✓8   0   1   0   0   1   0   0   0   0
   1 |   0 ✓10   0   0   0   0   0   0   0   0
   ...
```

### 7. Error Analysis
Lists most common misclassifications:
```
Most Common Errors:
  2 → 3: 5 times
  5 → 6: 3 times
  ...
```

## Workflow

### Complete Training and Testing Workflow

1. **Train the network**:
   ```bash
   make train-mnist
   # or
   ./train_mnist medium 0.01 10
   ```

2. **Test the trained network**:
   ```bash
   make test-mnist
   # or
   ./test_mnist medium mnist_test.csv 1000 30
   ```

3. **Analyze results**:
   - Check overall accuracy
   - Review per-digit performance
   - Examine confusion matrix for patterns
   - Identify common errors

## Troubleshooting

### Error: Network file not found
- **Solution**: Train the network first with `./train_mnist`
- The trained network must be saved to `data/json/mnist_trained_network.json`

### Warning: Architecture mismatch
- **Cause**: Loaded network has different number of neurons than specified architecture
- **Solution**: Use the same architecture type that was used for training
- Example: If trained with `medium`, test with `medium`

### Low accuracy with random weights
- **Normal**: If no trained network is loaded, random weights give ~10% accuracy (random guessing)
- **Solution**: Ensure you've trained the network first

### Slow testing
- **Cause**: Testing many samples with many steps
- **Solutions**:
  - Reduce `num_samples` for quick tests
  - Reduce `simulation_steps` (though this may reduce accuracy)
  - Use smaller architecture (`simple` instead of `complex`)

## Tips

1. **Start small**: Test with 10-100 samples first to verify everything works
2. **Match architecture**: Always use the same architecture for training and testing
3. **Use real data**: Synthetic data gives optimistic results; use real MNIST for accurate evaluation
4. **Interpret confusion matrix**: Look for patterns (e.g., 3 vs 5, 6 vs 8 confusion)
5. **Adjust steps**: If accuracy seems low, try increasing simulation steps

## Makefile Targets

```bash
# Build test program
make test_mnist

# Quick test (synthetic data, 100 samples)
make test-mnist

# Clean build files
make clean
```

## Expected Results

After training:
- **Simple architecture**: 60-70% accuracy
- **Medium architecture**: 75-85% accuracy (recommended)
- **Complex architecture**: 80-90% accuracy (slower training)

Note: Actual results depend on:
- Number of training epochs
- Learning rate
- Network initialization
- Training data quality

## Next Steps

After testing:
1. If accuracy is low: train for more epochs or adjust learning rate
2. If certain digits fail: check training data for those digits
3. If network is slow: consider using simpler architecture
4. For production: test on full 10,000 sample test set


