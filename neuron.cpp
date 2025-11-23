#include "neuron.h"
#include <algorithm>

Neuron::Neuron(double threshold, double resting, double decay)
    : membrane_potential(resting), threshold(threshold), 
      resting_potential(resting), decay_factor(decay),
      has_spiked(false), spike_count(0), last_spike_time(-1) {
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
        // Note: last_spike_time will be set by set_time_step() after update
        
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

void Neuron::set_time_step(int time_step) {
    if (has_spiked) {
        last_spike_time = time_step;
        spike_history.push_back(time_step);
        // Keep only recent spike history (last 100 spikes)
        if (spike_history.size() > 100) {
            spike_history.erase(spike_history.begin());
        }
    }
}

void Neuron::update_stdp(int current_time, double learning_rate, double tau_plus, double tau_minus) {
    // STDP: Spike-Timing Dependent Plasticity
    // If pre-synaptic neuron spikes before post-synaptic: strengthen (LTP)
    // If post-synaptic neuron spikes before pre-synaptic: weaken (LTD)
    
    if (last_spike_time < 0) return; // No spike history
    
    for (auto& conn : connections) {
        if (conn.target == nullptr) continue;
        
        int post_spike_time = conn.target->get_last_spike_time();
        if (post_spike_time < 0) continue; // Post-synaptic neuron hasn't spiked
        
        int dt = post_spike_time - last_spike_time; // Time difference
        
        if (dt > 0) {
            // Pre before post: Long-Term Potentiation (LTP)
            double weight_change = learning_rate * exp(-dt / tau_plus);
            conn.weight += weight_change;
            // Clamp weight
            if (conn.weight > 1.0) conn.weight = 1.0;
        } else if (dt < 0) {
            // Post before pre: Long-Term Depression (LTD)
            double weight_change = -learning_rate * exp(dt / tau_minus);
            conn.weight += weight_change;
            // Clamp weight
            if (conn.weight < 0.0) conn.weight = 0.0;
        }
    }
}

void Neuron::reset() {
    membrane_potential = resting_potential;
    has_spiked = false;
    spike_count = 0;
    last_spike_time = -1;
    spike_history.clear();
}

