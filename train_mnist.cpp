#include "network.h"
#include "load_mnist.cpp"
#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <random>
#include <cmath>
#include <algorithm>
#include <iomanip>
#include <sstream>

// MNIST Training Program for Spike Neural Network
// Recommended architectures:
// - Simple: 784 -> 300 -> 10
// - Medium: 784 -> 400 -> 200 -> 10
// - Complex: 784 -> 512 -> 256 -> 128 -> 10

struct NetworkArchitecture {
    int input_size;
    std::vector<int> hidden_sizes;
    int output_size;
    
    int total_neurons() const {
        int total = input_size + output_size;
        for (int h : hidden_sizes) {
            total += h;
        }
        return total;
    }
    
    std::string to_string() const {
        std::ostringstream oss;
        oss << input_size;
        for (int h : hidden_sizes) {
            oss << " -> " << h;
        }
        oss << " -> " << output_size;
        return oss.str();
    }
};

NetworkArchitecture create_simple_architecture() {
    NetworkArchitecture arch;
    arch.input_size = 784;  // 28x28 MNIST images
    arch.hidden_sizes = {300};
    arch.output_size = 10;  // 10 digits
    return arch;
}

NetworkArchitecture create_medium_architecture() {
    NetworkArchitecture arch;
    arch.input_size = 784;
    arch.hidden_sizes = {400, 200};
    arch.output_size = 10;
    return arch;
}

NetworkArchitecture create_complex_architecture() {
    NetworkArchitecture arch;
    arch.input_size = 784;
    arch.hidden_sizes = {512, 256, 128};
    arch.output_size = 10;
    return arch;
}

void build_network(Network& network, const NetworkArchitecture& arch, 
                   std::mt19937& gen, std::uniform_real_distribution<>& weight_dist) {
    // Connect input to first hidden layer
    for (int i = 0; i < arch.input_size; ++i) {
        for (int j = 0; j < arch.hidden_sizes[0]; ++j) {
            network.connect(i, arch.input_size + j, weight_dist(gen));
        }
    }
    
    // Connect hidden layers
    for (size_t layer = 0; layer < arch.hidden_sizes.size() - 1; ++layer) {
        // Calculate start and end indices for current layer
        int current_layer_start = arch.input_size;
        for (size_t i = 0; i < layer; ++i) {
            current_layer_start += arch.hidden_sizes[i];
        }
        int current_layer_end = current_layer_start + arch.hidden_sizes[layer];
        
        // Calculate start index for next layer
        int next_layer_start = arch.input_size;
        for (size_t i = 0; i <= layer; ++i) {
            next_layer_start += arch.hidden_sizes[i];
        }
        
        // Connect current layer to next layer
        for (int i = current_layer_start; i < current_layer_end; ++i) {
            for (int j = 0; j < arch.hidden_sizes[layer + 1]; ++j) {
                network.connect(i, next_layer_start + j, weight_dist(gen));
            }
        }
    }
    
    // Connect last hidden layer to output
    int last_hidden_start = arch.input_size;
    for (size_t i = 0; i < arch.hidden_sizes.size() - 1; ++i) {
        last_hidden_start += arch.hidden_sizes[i];
    }
    int last_hidden_end = last_hidden_start + arch.hidden_sizes.back();
    int output_start = arch.input_size;
    for (int h : arch.hidden_sizes) {
        output_start += h;
    }
    
    for (int i = last_hidden_start; i < last_hidden_end; ++i) {
        for (int j = 0; j < arch.output_size; ++j) {
            network.connect(i, output_start + j, weight_dist(gen));
        }
    }
}

