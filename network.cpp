#include "network.h"
#include <iostream>
#include <iomanip>
#include <sstream>
#include <map>
#include <fstream>
#include <algorithm>
#include <cctype>

Network::Network(size_t num_neurons) {
    neurons.reserve(num_neurons);
    for (size_t i = 0; i < num_neurons; ++i) {
        neurons.emplace_back(new Neuron());
    }
}

Neuron* Network::get_neuron(size_t index) {
    if (index < neurons.size()) {
        return neurons[index].get();
    }
    return nullptr;
}

void Network::connect(size_t from, size_t to, double weight) {
    if (from < neurons.size() && to < neurons.size() && from != to) {
        neurons[from]->add_connection(neurons[to].get(), weight);
    }
}

void Network::update() {
    // First, update all neurons
    for (auto& neuron : neurons) {
        neuron->update();
    }
}

void Network::update_with_learning(int time_step, double learning_rate) {
    // Update all neurons
    for (auto& neuron : neurons) {
        neuron->update();
    }
    
    // Set time step for spike tracking
    for (auto& neuron : neurons) {
        neuron->set_time_step(time_step);
    }
    
    // Apply STDP learning rule
    for (auto& neuron : neurons) {
        neuron->update_stdp(time_step, learning_rate);
    }
}

void Network::reset() {
    for (auto& neuron : neurons) {
        neuron->reset();
    }
}

void Network::print_state() const {
    std::cout << "\nNetwork State:\n";
    std::cout << "Neuron | Potential | Spiked | Spike Count | Connections\n";
    std::cout << "-------|-----------|--------|-------------|------------\n";
    
    for (size_t i = 0; i < neurons.size(); ++i) {
        std::cout << std::setw(6) << i << " | "
                  << std::setw(9) << std::fixed << std::setprecision(3) 
                  << neurons[i]->get_potential() << " | "
                  << std::setw(6) << (neurons[i]->spiked() ? "Yes" : "No") << " | "
                  << std::setw(11) << neurons[i]->get_spike_count() << " | "
                  << std::setw(11) << neurons[i]->get_connection_count() << "\n";
    }
    std::cout << std::endl;
}

void Network::export_to_json(std::ostream& out) const {
    // Create mapping from neuron pointer to index
    std::map<const Neuron*, size_t> neuron_to_index;
    for (size_t i = 0; i < neurons.size(); ++i) {
        neuron_to_index[neurons[i].get()] = i;
    }
    
    out << "{\n";
    out << "  \"neurons\": [\n";
    
    for (size_t i = 0; i < neurons.size(); ++i) {
        out << "    {\n";
        out << "      \"id\": " << i << ",\n";
        out << "      \"potential\": " << std::fixed << std::setprecision(4) 
            << neurons[i]->get_potential() << ",\n";
        out << "      \"spiked\": " << (neurons[i]->spiked() ? "true" : "false") << ",\n";
        out << "      \"spike_count\": " << neurons[i]->get_spike_count() << ",\n";
        out << "      \"connections\": [\n";
        
        const auto& connections = neurons[i]->get_connections();
        for (size_t j = 0; j < connections.size(); ++j) {
            auto it = neuron_to_index.find(connections[j].target);
            if (it != neuron_to_index.end()) {
                out << "        {\"target\": " << it->second 
                    << ", \"weight\": " << std::fixed << std::setprecision(4) 
                    << connections[j].weight << "}";
                if (j < connections.size() - 1) {
                    out << ",";
                }
                out << "\n";
            }
        }
        
        out << "      ]\n";
        out << "    }";
        if (i < neurons.size() - 1) {
            out << ",";
        }
        out << "\n";
    }
    
    out << "  ]\n";
    out << "}\n";
}

