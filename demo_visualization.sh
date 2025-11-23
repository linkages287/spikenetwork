#!/bin/bash
# Demo script for network visualization

echo "=== Spike Neural Network Visualization Demo ==="
echo ""

# Setup Python virtual environment
VENV_DIR="venv"
PYTHON_CMD="python3"

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating Python virtual environment..."
    $PYTHON_CMD -m venv $VENV_DIR
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create virtual environment"
        echo "Make sure python3-venv is installed:"
        echo "  macOS: python3 should include venv by default"
        echo "  Linux: sudo apt-get install python3-venv"
        exit 1
    fi
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source $VENV_DIR/bin/activate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment"
    exit 1
fi

# Check if dependencies are installed
echo "Checking Python dependencies..."
python -c "import matplotlib; import networkx; import numpy" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing required Python packages..."
    pip install --upgrade pip > /dev/null 2>&1
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies"
        deactivate
        exit 1
    fi
    echo "✓ Dependencies installed"
else
    echo "✓ Dependencies OK"
fi
echo ""

# Build export program
echo "Building export program..."
make export_network > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to build export_network"
    exit 1
fi
echo "✓ Build complete"
echo ""

# Export network state
echo "Exporting network state (5 steps)..."
./export_network demo_network.json 5 > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to export network state"
    exit 1
fi
echo "✓ Export complete"
echo ""

# Show available files
echo "Generated files:"
ls -1 demo_network_step*.json 2>/dev/null | head -5
echo ""

# Ask user which visualization mode
echo "Visualization options:"
echo "  1. Static view (single step)"
echo "  2. Dynamic time series (animated through all steps) [RECOMMENDED]"
echo "  3. View all steps individually"
read -p "Enter choice [2]: " viz_choice
viz_choice=${viz_choice:-2}

if [ "$viz_choice" = "1" ]; then
    echo "Which step would you like to visualize? (0-4)"
    read -p "Enter step number [0]: " choice
    choice=${choice:-0}
    
    file="demo_network_step${choice}.json"
    if [ -f "$file" ]; then
        echo "Opening static visualization for step $choice..."
        python visualize_network.py "$file"
    else
        echo "ERROR: File $file not found"
        deactivate
        exit 1
    fi
elif [ "$viz_choice" = "2" ]; then
    echo "Opening dynamic time series visualization..."
    echo "This will show connections activating as spikes propagate!"
    echo "Close the window to stop."
    python visualize_network.py demo_network_step0.json --time-series --interval 0.8
elif [ "$viz_choice" = "3" ]; then
    echo "Opening all visualizations sequentially..."
    for file in demo_network_step*.json; do
        if [ -f "$file" ]; then
            echo "Showing $file..."
            python visualize_network.py "$file"
        fi
    done
else
    echo "Invalid choice. Using dynamic time series..."
    python visualize_network.py demo_network_step0.json --time-series --interval 0.8
fi

# Deactivate virtual environment
deactivate

echo ""
echo "Demo complete!"

