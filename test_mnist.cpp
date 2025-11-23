#include "network.h"
#include "load_mnist.cpp"
#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>
#include <random>
#include <cmath>
#include <algorithm>
#include <iomanip>
#include <map>

// MNIST Test Program - Tests trained network on MNIST test data

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
    
    int get_output_start() const {
        int start = input_size;
        for (int h : hidden_sizes) {
            start += h;
        }
        return start;
    }
};

NetworkArchitecture create_simple_architecture() {
    NetworkArchitecture arch;
    arch.input_size = 784;
    arch.hidden_sizes = {300};
    arch.output_size = 10;
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

// Recreate network architecture (simplified - loads weights from JSON in future)
Network* recreate_network(const NetworkArchitecture& arch) {
    Network* network = new Network(arch.total_neurons());
    
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> weight_dist(0.1, 0.3);
    
    // Connect input to first hidden layer
    for (int i = 0; i < arch.input_size; ++i) {
        for (int j = 0; j < arch.hidden_sizes[0]; ++j) {
            network->connect(i, arch.input_size + j, weight_dist(gen));
        }
    }
    
    // Connect hidden layers
    for (size_t layer = 0; layer < arch.hidden_sizes.size() - 1; ++layer) {
        int current_layer_start = arch.input_size;
        for (size_t i = 0; i < layer; ++i) {
            current_layer_start += arch.hidden_sizes[i];
        }
        int current_layer_end = current_layer_start + arch.hidden_sizes[layer];
        int next_layer_start = arch.input_size;
        for (size_t i = 0; i <= layer; ++i) {
            next_layer_start += arch.hidden_sizes[i];
        }
        
        for (int i = current_layer_start; i < current_layer_end; ++i) {
            for (int j = 0; j < arch.hidden_sizes[layer + 1]; ++j) {
                network->connect(i, next_layer_start + j, weight_dist(gen));
            }
        }
    }
    
    // Connect last hidden layer to output
    int last_hidden_start = arch.input_size;
    for (size_t i = 0; i < arch.hidden_sizes.size() - 1; ++i) {
        last_hidden_start += arch.hidden_sizes[i];
    }
    int last_hidden_end = last_hidden_start + arch.hidden_sizes.back();
    int output_start = arch.get_output_start();
    
    for (int i = last_hidden_start; i < last_hidden_end; ++i) {
        for (int j = 0; j < arch.output_size; ++j) {
            network->connect(i, output_start + j, weight_dist(gen));
        }
    }
    
    return network;
}

int predict_digit(Network& network, const NetworkArchitecture& arch, 
                  const std::vector<double>& image, int simulation_steps = 30) {
    network.reset();
    
    // Apply input (rate coding)
    for (size_t i = 0; i < image.size() && i < (size_t)arch.input_size; ++i) {
        double input_current = image[i] * 2.0;
        network.get_neuron(i)->apply_input(input_current);
    }
    
    // Run simulation
    std::vector<int> output_spikes(arch.output_size, 0);
    int output_start = arch.get_output_start();
    
    for (int step = 0; step < simulation_steps; ++step) {
        network.update();
        
        // Count spikes in output layer
        for (int i = 0; i < arch.output_size; ++i) {
            int neuron_idx = output_start + i;
            if (network.get_neuron(neuron_idx)->spiked()) {
                output_spikes[i]++;
            }
        }
    }
    
    // Find prediction (neuron with most spikes)
    int predicted = 0;
    int max_spikes = output_spikes[0];
    for (int i = 1; i < arch.output_size; ++i) {
        if (output_spikes[i] > max_spikes) {
            max_spikes = output_spikes[i];
            predicted = i;
        }
    }
    
    return predicted;
}

int main(int argc, char* argv[]) {
    std::cout << "=== MNIST Network Testing ===\n\n";
    
    // Parse arguments
    std::string architecture_type = "medium";
    std::string test_file = "";
    int num_test_samples = 100;
    int simulation_steps = 30;
    std::string network_file = "data/json/mnist_trained_network.json";
    
    if (argc > 1) architecture_type = argv[1];  // simple, medium, complex
    if (argc > 2) test_file = argv[2];          // MNIST test CSV file
    if (argc > 3) num_test_samples = std::stoi(argv[3]);
    if (argc > 4) simulation_steps = std::stoi(argv[4]);
    
    // Select architecture
    NetworkArchitecture arch;
    if (architecture_type == "simple") {
        arch = create_simple_architecture();
    } else if (architecture_type == "complex") {
        arch = create_complex_architecture();
    } else {
        arch = create_medium_architecture();
    }
    
    std::cout << "Architecture: " << architecture_type << "\n";
    std::cout << "  Input: " << arch.input_size << " neurons\n";
    for (size_t i = 0; i < arch.hidden_sizes.size(); ++i) {
        std::cout << "  Hidden " << (i+1) << ": " << arch.hidden_sizes[i] << " neurons\n";
    }
    std::cout << "  Output: " << arch.output_size << " neurons\n";
    std::cout << "  Total: " << arch.total_neurons() << " neurons\n\n";
    
    // Load network from JSON file if it exists
    std::cout << "Loading network...\n";
    Network* network = nullptr;
    
    // Try to load from JSON file first
    std::ifstream check_file(network_file);
    if (check_file.good()) {
        check_file.close();
        std::cout << "Loading trained network from: " << network_file << "\n";
        network = Network::load_from_json(network_file);
        if (network) {
            std::cout << "✅ Successfully loaded network with " << network->size() << " neurons\n\n";
            
            // Verify architecture matches (check neuron count)
            int expected_neurons = arch.total_neurons();
            if ((int)network->size() != expected_neurons) {
                std::cerr << "⚠️  Warning: Loaded network has " << network->size() 
                          << " neurons, but architecture expects " << expected_neurons << "\n";
                std::cerr << "   Architecture may not match. Results may be incorrect.\n\n";
            }
        } else {
            std::cerr << "⚠️  Failed to load from JSON. Creating new network with random weights.\n";
            network = recreate_network(arch);
        }
    } else {
        std::cout << "Network file not found: " << network_file << "\n";
        std::cout << "Creating new network with random weights.\n";
        std::cout << "⚠️  Note: Train the network first with: ./train_mnist " 
                  << architecture_type << " <epochs> <learning_rate>\n\n";
        network = recreate_network(arch);
    }
    
    if (!network) {
        std::cerr << "Error: Failed to create network\n";
        return 1;
    }
    
    // Load test data
    std::cout << "Loading test data...\n";
    std::vector<MNISTLoader::Sample> test_data;
    
    if (!test_file.empty()) {
        std::cout << "Attempting to load from CSV: " << test_file << "\n";
        test_data = MNISTLoader::load_from_csv(test_file);
        
        if (test_data.empty()) {
            std::cout << "⚠️  Could not load CSV file. Falling back to synthetic MNIST-like data.\n";
            std::cout << "   To use real MNIST, download from:\n";
            std::cout << "   https://www.kaggle.com/datasets/oddrationale/mnist-in-csv\n";
            std::cout << "   And place mnist_test.csv in the project directory.\n\n";
            test_data = MNISTLoader::generate_synthetic_mnist(num_test_samples / 10);  // Adjust for requested samples
        } else {
            if (test_data.size() > (size_t)num_test_samples) {
                test_data.resize(num_test_samples);
            }
            std::cout << "✅ Successfully loaded " << test_data.size() << " samples from CSV\n\n";
        }
    } else {
        std::cout << "Using synthetic MNIST-like data (for testing)\n";
        std::cout << "To test with real MNIST, download test CSV from:\n";
        std::cout << "  https://www.kaggle.com/datasets/oddrationale/mnist-in-csv\n";
        std::cout << "Then run: ./test_mnist medium mnist_test.csv " << num_test_samples << "\n\n";
        test_data = MNISTLoader::generate_synthetic_mnist(num_test_samples / 10);  // Adjust for requested samples
    }
    
    if (test_data.empty()) {
        std::cerr << "Error: No test data loaded\n";
        return 1;
    }
    
    std::cout << "Loaded " << test_data.size() << " test samples\n\n";
    
    // Test the network
    std::cout << "Testing network...\n";
    std::cout << "Simulation steps per sample: " << simulation_steps << "\n\n";
    
    int correct = 0;
    int total = test_data.size();
    std::map<int, int> digit_correct;    // Correct predictions per digit
    std::map<int, int> digit_total;      // Total samples per digit
    std::map<int, std::map<int, int>> confusion_matrix;  // Confusion matrix
    
    // Test each sample
    std::cout << "\nDetailed Test Results:\n";
    std::cout << "Sample | Actual | Predicted | Result\n";
    std::cout << "-------|--------|-----------|--------\n";
    
    for (size_t i = 0; i < test_data.size(); ++i) {
        const auto& sample = test_data[i];
        int actual = sample.label;
        int predicted = predict_digit(*network, arch, sample.data, simulation_steps);
        
        digit_total[actual]++;
        bool is_correct = (predicted == actual);
        if (is_correct) {
            correct++;
            digit_correct[actual]++;
        }
        
        confusion_matrix[actual][predicted]++;
        
        // Show each test case
        std::cout << std::setw(6) << (i + 1) << " | "
                  << std::setw(6) << actual << " | "
                  << std::setw(9) << predicted << " | "
                  << (is_correct ? "✓ Correct" : "✗ Wrong") << "\n";
        
        // Show progress every 10 samples
        if ((i + 1) % 10 == 0 && (i + 1) < total) {
            double accuracy = (double)correct / (i + 1) * 100.0;
            std::cout << "-------|--------|-----------|--------\n";
            std::cout << "Progress: " << (i + 1) << "/" << total 
                      << " | Accuracy: " << std::fixed << std::setprecision(2) 
                      << accuracy << "% (" << correct << "/" << (i + 1) << ")\n\n";
            std::cout << "Sample | Actual | Predicted | Result\n";
            std::cout << "-------|--------|-----------|--------\n";
        }
    }
    
    std::cout << "\n";
    
    // Print results
    std::cout << "\n=== Test Results ===\n";
    std::cout << "Total test samples: " << total << "\n";
    std::cout << "Correct predictions: " << correct << "\n";
    std::cout << "Incorrect predictions: " << (total - correct) << "\n";
    
    double overall_accuracy = (double)correct / total * 100.0;
    std::cout << "\nOverall Accuracy: " << std::fixed << std::setprecision(2) 
              << overall_accuracy << "% (" << correct << "/" << total << ")\n\n";
    
    // Per-digit accuracy
    std::cout << "Per-Digit Accuracy:\n";
    std::cout << "Digit | Correct | Total | Accuracy\n";
    std::cout << "------|---------|-------|----------\n";
    for (int digit = 0; digit < 10; ++digit) {
        int correct_count = digit_correct[digit];
        int total_count = digit_total[digit];
        double accuracy = (total_count > 0) ? (double)correct_count / total_count * 100.0 : 0.0;
        
        std::cout << std::setw(5) << digit << " | "
                  << std::setw(7) << correct_count << " | "
                  << std::setw(5) << total_count << " | "
                  << std::fixed << std::setprecision(2) << accuracy << "%\n";
    }
    
    // Confusion matrix
    std::cout << "\nConfusion Matrix (rows=actual, cols=predicted):\n";
    std::cout << "      ";
    for (int i = 0; i < 10; ++i) {
        std::cout << std::setw(4) << i;
    }
    std::cout << "\n";
    std::cout << "------";
    for (int i = 0; i < 10; ++i) {
        std::cout << "----";
    }
    std::cout << "\n";
    
    for (int actual = 0; actual < 10; ++actual) {
        std::cout << std::setw(4) << actual << " |";
        for (int predicted = 0; predicted < 10; ++predicted) {
            int count = confusion_matrix[actual][predicted];
            if (actual == predicted && count > 0) {
                std::cout << std::setw(4) << "✓" << count;
            } else if (count > 0) {
                std::cout << std::setw(4) << count;
            } else {
                std::cout << std::setw(4) << ".";
            }
        }
        std::cout << "\n";
    }
    
    // Error analysis
    std::cout << "\nMost Common Errors:\n";
    std::vector<std::tuple<int, int, int>> errors;  // (actual, predicted, count)
    
    for (const auto& actual_pair : confusion_matrix) {
        int actual = actual_pair.first;
        for (const auto& pred_pair : actual_pair.second) {
            int predicted = pred_pair.first;
            int count = pred_pair.second;
            if (actual != predicted && count > 0) {
                errors.push_back(std::make_tuple(actual, predicted, count));
            }
        }
    }
    
    std::sort(errors.begin(), errors.end(), 
              [](const std::tuple<int, int, int>& a, const std::tuple<int, int, int>& b) {
                  return std::get<2>(a) > std::get<2>(b);
              });
    
    for (size_t i = 0; i < std::min((size_t)10, errors.size()); ++i) {
        int actual = std::get<0>(errors[i]);
        int predicted = std::get<1>(errors[i]);
        int count = std::get<2>(errors[i]);
        std::cout << "  " << actual << " → " << predicted << ": " << count << " times\n";
    }
    
    std::cout << "\n=== Testing Complete ===\n";
    
    delete network;
    return 0;
}

