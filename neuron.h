#ifndef NEURON_H
#define NEURON_H

#include <vector>
#include <memory>
#include <functional>

class Neuron {
public:
    // Connection structure to hold link to another neuron and weight
    struct Connection {
        Neuron* target;
        double weight;
        
        Connection(Neuron* t, double w) : target(t), weight(w) {}
    };

private:
    double membrane_potential;      // Current membrane potential
    double threshold;                // Spike threshold
    double resting_potential;         // Resting membrane potential
    double decay_factor;             // Membrane potential decay
    std::vector<Connection> connections;  // Dynamic connections to other neurons
    bool has_spiked;                 // Whether neuron spiked in current time step
    int spike_count;                 // Total number of spikes

public:
    // Constructor
    Neuron(double threshold = 1.0, double resting = 0.0, double decay = 0.9);
    
    // Add a connection to another neuron
    void add_connection(Neuron* target, double weight);
    
    // Remove a connection to a specific neuron
    void remove_connection(Neuron* target);
    
    // Update neuron state (called each time step)
    void update();
    
    // Receive input spike from another neuron
    void receive_spike(double weight);
    
    // Apply external input current
    void apply_input(double current);
    
    // Check if neuron spiked
    bool spiked() const { return has_spiked; }
    
    // Get current membrane potential
    double get_potential() const { return membrane_potential; }
    
    // Get spike count
    int get_spike_count() const { return spike_count; }
    
    // Get number of connections
    size_t get_connection_count() const { return connections.size(); }
    
    // Get connections (for export/visualization)
    const std::vector<Connection>& get_connections() const { return connections; }
    
    // Reset neuron state
    void reset();
};

#endif // NEURON_H