int main(int argc, char* argv[]) {
    std::cout << "=== MNIST Spike Neural Network Training ===\n\n";
    
    // Parse arguments
    std::string architecture_type = "medium";  // simple, medium, complex
    double learning_rate = 0.01;
    int epochs = 5;
    std::string mnist_file = "";  // CSV file path, empty = use synthetic
    
    if (argc > 1) architecture_type = argv[1];
    if (argc > 2) learning_rate = std::stod(argv[2]);
    if (argc > 3) epochs = std::stoi(argv[3]);
    if (argc > 4) mnist_file = argv[4];
    
    // Select architecture
    NetworkArchitecture arch;
    if (architecture_type == "simple") {
        arch = create_simple_architecture();
    } else if (architecture_type == "complex") {
        arch = create_complex_architecture();
    } else {
        arch = create_medium_architecture();
    }
    
    std::cout << "Architecture: " << arch.to_string() << "\n";
    std::cout << "Total neurons: " << arch.total_neurons() << "\n";
    std::cout << "Layers: " << (2 + arch.hidden_sizes.size()) << "\n";
    std::cout << "  - Input: " << arch.input_size << " neurons\n";
    for (size_t i = 0; i < arch.hidden_sizes.size(); ++i) {
        std::cout << "  - Hidden " << (i+1) << ": " << arch.hidden_sizes[i] << " neurons\n";
    }
    std::cout << "  - Output: " << arch.output_size << " neurons\n\n";
    
    // Create network
    Network network(arch.total_neurons());
    
    std::cout << "Creating network connections...\n";
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> weight_dist(0.05, 0.15);  // Smaller weights for larger network
    
    build_network(network, arch, gen, weight_dist);
    
    // Calculate total connections
    int total_connections = 0;
    total_connections += arch.input_size * arch.hidden_sizes[0];
    for (size_t i = 0; i < arch.hidden_sizes.size() - 1; ++i) {
        total_connections += arch.hidden_sizes[i] * arch.hidden_sizes[i + 1];
    }
    total_connections += arch.hidden_sizes.back() * arch.output_size;
    
    std::cout << "Total connections: " << total_connections << "\n\n";
    
    // Load MNIST data
    std::cout << "Loading MNIST data...\n";
    std::vector<MNISTLoader::Sample> training_data;
    
    if (!mnist_file.empty()) {
        std::cout << "Loading from CSV: " << mnist_file << "\n";
        training_data = MNISTLoader::load_from_csv(mnist_file);
        
        if (training_data.empty()) {
            std::cout << "⚠️  Could not load CSV file. Falling back to synthetic MNIST-like data.\n";
            std::cout << "   To use real MNIST, download from:\n";
            std::cout << "   https://www.kaggle.com/datasets/oddrationale/mnist-in-csv\n";
            std::cout << "   And place mnist_train.csv in the project directory.\n";
            std::cout << "   Or run: ./download_mnist.sh\n\n";
            training_data = MNISTLoader::generate_synthetic_mnist(100);
        } else {
            std::cout << "✅ Successfully loaded " << training_data.size() << " samples from CSV\n\n";
        }
    } else {
        std::cout << "Using synthetic MNIST-like data (for testing)\n";
        std::cout << "To use real MNIST, download from:\n";
        std::cout << "  https://www.kaggle.com/datasets/oddrationale/mnist-in-csv\n";
        std::cout << "Then run: ./train_mnist medium 0.01 10 mnist_train.csv\n\n";
        training_data = MNISTLoader::generate_synthetic_mnist(100);
    }
    
    if (training_data.empty()) {
        std::cerr << "Error: No training data loaded\n";
        return 1;
    }
    
    std::cout << "Loaded " << training_data.size() << " training samples\n\n";
    
    // Training loop
    std::cout << "Starting training...\n";
    std::cout << "Epochs: " << epochs << ", Learning rate: " << learning_rate << "\n\n";
    
    for (int epoch = 0; epoch < epochs; ++epoch) {
        std::cout << "=== Epoch " << (epoch + 1) << "/" << epochs << " ===\n";
        std::shuffle(training_data.begin(), training_data.end(), gen);
        
        int correct = 0;
        double total_loss = 0.0;
        int processed = 0;
        
        // Process in batches to show progress
        int batch_size = std::min(100, (int)training_data.size());
        
        for (size_t sample_idx = 0; sample_idx < training_data.size(); ++sample_idx) {
            const auto& sample = training_data[sample_idx];
            network.reset();
            
            // Apply input (rate coding: pixel intensity -> input current)
            for (size_t i = 0; i < sample.data.size() && i < (size_t)arch.input_size; ++i) {
                // Convert pixel value (0-1) to input current (0-2)
                // Higher pixel intensity = stronger input
                double input_current = sample.data[i] * 2.0;
                network.get_neuron(i)->apply_input(input_current);
            }
            
            // Run simulation
            int simulation_steps = 30;  // More steps for larger network
            std::vector<int> output_spikes(arch.output_size, 0);
            
            for (int step = 0; step < simulation_steps; ++step) {
                network.update_with_learning(step, learning_rate);
                
                // Count spikes in output layer
                int output_start = arch.input_size;
                for (int h : arch.hidden_sizes) {
                    output_start += h;
                }
                
                for (int i = 0; i < arch.output_size; ++i) {
                    int neuron_idx = output_start + i;
                    if (network.get_neuron(neuron_idx)->spiked()) {
                        output_spikes[i]++;
                    }
                }
            }
            
            // Find prediction
            int predicted = 0;
            int max_spikes = output_spikes[0];
            for (int i = 1; i < arch.output_size; ++i) {
                if (output_spikes[i] > max_spikes) {
                    max_spikes = output_spikes[i];
                    predicted = i;
                }
            }
            
            if (predicted == sample.label) correct++;
            
            // Calculate loss
            double loss = 0.0;
            for (int i = 0; i < arch.output_size; ++i) {
                double target = (i == sample.label) ? 1.0 : 0.0;
                double actual = (double)output_spikes[i] / simulation_steps;
                loss += (target - actual) * (target - actual);
            }
            total_loss += loss;
            processed++;
            
            // Progress update
            if (processed % batch_size == 0) {
                double accuracy = (double)correct / processed * 100.0;
                std::cout << "  Processed: " << processed << "/" << training_data.size()
                          << " | Accuracy: " << std::fixed << std::setprecision(2)
                          << accuracy << "% (" << correct << "/" << processed << ")\n";
            }
        }
        
        double accuracy = (double)correct / training_data.size() * 100.0;
        double avg_loss = total_loss / training_data.size();
        
        std::cout << "\nEpoch " << (epoch + 1) << " Results:\n";
        std::cout << "  Accuracy: " << std::fixed << std::setprecision(2) 
                  << accuracy << "% (" << correct << "/" << training_data.size() << ")\n";
        std::cout << "  Average Loss: " << std::fixed << std::setprecision(4) 
                  << avg_loss << "\n\n";
    }
    
    // Save trained network
    std::cout << "Saving trained network...\n";
    system("mkdir -p data/json");
    std::ofstream out_file("data/json/mnist_trained_network.json");
    if (out_file.is_open()) {
        network.export_to_json(out_file);
        out_file.close();
        std::cout << "Network saved to data/json/mnist_trained_network.json\n";
    }
    
    std::cout << "\n=== Training Complete ===\n";
    return 0;
}

