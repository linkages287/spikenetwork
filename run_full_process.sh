#!/bin/bash

# Full Process Script for Spike Neural Network
# This script runs the complete workflow: build -> train -> simulate -> visualize

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
EPOCHS=${1:-5}
LEARNING_RATE=${2:-0.01}
TEST_DIGIT=${3:-0}
SIMULATION_STEPS=${4:-30}

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Spike Neural Network - Full Process${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Step 1: Clean and Build
echo -e "${YELLOW}[1/6] Cleaning and building project...${NC}"
make clean > /dev/null 2>&1
make
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Build successful${NC}"
else
    echo -e "${RED}❌ Build failed${NC}"
    exit 1
fi
echo ""

# Step 2: Setup Python environment (if needed)
echo -e "${YELLOW}[2/6] Checking Python environment...${NC}"
if [ ! -d "venv" ]; then
    echo "Setting up virtual environment..."
    make setup-venv
fi

if [ -d "venv" ]; then
    source venv/bin/activate
    echo -e "${GREEN}✅ Python environment ready${NC}"
else
    echo -e "${YELLOW}⚠️  Using system Python${NC}"
fi
echo ""

# Step 3: Train the network
echo -e "${YELLOW}[3/6] Training network for number recognition...${NC}"
echo "  Epochs: $EPOCHS"
echo "  Learning rate: $LEARNING_RATE"
echo ""
./train_numbers $EPOCHS $LEARNING_RATE
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Training completed${NC}"
    if [ -f "data/json/trained_network.json" ]; then
        echo "  Network saved to: data/json/trained_network.json"
    fi
else
    echo -e "${RED}❌ Training failed${NC}"
    exit 1
fi
echo ""

# Step 4: Simulate spiking process
echo -e "${YELLOW}[4/6] Simulating spiking process...${NC}"
echo "  Test digit: $TEST_DIGIT"
echo "  Simulation steps: $SIMULATION_STEPS"
echo ""
if [ -f "data/json/trained_network.json" ]; then
    ./simulate_spiking data/json/trained_network.json $TEST_DIGIT $SIMULATION_STEPS
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Simulation completed${NC}"
        echo "  Animation frames saved to: data/json/spike_animation_step*.json"
    else
        echo -e "${RED}❌ Simulation failed${NC}"
        exit 1
    fi
else
    echo -e "${YELLOW}⚠️  Trained network not found, creating test network...${NC}"
    ./export_network data/json/test_network.json 10
    ./simulate_spiking data/json/test_network.json $TEST_DIGIT $SIMULATION_STEPS
fi
echo ""

# Step 5: Generate visualizations
echo -e "${YELLOW}[5/6] Generating visualizations...${NC}"

# 5a: 3D Network Structure
if [ -f "data/json/trained_network.json" ]; then
    echo "  Creating 3D network structure visualization..."
    python visualize_3d.py data/json/trained_network.json --save network_3d_structure.png 2>/dev/null
    if [ -f "network_3d_structure.png" ]; then
        echo -e "  ${GREEN}✅ 3D structure saved: network_3d_structure.png${NC}"
    fi
fi

# 5b: Project Structure
echo "  Creating project structure diagram..."
python visualize_project_structure.py --save project_structure.png 2>/dev/null
if [ -f "project_structure.png" ]; then
    echo -e "  ${GREEN}✅ Project structure saved: project_structure.png${NC}"
fi

# 5c: Neuron Structure
echo "  Creating neuron structure diagram..."
python visualize_neuron_structure.py --save neuron_structure.png 2>/dev/null
if [ -f "neuron_structure.png" ]; then
    echo -e "  ${GREEN}✅ Neuron structure saved: neuron_structure.png${NC}"
fi

# 5d: Neuron Code Structure
echo "  Creating neuron code structure diagram..."
python visualize_neuron_code.py --save neuron_code_structure.png 2>/dev/null
if [ -f "neuron_code_structure.png" ]; then
    echo -e "  ${GREEN}✅ Code structure saved: neuron_code_structure.png${NC}"
fi

echo -e "${GREEN}✅ All visualizations generated${NC}"
echo ""

# Step 6: Summary
echo -e "${YELLOW}[6/6] Process Summary${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}✅ Build: Complete${NC}"
echo -e "${GREEN}✅ Training: Complete${NC}"
echo -e "${GREEN}✅ Simulation: Complete${NC}"
echo -e "${GREEN}✅ Visualizations: Complete${NC}"
echo ""
echo -e "${BLUE}Generated Files:${NC}"
echo "  📊 Network: data/json/trained_network.json"
echo "  🎬 Animation: data/json/spike_animation_step*.json"
echo "  📈 Visualizations: *.png"
echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo "  • View 3D animation: python animate_3d_spiking.py data/json/spike_animation_step0.json"
echo "  • View 2D animation: python visualize_network.py data/json/spike_animation_step0.json --time-series"
echo "  • Train with animation: make animate-training"
echo ""
echo -e "${GREEN}🎉 Full process completed successfully!${NC}"
echo -e "${BLUE}========================================${NC}"



