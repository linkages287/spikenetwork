#include "neuron.h"
#include <algorithm>

Neuron::Neuron(double threshold, double resting, double decay)
    : membrane_potential(resting), threshold(threshold), 
      resting_potential(resting), decay_factor(decay),
      has_spiked(false), spike_count(0) {
}

void Neuron::add_connection(Neuron* target, double weight) {
    // Check if connection already exists
    auto it = std::find_if(connections.begin(), connections.end(),
        [target](const Connection& conn) {
            return conn.target == target;
        });
    
    if (it == connections.end()) {
        connections.emplace_back(target, weight);
    } else {
        // Update weight if connection exists
        it->weight = weight;
    }
}

void Neuron::remove_connection(Neuron* target) {
    connections.erase(
        std::remove_if(connections.begin(), connections.end(),
            [target](const Connection& conn) {
                return conn.target == target;
            }),
        connections.end()
    );
}

void Neuron::update() {
    // Reset spike flag
    has_spiked = false;
    
    // Check if threshold is reached (before decay)
    if (membrane_potential >= threshold) {
        // Neuron spikes
        has_spiked = true;
        spike_count++;
        
        // Reset membrane potential after spike
        membrane_potential = resting_potential;
        
        // Send spikes to all connected neurons
        for (auto& conn : connections) {
            if (conn.target != nullptr) {
                conn.target->receive_spike(conn.weight);
            }
        }
    } else {
        // Decay membrane potential towards resting potential (only if no spike)
        membrane_potential = resting_potential + 
                            (membrane_potential - resting_potential) * decay_factor;
    }
}

void Neuron::receive_spike(double weight) {
    // Add weighted input to membrane potential
    membrane_potential += weight;
}

void Neuron::apply_input(double current) {
    // Add external current to membrane potential
    membrane_potential += current;
}

void Neuron::reset() {
    membrane_potential = resting_potential;
    has_spiked = false;
    spike_count = 0;
}

