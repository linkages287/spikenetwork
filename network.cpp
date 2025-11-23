#include "network.h"
#include <iostream>
#include <iomanip>
#include <sstream>
#include <map>

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

