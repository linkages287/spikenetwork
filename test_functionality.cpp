#include "network.h"
#include <iostream>
#include <cassert>
#include <cmath>

// Test helper function
bool approximately_equal(double a, double b, double epsilon = 0.001) {
    return std::abs(a - b) < epsilon;
}

void test_neuron_basic() {
    std::cout << "Test 1: Basic Neuron Functionality\n";
    
    Neuron neuron(1.0, 0.0, 0.9);
    
    // Test initial state
    assert(neuron.get_potential() == 0.0);
    assert(!neuron.spiked());
    assert(neuron.get_spike_count() == 0);
    assert(neuron.get_connection_count() == 0);
    
    // Test input application
    neuron.apply_input(0.5);
    assert(approximately_equal(neuron.get_potential(), 0.5));
    
    // Test decay
    neuron.update();
    assert(approximately_equal(neuron.get_potential(), 0.45)); // 0.5 * 0.9
    
    // Test spike threshold
    neuron.apply_input(0.6); // Total should be 0.45 + 0.6 = 1.05 > 1.0
    neuron.update();
    assert(neuron.spiked());
    assert(neuron.get_spike_count() == 1);
    assert(approximately_equal(neuron.get_potential(), 0.0)); // Reset after spike
    
    std::cout << "  ✓ Passed\n\n";
}

void test_neuron_connections() {
    std::cout << "Test 2: Neuron Connections\n";
    
    Neuron neuron1, neuron2, neuron3;
    
    // Test adding connections
    neuron1.add_connection(&neuron2, 0.3);
    neuron1.add_connection(&neuron3, 0.5);
    assert(neuron1.get_connection_count() == 2);
    
    // Test spike propagation
    neuron1.apply_input(1.5); // Force spike
    neuron1.update();
    
    // Check that connected neurons received spikes
    assert(approximately_equal(neuron2.get_potential(), 0.3));
    assert(approximately_equal(neuron3.get_potential(), 0.5));
    
    // Test removing connection
    neuron1.remove_connection(&neuron2);
    assert(neuron1.get_connection_count() == 1);
    
    // Reset and test again
    neuron2.reset();
    neuron3.reset();
    neuron1.apply_input(1.5);
    neuron1.update();
    
    // neuron2 should not receive spike, neuron3 should
    assert(approximately_equal(neuron2.get_potential(), 0.0));
    assert(approximately_equal(neuron3.get_potential(), 0.5));
    
    std::cout << "  ✓ Passed\n\n";
}

void test_network_basic() {
    std::cout << "Test 3: Network Basic Functionality\n";
    
    Network network(5);
    assert(network.size() == 5);
    
    // Test getting neurons
    Neuron* n0 = network.get_neuron(0);
    Neuron* n1 = network.get_neuron(1);
    assert(n0 != nullptr);
    assert(n1 != nullptr);
    assert(network.get_neuron(10) == nullptr); // Out of bounds
    
    // Test connections
    network.connect(0, 1, 0.4);
    network.connect(1, 2, 0.3);
    assert(n0->get_connection_count() == 1);
    assert(n1->get_connection_count() == 1);
    
    // Test invalid connections
    network.connect(0, 0, 0.5); // Self-connection (should be ignored)
    network.connect(0, 10, 0.5); // Out of bounds (should be ignored)
    assert(n0->get_connection_count() == 1);
    
    std::cout << "  ✓ Passed\n\n";
}

void test_network_propagation() {
    std::cout << "Test 4: Network Spike Propagation\n";
    
    Network network(3);
    
    // Create chain: 0 -> 1 -> 2
    network.connect(0, 1, 0.5);
    network.connect(1, 2, 0.5);
    
    // Apply input to neuron 0 to make it spike
    network.get_neuron(0)->apply_input(1.2);
    network.update();
    
    // Neuron 0 should have spiked
    assert(network.get_neuron(0)->spiked());
    assert(network.get_neuron(0)->get_spike_count() == 1);
    
    // Neuron 1 should have received spike and then decayed (0.5 * 0.9 = 0.45)
    // Note: In the same update cycle, neuron 1 receives the spike then decays
    assert(approximately_equal(network.get_neuron(1)->get_potential(), 0.45));
    
    // Neuron 2 should not have received spike yet (neuron 1 hasn't spiked)
    assert(approximately_equal(network.get_neuron(2)->get_potential(), 0.0));
    
    // Apply more input to neuron 1 to push it over threshold
    network.get_neuron(1)->apply_input(0.6); // 0.45 + 0.6 = 1.05 > 1.0
    
    // Update again - neuron 1 should spike now
    network.update();
    assert(network.get_neuron(1)->spiked());
    assert(approximately_equal(network.get_neuron(2)->get_potential(), 0.45)); // 0.5 * 0.9 after decay
    
    std::cout << "  ✓ Passed\n\n";
}

void test_sustained_input() {
    std::cout << "Test 5: Sustained Input Accumulation\n";
    
    Neuron neuron;
    
    // Apply small inputs multiple times
    for (int i = 0; i < 3; ++i) {
        neuron.apply_input(0.3);
        neuron.update();
    }
    
    // After 3 inputs of 0.3 with decay:
    // Step 1: 0.3 -> decay to 0.27
    // Step 2: 0.27 + 0.3 = 0.57 -> decay to 0.513
    // Step 3: 0.513 + 0.3 = 0.813 -> decay to 0.732
    assert(approximately_equal(neuron.get_potential(), 0.732, 0.01));
    assert(!neuron.spiked());
    
    // Apply one more input to push over threshold
    neuron.apply_input(0.3);
    neuron.update();
    // 0.732 + 0.3 = 1.032 > 1.0, should spike
    assert(neuron.spiked());
    assert(neuron.get_spike_count() == 1);
    
    std::cout << "  ✓ Passed\n\n";
}

int main() {
    std::cout << "=== Running Functionality Tests ===\n\n";
    
    try {
        test_neuron_basic();
        test_neuron_connections();
        test_network_basic();
        test_network_propagation();
        test_sustained_input();
        
        std::cout << "=== All Tests Passed! ===\n";
        return 0;
    } catch (const std::exception& e) {
        std::cerr << "Test failed with exception: " << e.what() << std::endl;
        return 1;
    } catch (...) {
        std::cerr << "Test failed with unknown exception" << std::endl;
        return 1;
    }
}

