#ifndef NETWORK_H
#define NETWORK_H

#include "neuron.h"
#include <vector>
#include <memory>

class Network {
private:
    std::vector<std::unique_ptr<Neuron>> neurons;

public:
    // Constructor: creates a network with specified number of neurons
    Network(size_t num_neurons);
    
    // Get neuron at index
    Neuron* get_neuron(size_t index);
    
    // Connect two neurons
    void connect(size_t from, size_t to, double weight);
    
    // Update all neurons in the network (one time step)
    void update();
    
    // Get number of neurons
    size_t size() const { return neurons.size(); }
    
    // Reset all neurons
    void reset();
    
    // Print network state
    void print_state() const;
    
    // Export network state to JSON (for visualization)
    void export_to_json(std::ostream& out) const;
};

#endif // NETWORK_H

