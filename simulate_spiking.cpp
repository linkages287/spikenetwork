#include "network.h"
#include <iostream>
#include <fstream>
#include <vector>
#include <random>
#include <cmath>
#include <algorithm>
#include <iomanip>

// Number data loader (same as in train_numbers.cpp)
class NumberDataLoader {
public:
    struct Sample {
        std::vector<double> data;
        int label;
    };
    
    static std::vector<Sample> generate_synthetic_data(int samples_per_digit = 1) {
        std::vector<Sample> dataset;
        int grid_size = 7;
        int total_pixels = grid_size * grid_size;
        
        for (int digit = 0; digit < 10; ++digit) {
            Sample s;
            s.label = digit;
            s.data.resize(total_pixels, 0.0);
            create_digit_pattern(digit, s.data, grid_size, 0);
            dataset.push_back(s);
        }
        return dataset;
    }
    
private:
    static void create_digit_pattern(int digit, std::vector<double>& pattern, 
                                     int grid_size, int variation) {
        std::mt19937 gen(digit * 1000 + variation);
        std::uniform_real_distribution<> noise(-0.1, 0.1);
        
        switch (digit) {
            case 0: draw_circle(pattern, grid_size, 3, 3, 2.5, 1.0); break;
            case 1: draw_line(pattern, grid_size, 3, 1, 3, 5, 1.0); break;
            case 2:
                draw_line(pattern, grid_size, 1, 1, 5, 1, 1.0);
                draw_line(pattern, grid_size, 5, 1, 5, 3, 1.0);
                draw_line(pattern, grid_size, 5, 3, 1, 3, 1.0);
                draw_line(pattern, grid_size, 1, 3, 1, 5, 1.0);
                draw_line(pattern, grid_size, 1, 5, 5, 5, 1.0);
                break;
            case 3:
                draw_line(pattern, grid_size, 1, 1, 4, 1, 1.0);
                draw_line(pattern, grid_size, 1, 3, 4, 3, 1.0);
                draw_line(pattern, grid_size, 1, 5, 4, 5, 1.0);
                draw_line(pattern, grid_size, 5, 1, 5, 5, 1.0);
                break;
            case 4:
                draw_line(pattern, grid_size, 1, 1, 1, 3, 1.0);
                draw_line(pattern, grid_size, 1, 3, 5, 3, 1.0);
                draw_line(pattern, grid_size, 5, 1, 5, 5, 1.0);
                break;
            case 5:
                draw_line(pattern, grid_size, 5, 1, 1, 1, 1.0);
                draw_line(pattern, grid_size, 1, 1, 1, 3, 1.0);
                draw_line(pattern, grid_size, 1, 3, 5, 3, 1.0);
                draw_line(pattern, grid_size, 5, 3, 5, 5, 1.0);
                draw_line(pattern, grid_size, 5, 5, 1, 5, 1.0);
                break;
            case 6:
                draw_circle(pattern, grid_size, 3, 4, 2.0, 1.0);
                draw_line(pattern, grid_size, 1, 3, 1, 5, 1.0);
                break;
            case 7:
                draw_line(pattern, grid_size, 1, 1, 5, 1, 1.0);
                draw_line(pattern, grid_size, 5, 1, 3, 5, 1.0);
                break;
            case 8:
                draw_circle(pattern, grid_size, 3, 2, 1.5, 1.0);
                draw_circle(pattern, grid_size, 3, 5, 1.5, 1.0);
                break;
            case 9:
                draw_circle(pattern, grid_size, 3, 3, 2.0, 1.0);
                draw_line(pattern, grid_size, 5, 1, 5, 3, 1.0);
                break;
        }
        
        for (auto& p : pattern) {
            p += noise(gen);
            if (p < 0) p = 0;
            if (p > 1) p = 1;
        }
    }
    
    static void draw_line(std::vector<double>& pattern, int grid_size, 
                         int x1, int y1, int x2, int y2, double value) {
        int dx = abs(x2 - x1);
        int dy = abs(y2 - y1);
        int steps = std::max(dx, dy);
        
        for (int i = 0; i <= steps; ++i) {
            double t = (steps > 0) ? (double)i / steps : 0;
            int x = (int)(x1 + t * (x2 - x1));
            int y = (int)(y1 + t * (y2 - y1));
            
            if (x >= 0 && x < grid_size && y >= 0 && y < grid_size) {
                pattern[y * grid_size + x] = value;
            }
        }
    }
    
