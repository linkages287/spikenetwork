#include "network.h"
#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>
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
    
    static std::vector<Sample> generate_synthetic_data(int /* samples_per_digit */ = 1) {
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

int main(int argc, char* argv[]) {
    std::cout << "=== Training with Animation - All Digits ===\n\n";
    
    int input_size = 49;
    int hidden_size = 50;
    int output_size = 10;
    int total_neurons = input_size + hidden_size + output_size;
    
    double learning_rate = 0.01;
    int epochs = 5;
    int samples_per_digit = 10;
    int export_interval = 5;  // Export every N samples
    
    if (argc > 1) epochs = std::stoi(argv[1]);
    if (argc > 2) learning_rate = std::stod(argv[2]);
    
    Network network(total_neurons);
    
    std::cout << "Creating network architecture...\n";
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> weight_dist(0.1, 0.3);
    
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
    
    std::cout << "Network created: " << input_size << " input + " 
              << hidden_size << " hidden + " << output_size << " output neurons\n\n";
    
    std::cout << "Loading training data...\n";
    std::vector<NumberDataLoader::Sample> training_data = 
        NumberDataLoader::generate_synthetic_data(samples_per_digit);
    std::cout << "Loaded " << training_data.size() << " training samples\n\n";
    
    std::cout << "Starting training with animation export...\n";
    std::cout << "Epochs: " << epochs << ", Learning rate: " << learning_rate << "\n";
    std::cout << "Exporting network state every " << export_interval << " samples\n\n";
    
    int frame_count = 0;
    int total_samples = 0;
    
    for (int epoch = 0; epoch < epochs; ++epoch) {
        std::cout << "=== Epoch " << (epoch + 1) << "/" << epochs << " ===\n";
        std::shuffle(training_data.begin(), training_data.end(), gen);
        
        int correct = 0;
        
        for (size_t sample_idx = 0; sample_idx < training_data.size(); ++sample_idx) {
            const auto& sample = training_data[sample_idx];
            network.reset();
            
            for (size_t i = 0; i < sample.data.size() && i < (size_t)input_size; ++i) {
                network.get_neuron(i)->apply_input(sample.data[i] * 2.0);
            }
            
            int simulation_steps = 15;
            std::vector<int> output_spikes(output_size, 0);
            
            // Run simulation and export at key steps
            for (int step = 0; step < simulation_steps; ++step) {
                network.update_with_learning(step, learning_rate);
                
                for (int i = 0; i < output_size; ++i) {
                    int neuron_idx = input_size + hidden_size + i;
                    if (network.get_neuron(neuron_idx)->spiked()) {
                        output_spikes[i]++;
                    }
                }
                
                // Export network state at certain steps during first few samples of each epoch
                if (sample_idx < 3 && (step == 0 || step == 5 || step == 10 || step == simulation_steps - 1)) {
                    system("mkdir -p data/json");
                    std::string filename = "data/json/training_epoch" + std::to_string(epoch) + 
                                         "_digit" + std::to_string(sample.label) + 
                                         "_step" + std::to_string(step) + ".json";
                    std::ofstream out(filename);
                    if (out) {
                        network.export_to_json(out);
                        out.close();
                        frame_count++;
                    }
                }
            }
            
            int predicted = 0;
            int max_spikes = output_spikes[0];
            for (int i = 1; i < output_size; ++i) {
                if (output_spikes[i] > max_spikes) {
                    max_spikes = output_spikes[i];
                    predicted = i;
                }
            }
            
            if (predicted == sample.label) correct++;
            total_samples++;
            
            // Export final state after each sample (for animation)
            if (total_samples % export_interval == 0) {
                system("mkdir -p data/json");
                std::string filename = "data/json/training_progress_sample" + std::to_string(total_samples) + ".json";
                std::ofstream out(filename);
                if (out) {
                    network.export_to_json(out);
                    out.close();
                }
            }
        }
        
        double accuracy = (double)correct / training_data.size() * 100.0;
        std::cout << "Epoch " << (epoch + 1) << " Accuracy: " << std::fixed << std::setprecision(2) 
                  << accuracy << "% (" << correct << "/" << training_data.size() << ")\n\n";
        
        // Test all digits and export
        std::cout << "Testing all digits after epoch " << (epoch + 1) << "...\n";
        std::vector<NumberDataLoader::Sample> test_digits = 
            NumberDataLoader::generate_synthetic_data(1);
        
        for (int digit = 0; digit < 10; ++digit) {
            network.reset();
            const auto& test_sample = test_digits[digit];
            
            for (size_t i = 0; i < test_sample.data.size() && i < (size_t)input_size; ++i) {
                network.get_neuron(i)->apply_input(test_sample.data[i] * 2.0);
            }
            
            int simulation_steps = 20;
            for (int step = 0; step < simulation_steps; ++step) {
                network.update();
                
                // Export at key steps
                if (step == 0 || step == 5 || step == 10 || step == 15 || step == simulation_steps - 1) {
                    system("mkdir -p data/json");
                    std::string filename = "data/json/training_epoch" + std::to_string(epoch) + 
                                         "_test_digit" + std::to_string(digit) + 
                                         "_step" + std::to_string(step) + ".json";
                    std::ofstream out(filename);
                    if (out) {
                        network.export_to_json(out);
                        out.close();
                        frame_count++;
                    }
                }
            }
        }
        std::cout << "Exported test frames for epoch " << (epoch + 1) << "\n\n";
    }
    
    std::cout << "Training complete!\n";
    std::cout << "Exported " << frame_count << " animation frames\n";
    std::cout << "\nTo view training animation:\n";
    std::cout << "  python animate_training.py data/json/training_epoch0_test_digit0_step0.json\n";
    
    return 0;
}

