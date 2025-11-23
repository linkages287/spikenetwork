#include "network.h"
#include <iostream>
#include <random>

int main() {
    std::cout << "=== Spike Neural Network Test ===\n\n";
    
    // Create a network with 10 neurons
    Network network(10);
    
    // Create random connections between neurons
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> neuron_dist(0, 9);
    std::uniform_real_distribution<> weight_dist(0.1, 0.5);
    
    std::cout << "Creating random connections...\n";
    // Create 15 random connections
    for (int i = 0; i < 15; ++i) {
        int from = neuron_dist(gen);
        int to = neuron_dist(gen);
        double weight = weight_dist(gen);
        
        if (from != to) {
            network.connect(from, to, weight);
            std::cout << "Connected neuron " << from << " -> " << to 
                      << " (weight: " << weight << ")\n";
        }
    }
    
    // Create a simple feed-forward structure as well
    std::cout << "\nAdding feed-forward connections...\n";
    for (int i = 0; i < 9; ++i) {
        network.connect(i, i + 1, 0.3);
        std::cout << "Connected neuron " << i << " -> " << (i + 1) << "\n";
    }
    
    // Test 1: Apply input to first neuron and observe propagation
    std::cout << "\n=== Test 1: Single Input Spike ===\n";
    network.reset();
    
    // Apply strong input to neuron 0
    network.get_neuron(0)->apply_input(1.5);
    std::cout << "Applied input (1.5) to neuron 0\n";
    
    // Run simulation for 10 time steps
    for (int step = 0; step < 10; ++step) {
        std::cout << "\n--- Time Step " << step << " ---\n";
        network.update();
        network.print_state();
    }
    
    // Test 2: Multiple inputs
    std::cout << "\n=== Test 2: Multiple Input Spikes ===\n";
    network.reset();
    
    // Apply inputs to multiple neurons
    network.get_neuron(0)->apply_input(1.2);
    network.get_neuron(2)->apply_input(1.0);
    network.get_neuron(5)->apply_input(1.3);
    
    std::cout << "Applied inputs to neurons 0, 2, and 5\n";
    
    // Run simulation for 8 time steps
    for (int step = 0; step < 8; ++step) {
        std::cout << "\n--- Time Step " << step << " ---\n";
        network.update();
        network.print_state();
    }
    
    // Test 3: Sustained input
    std::cout << "\n=== Test 3: Sustained Input ===\n";
    network.reset();
    
    // Apply sustained input to neuron 0 for 5 time steps
    for (int step = 0; step < 5; ++step) {
        network.get_neuron(0)->apply_input(0.3);  // Small input each step
        std::cout << "\n--- Time Step " << step << " (applied 0.3 to neuron 0) ---\n";
        network.update();
        network.print_state();
    }
    
    // Continue without input for 5 more steps
    for (int step = 5; step < 10; ++step) {
        std::cout << "\n--- Time Step " << step << " (no input) ---\n";
        network.update();
        network.print_state();
    }
    
    std::cout << "\n=== Test Complete ===\n";
    
    return 0;
}

