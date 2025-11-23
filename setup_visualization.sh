#!/bin/bash
# Setup script for visualization environment

echo "=== Setting up Visualization Environment ==="
echo ""

VENV_DIR="venv"
PYTHON_CMD="python3"

# Check if Python 3 is available
if ! command -v $PYTHON_CMD &> /dev/null; then
    echo "ERROR: python3 not found. Please install Python 3."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating Python virtual environment..."
    $PYTHON_CMD -m venv $VENV_DIR
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create virtual environment"
        echo ""
        echo "Troubleshooting:"
        echo "  macOS: python3 should include venv by default"
        echo "  Linux: sudo apt-get install python3-venv"
        echo "  Windows: python -m venv venv"
        exit 1
    fi
    echo "✓ Virtual environment created in $VENV_DIR/"
else
    echo "✓ Virtual environment already exists in $VENV_DIR/"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source $VENV_DIR/bin/activate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment"
    exit 1
fi

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip --quiet

# Install dependencies
echo "Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies"
        deactivate
        exit 1
    fi
    echo "✓ Dependencies installed from requirements.txt"
else
    echo "Installing dependencies manually..."
    pip install matplotlib networkx numpy
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies"
        deactivate
        exit 1
    fi
    echo "✓ Dependencies installed"
fi

# Verify installation
echo ""
echo "Verifying installation..."
python -c "import matplotlib; import networkx; import numpy; print('✓ All modules imported successfully')" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "ERROR: Module verification failed"
    deactivate
    exit 1
fi

# Deactivate virtual environment
deactivate

echo ""
echo "=== Setup Complete ==="
echo ""
echo "To use the visualization:"
echo "  1. Activate the virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  2. Run the visualization:"
echo "     python visualize_network.py <json_file>"
echo ""
echo "  3. Or use the demo script:"
echo "     ./demo_visualization.sh"
echo ""
echo "To deactivate the virtual environment:"
echo "     deactivate"
echo ""

