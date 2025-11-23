#!/bin/bash

# MNIST Dataset Download Helper
# This script helps you download MNIST CSV files for training and testing

set -e

# Set Kaggle API token for authentication
export KAGGLE_API_TOKEN=KGAT_3ef64894270b711c9f430ec1de453277

echo "=== MNIST Dataset Download Helper ==="
echo ""

# Check if files already exist
if [ -f "mnist_train.csv" ] && [ -f "mnist_test.csv" ]; then
    echo "✅ MNIST files already exist:"
    ls -lh mnist_train.csv mnist_test.csv
    echo ""
    echo "You can now run:"
    echo "  ./train_mnist medium 0.01 10 mnist_train.csv"
    echo "  ./test_mnist medium mnist_test.csv"
    exit 0
fi

# Check for Kaggle CLI
if command -v kaggle &> /dev/null; then
    echo "📦 Kaggle CLI detected!"
    echo ""
    echo "Downloading MNIST dataset from Kaggle..."
    echo ""
    
    # Check if authenticated
    if ! kaggle datasets list &> /dev/null; then
        echo "⚠️  Kaggle CLI not authenticated."
        echo "   Please set up your API credentials:"
        echo "   1. Go to https://www.kaggle.com/account"
        echo "   2. Create API token"
        echo "   3. Place kaggle.json in ~/.kaggle/"
        echo ""
        echo "   Or download manually from:"
        echo "   https://www.kaggle.com/datasets/oddrationale/mnist-in-csv"
        exit 1
    fi
    
    echo "Downloading MNIST CSV files..."
    kaggle datasets download -d oddrationale/mnist-in-csv
    
    if [ -f "mnist-in-csv.zip" ]; then
        echo "Extracting files..."
        unzip -q mnist-in-csv.zip
        rm mnist-in-csv.zip
        echo "✅ Download complete!"
        ls -lh mnist_*.csv
    else
        echo "❌ Download failed"
        exit 1
    fi
    
else
    echo "📥 Manual Download Required"
    echo ""
    echo "Kaggle CLI not found. Please download manually:"
    echo ""
    echo "1. Visit: https://www.kaggle.com/datasets/oddrationale/mnist-in-csv"
    echo "2. Click 'Download' (requires Kaggle account - it's free)"
    echo "3. Extract the ZIP file"
    echo "4. Place the following files in this directory:"
    echo "   - mnist_train.csv"
    echo "   - mnist_test.csv"
    echo ""
    echo "Alternative: Install Kaggle CLI for automatic download:"
    echo "  pip install kaggle"
    echo "  # Then follow setup instructions at kaggle.com/account"
    echo ""
    
    # Check if we can use curl/wget to download (if public link exists)
    echo "Checking for alternative download methods..."
    
    # Note: Kaggle requires authentication, so direct download won't work
    echo "⚠️  Direct download not available (requires Kaggle authentication)"
    echo ""
    echo "Once files are downloaded, you can verify with:"
    echo "  ls -lh mnist_train.csv mnist_test.csv"
    echo ""
    echo "Expected file sizes:"
    echo "  mnist_train.csv: ~104 MB"
    echo "  mnist_test.csv: ~17 MB"
fi

echo ""
echo "After downloading, you can:"
echo "  ./train_mnist medium 0.01 10 mnist_train.csv"
echo "  ./test_mnist medium mnist_test.csv 10000 30"