Network* Network::load_from_json(const std::string& filename) {
    std::ifstream file(filename);
    if (!file.is_open()) {
        std::cerr << "Error: Could not open file: " << filename << "\n";
        return nullptr;
    }
    
    // First pass: find maximum "id" value (neurons are 0-indexed, so count = max_id + 1)
    // Simple approach: look for all lines with "id": <number> and track the maximum
    int max_id = -1;
    std::string line;
    bool in_neurons_array = false;
    
    while (std::getline(file, line)) {
        // Check if we entered neurons array
        if (line.find("\"neurons\"") != std::string::npos) {
            in_neurons_array = true;
        }
        
        // Check if we exited neurons array (the closing ] after all neurons)
        // The neurons array closes with "  ]" on a line that doesn't contain "connections"
        if (in_neurons_array && line.find("  ]") == 0 && 
            line.find("\"connections\"") == std::string::npos &&
            line.length() <= 4) {
            // This is the closing bracket of the neurons array
            break;
        }
        
        // While in neurons array, find all "id" fields and track max
        // Look for pattern: "id": <number>
        if (in_neurons_array) {
            size_t id_pos = line.find("\"id\"");
            if (id_pos != std::string::npos) {
                // Find the colon after "id"
                size_t colon_pos = line.find(':', id_pos);
                if (colon_pos != std::string::npos) {
                    std::string id_str = line.substr(colon_pos + 1);
                    // Remove comma if present
                    size_t comma_pos = id_str.find(',');
                    if (comma_pos != std::string::npos) {
                        id_str = id_str.substr(0, comma_pos);
                    }
                    // Trim whitespace
                    id_str.erase(0, id_str.find_first_not_of(" \t"));
                    id_str.erase(id_str.find_last_not_of(" \t") + 1);
                    try {
                        int id = std::stoi(id_str);
                        if (id > max_id) max_id = id;
                    } catch (...) {
                        // Ignore parsing errors
                    }
                }
            }
        }
    }
    // Neuron count is max_id + 1 (ids are 0-indexed)
    int neuron_count = max_id + 1;
    
    if (neuron_count <= 0) {
        std::cerr << "Error: No neurons found in JSON file (max_id=" << max_id << ")\n";
        return nullptr;
    }
    
    // Create network with the correct number of neurons
    Network* network = new Network(neuron_count);
    
    // Second pass: read connections
    file.clear();
    file.seekg(0, std::ios::beg);
    
    int current_neuron = -1;
    bool in_connections = false;
    bool in_connection_obj = false;
    int target = -1;
    double weight = 0.0;
    
    while (std::getline(file, line)) {
        // Find neuron id
        size_t id_pos = line.find("\"id\"");
        if (id_pos != std::string::npos) {
            size_t colon_pos = line.find(':', id_pos);
            if (colon_pos != std::string::npos) {
                std::string id_str = line.substr(colon_pos + 1);
                // Remove comma if present
                size_t comma_pos = id_str.find(',');
                if (comma_pos != std::string::npos) {
                    id_str = id_str.substr(0, comma_pos);
                }
                // Trim whitespace
                id_str.erase(0, id_str.find_first_not_of(" \t"));
                id_str.erase(id_str.find_last_not_of(" \t") + 1);
                current_neuron = std::stoi(id_str);
            }
        }
        
        // Check if entering connections array
        if (line.find("\"connections\"") != std::string::npos && 
            line.find('[') != std::string::npos) {
            in_connections = true;
            continue;
        }
        
        // Check if exiting connections array
        if (in_connections && line.find(']') != std::string::npos && 
            line.find("\"connections\"") == std::string::npos) {
            in_connections = false;
            continue;
        }
        
        // Check if entering a connection object
        if (in_connections && line.find('{') != std::string::npos) {
            in_connection_obj = true;
            target = -1;
            weight = 0.0;
            continue;
        }
        
        // Check if exiting a connection object
        if (in_connection_obj && line.find('}') != std::string::npos) {
            if (current_neuron >= 0 && target >= 0) {
                network->connect(current_neuron, target, weight);
            }
            in_connection_obj = false;
            continue;
        }
        
        // Read target
        if (in_connection_obj) {
            size_t target_pos = line.find("\"target\"");
            if (target_pos != std::string::npos) {
                size_t colon_pos = line.find(':', target_pos);
                if (colon_pos != std::string::npos) {
                    std::string target_str = line.substr(colon_pos + 1);
                    size_t comma_pos = target_str.find(',');
                    if (comma_pos != std::string::npos) {
                        target_str = target_str.substr(0, comma_pos);
                    }
                    target_str.erase(0, target_str.find_first_not_of(" \t"));
                    target_str.erase(target_str.find_last_not_of(" \t") + 1);
                    target = std::stoi(target_str);
                }
            }
        }
        
        // Read weight
        if (in_connection_obj) {
            size_t weight_pos = line.find("\"weight\"");
            if (weight_pos != std::string::npos) {
                size_t colon_pos = line.find(':', weight_pos);
                if (colon_pos != std::string::npos) {
                    std::string weight_str = line.substr(colon_pos + 1);
                    size_t comma_pos = weight_str.find(',');
                    if (comma_pos != std::string::npos) {
                        weight_str = weight_str.substr(0, comma_pos);
                    }
                    size_t brace_pos = weight_str.find('}');
                    if (brace_pos != std::string::npos) {
                        weight_str = weight_str.substr(0, brace_pos);
                    }
                    weight_str.erase(0, weight_str.find_first_not_of(" \t"));
                    weight_str.erase(weight_str.find_last_not_of(" \t") + 1);
                    weight = std::stod(weight_str);
                }
            }
        }
    }
    
    file.close();
    return network;
}

