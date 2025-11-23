#include "network.h"
#include <iostream>
#include <fstream>
#include <random>

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <output_json_file> [num_steps]\n";
        std::cerr << "  output_json_file: Path to JSON file to write\n";
        std::cerr << "  num_steps: Number of simulation steps (default: 10)\n";
        return 1;
    }
    
    std::string output_file = argv[1];
    int num_steps = 10;
    if (argc >= 3) {
        num_steps = std::atoi(argv[2]);
    }
    
    std::cout << "Creating network with 10 neurons...\n";
    Network network(10);
    
    // Create random connections
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> neuron_dist(0, 9);
    std::uniform_real_distribution<> weight_dist(0.1, 0.5);
    
    std::cout << "Creating connections...\n";
    // Create 15 random connections
    for (int i = 0; i < 15; ++i) {
        int from = neuron_dist(gen);
        int to = neuron_dist(gen);
        double weight = weight_dist(gen);
        
        if (from != to) {
            network.connect(from, to, weight);
        }
    }
    
    // Create feed-forward structure
    for (int i = 0; i < 9; ++i) {
        network.connect(i, i + 1, 0.3);
    }
    
    // Apply initial input
    network.get_neuron(0)->apply_input(1.2);
    network.get_neuron(2)->apply_input(0.8);
    
    std::cout << "Running simulation for " << num_steps << " steps...\n";
    
    // Run simulation and export at each step
    for (int step = 0; step < num_steps; ++step) {
        // Update network
        network.update();
        
        // Export to JSON
        std::string step_file = output_file;
        if (num_steps > 1) {
            // Add step number to filename
            size_t dot_pos = output_file.find_last_of('.');
            if (dot_pos != std::string::npos) {
                step_file = output_file.substr(0, dot_pos) + 
                           "_step" + std::to_string(step) + 
                           output_file.substr(dot_pos);
            } else {
                step_file = output_file + "_step" + std::to_string(step);
            }
        }
        
        std::ofstream out(step_file);
        if (!out) {
            std::cerr << "Error: Cannot open file " << step_file << " for writing\n";
            return 1;
        }
        
        network.export_to_json(out);
        out.close();
        
        std::cout << "Exported step " << step << " to " << step_file << "\n";
        
        // Apply some additional inputs during simulation
        if (step == 3) {
            network.get_neuron(5)->apply_input(1.0);
        }
    }
    
    std::cout << "\nSimulation complete. Use visualize_network.py to view:\n";
    std::cout << "  python visualize_network.py " << output_file << "\n";
    if (num_steps > 1) {
        std::cout << "Or view individual steps:\n";
        for (int step = 0; step < num_steps; ++step) {
            size_t dot_pos = output_file.find_last_of('.');
            std::string step_file = output_file.substr(0, dot_pos) + 
                                   "_step" + std::to_string(step) + 
                                   output_file.substr(dot_pos);
            std::cout << "  python visualize_network.py " << step_file << "\n";
        }
    }
    
    return 0;
}