    static void draw_circle(std::vector<double>& pattern, int grid_size,
                           int cx, int cy, double radius, double value) {
        for (int y = 0; y < grid_size; ++y) {
            for (int x = 0; x < grid_size; ++x) {
                double dx = x - cx;
                double dy = y - cy;
                double dist = sqrt(dx*dx + dy*dy);
                if (fabs(dist - radius) < 0.5) {
                    pattern[y * grid_size + x] = value;
                }
            }
        }
    }
};

// Load network from JSON (simplified - we'll recreate it)
Network* recreate_network_from_json(const std::string& filename) {
    // For now, we'll create a new network with the same architecture
    // In a full implementation, you'd parse the JSON to restore exact weights
    int input_size = 49;
    int hidden_size = 50;
    int output_size = 10;
    int total_neurons = input_size + hidden_size + output_size;
    
    Network* network = new Network(total_neurons);
    
    // Recreate connections (with random weights for demo)
    // In production, you'd load actual weights from JSON
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> weight_dist(0.1, 0.5);
    
    for (int i = 0; i < input_size; ++i) {
        for (int j = 0; j < hidden_size; ++j) {
            network->connect(i, input_size + j, weight_dist(gen));
        }
    }
    
    for (int i = 0; i < hidden_size; ++i) {
        for (int j = 0; j < output_size; ++j) {
            network->connect(input_size + i, input_size + hidden_size + j, weight_dist(gen));
        }
    }
    
    return network;
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <trained_network.json> [digit] [num_steps]\n";
        std::cerr << "  trained_network.json: Trained network file\n";
        std::cerr << "  digit: Digit to test (0-9, default: 0)\n";
        std::cerr << "  num_steps: Number of simulation steps (default: 30)\n";
        return 1;
    }
    
    std::string network_file = argv[1];
    int test_digit = 0;
    int num_steps = 30;
    
    if (argc >= 3) {
        test_digit = std::stoi(argv[2]);
        if (test_digit < 0 || test_digit > 9) {
            std::cerr << "Error: Digit must be between 0 and 9\n";
            return 1;
        }
    }
    
    if (argc >= 4) {
        num_steps = std::stoi(argv[3]);
    }
    
    std::cout << "=== Simulating Spike Network with Digit " << test_digit << " ===\n\n";
    
    // Create network (same architecture as training)
    int input_size = 49;
    int hidden_size = 50;
    int output_size = 10;
    int total_neurons = input_size + hidden_size + output_size;
    
    Network network(total_neurons);
    
    // Recreate connections (simplified - in production load from JSON)
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> weight_dist(0.2, 0.4);
    
    for (int i = 0; i < input_size; ++i) {
        for (int j = 0; j < hidden_size; ++j) {
            network.connect(i, input_size + j, weight_dist(gen));
        }
    }
    
    for (int i = 0; i < hidden_size; ++i) {
        for (int j = 0; j < output_size; ++j) {
            network.connect(input_size + i, input_size + hidden_size + j, weight_dist(gen));
        }
    }
    
    // Load test digit
    std::vector<NumberDataLoader::Sample> test_data = 
        NumberDataLoader::generate_synthetic_data(1);
    NumberDataLoader::Sample test_sample = test_data[test_digit];
    
    std::cout << "Applying input pattern for digit " << test_digit << "...\n";
    network.reset();
    
    // Apply input pattern
    for (size_t i = 0; i < test_sample.data.size() && i < (size_t)input_size; ++i) {
        double input_current = test_sample.data[i] * 2.0;
        network.get_neuron(i)->apply_input(input_current);
    }
    
    std::cout << "Running simulation for " << num_steps << " steps...\n";
    std::cout << "Exporting network state at each step...\n\n";
    
    // Run simulation and export at each step
    std::string base_filename = "spike_animation";
    
    for (int step = 0; step < num_steps; ++step) {
        // Update network
        network.update();
        
        // Export to JSON
        std::string step_file = base_filename + "_step" + std::to_string(step) + ".json";
        std::ofstream out(step_file);
        if (!out) {
            std::cerr << "Error: Cannot open file " << step_file << " for writing\n";
            return 1;
        }
        
        network.export_to_json(out);
        out.close();
        
        if ((step + 1) % 5 == 0) {
            std::cout << "  Exported step " << step << "\n";
        }
    }
    
    std::cout << "\nSimulation complete!\n";
    std::cout << "Created " << num_steps << " time step files: " 
              << base_filename << "_step0.json to " 
              << base_filename << "_step" << (num_steps-1) << ".json\n\n";
    std::cout << "To visualize the animation:\n";
    std::cout << "  python visualize_network.py " << base_filename << "_step0.json --time-series\n";
    std::cout << "Or for 3D animation:\n";
    std::cout << "  python animate_3d_spiking.py " << base_filename << "_step0.json\n";
    
    return 0;
}

