#!/usr/bin/env python3
"""
Visualize the code structure of neuron.cpp - methods, calls, and relationships
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Ellipse
import matplotlib.patches as patches

def create_code_structure_diagram():
    """Create a comprehensive code structure diagram"""
    fig = plt.figure(figsize=(18, 14))
    
    # Create main axes
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 16)
    ax.axis('off')
    
    # Title
    ax.text(10, 15.5, 'Neuron Class Code Structure', 
            ha='center', fontsize=22, fontweight='bold')
    ax.text(10, 14.8, 'neuron.cpp / neuron.h', 
            ha='center', fontsize=14, style='italic')
    
    # Class header box
    class_box = FancyBboxPatch((1, 12.5), 18, 1.5,
                               boxstyle="round,pad=0.2",
                               facecolor='lightblue', 
                               edgecolor='navy', linewidth=3)
    ax.add_patch(class_box)
    ax.text(10, 13.5, 'class Neuron', ha='center', va='center',
            fontsize=16, fontweight='bold')
    ax.text(10, 13, 'Public Methods | Private Members', ha='center', va='center',
            fontsize=11)
    
    # Private members section
    members_box = FancyBboxPatch((1, 9.5), 8, 2.5,
                                boxstyle="round,pad=0.15",
                                facecolor='lightyellow', 
                                edgecolor='orange', linewidth=2)
    ax.add_patch(members_box)
    ax.text(5, 11.5, 'Private Members', ha='center', va='center',
            fontsize=13, fontweight='bold')
    
    members = [
        'membrane_potential (double)',
        'threshold (double)',
        'resting_potential (double)',
        'decay_factor (double)',
        'connections (vector<Connection>)',
        'has_spiked (bool)',
        'spike_count (int)',
        'last_spike_time (int)',
        'spike_history (vector<int>)'
    ]
    
    y_pos = 11.2
    for member in members:
        ax.text(1.2, y_pos, f'• {member}', ha='left', va='top',
               fontsize=9, family='monospace')
        y_pos -= 0.25
    
    # Public methods section
    methods_box = FancyBboxPatch((10, 9.5), 9, 2.5,
                                boxstyle="round,pad=0.15",
                                facecolor='lightgreen', 
                                edgecolor='darkgreen', linewidth=2)
    ax.add_patch(methods_box)
    ax.text(14.5, 11.5, 'Public Methods', ha='center', va='center',
            fontsize=13, fontweight='bold')
    
    methods = [
        'Neuron() - Constructor',
        'add_connection()',
        'remove_connection()',
        'update()',
        'receive_spike()',
        'apply_input()',
        'spiked() - const',
        'get_potential() - const',
        'get_spike_count() - const',
        'get_connections() - const',
        'update_stdp()',
        'reset()',
        'set_time_step()'
    ]
    
    y_pos = 11.2
    for method in methods:
        ax.text(10.2, y_pos, f'• {method}', ha='left', va='top',
               fontsize=9, family='monospace')
        y_pos -= 0.25
    
    # Method call flow diagram
    ax.text(10, 8.8, 'Method Call Flow & Relationships', ha='center',
            fontsize=14, fontweight='bold')
    
    # Constructor
    constr_box = FancyBboxPatch((1, 6.5), 3.5, 1,
                               boxstyle="round,pad=0.1",
                               facecolor='lightcyan', 
                               edgecolor='blue', linewidth=2)
    ax.add_patch(constr_box)
    ax.text(2.75, 7, 'Neuron()', ha='center', va='center',
            fontsize=11, fontweight='bold')
    ax.text(2.75, 6.6, 'Initializes all\nmember variables', ha='center', va='center',
            fontsize=8)
    
    # Core update cycle
    update_box = FancyBboxPatch((6, 6.5), 3.5, 1,
                               boxstyle="round,pad=0.1",
                               facecolor='lightcoral', 
                               edgecolor='red', linewidth=2)
    ax.add_patch(update_box)
    ax.text(7.75, 7, 'update()', ha='center', va='center',
            fontsize=11, fontweight='bold')
    ax.text(7.75, 6.6, 'Main update loop', ha='center', va='center',
            fontsize=8)
    
    # Input methods
    apply_input_box = FancyBboxPatch((11, 7.2), 3.5, 0.8,
                                    boxstyle="round,pad=0.1",
                                    facecolor='lightyellow', 
                                    edgecolor='orange', linewidth=2)
    ax.add_patch(apply_input_box)
    ax.text(12.75, 7.6, 'apply_input()', ha='center', va='center',
            fontsize=10, fontweight='bold')
    
    receive_box = FancyBboxPatch((11, 6.2), 3.5, 0.8,
                                boxstyle="round,pad=0.1",
                                facecolor='lightyellow', 
                                edgecolor='orange', linewidth=2)
    ax.add_patch(receive_box)
    ax.text(12.75, 6.6, 'receive_spike()', ha='center', va='center',
            fontsize=10, fontweight='bold')
    
    # Learning methods
    stdp_box = FancyBboxPatch((16, 6.5), 3.5, 1,
                             boxstyle="round,pad=0.1",
                             facecolor='plum', 
                             edgecolor='purple', linewidth=2)
    ax.add_patch(stdp_box)
    ax.text(17.75, 7, 'update_stdp()', ha='center', va='center',
            fontsize=11, fontweight='bold')
    ax.text(17.75, 6.6, 'STDP learning', ha='center', va='center',
            fontsize=8)
    
    # Connection management
    add_conn_box = FancyBboxPatch((1, 4.5), 3.5, 0.8,
                                 boxstyle="round,pad=0.1",
                                 facecolor='lightgreen', 
                                 edgecolor='green', linewidth=2)
    ax.add_patch(add_conn_box)
    ax.text(2.75, 4.9, 'add_connection()', ha='center', va='center',
            fontsize=10, fontweight='bold')
    
    remove_conn_box = FancyBboxPatch((1, 3.5), 3.5, 0.8,
                                    boxstyle="round,pad=0.1",
                                    facecolor='lightgreen', 
                                    edgecolor='green', linewidth=2)
    ax.add_patch(remove_conn_box)
    ax.text(2.75, 3.9, 'remove_connection()', ha='center', va='center',
            fontsize=10, fontweight='bold')
    
    # Utility methods
    reset_box = FancyBboxPatch((6, 4.5), 3.5, 0.8,
                             boxstyle="round,pad=0.1",
                             facecolor='wheat', 
                             edgecolor='brown', linewidth=2)
    ax.add_patch(reset_box)
    ax.text(7.75, 4.9, 'reset()', ha='center', va='center',
            fontsize=10, fontweight='bold')
    
    set_time_box = FancyBboxPatch((6, 3.5), 3.5, 0.8,
                                 boxstyle="round,pad=0.1",
                                 facecolor='wheat', 
                                 edgecolor='brown', linewidth=2)
    ax.add_patch(set_time_box)
    ax.text(7.75, 3.9, 'set_time_step()', ha='center', va='center',
            fontsize=10, fontweight='bold')
    
    # Getter methods
    getters_box = FancyBboxPatch((11, 3.5), 8.5, 1.8,
                                boxstyle="round,pad=0.1",
                                facecolor='lavender', 
                                edgecolor='indigo', linewidth=2)
    ax.add_patch(getters_box)
    ax.text(15.25, 5, 'Getter Methods (const)', ha='center', va='center',
            fontsize=11, fontweight='bold')
    getters = [
        'spiked()', 'get_potential()', 'get_spike_count()',
        'get_connection_count()', 'get_connections()',
        'get_last_spike_time()', 'get_spike_history()'
    ]
    y_pos = 4.7
    for i, getter in enumerate(getters):
        x_pos = 11.5 + (i % 4) * 2
        if i >= 4:
            y_pos = 4.2
        ax.text(x_pos, y_pos, f'• {getter}', ha='left', va='top',
               fontsize=8, family='monospace')
        if i == 3:
            y_pos = 4.2
    
    # Arrows showing call relationships
    # Constructor -> Members
    arrow1 = FancyArrowPatch((2.75, 6.5), (5, 10),
                            arrowstyle='->', mutation_scale=15,
                            color='blue', linewidth=1.5, alpha=0.6)
    ax.add_patch(arrow1)
    ax.text(3.5, 8, 'initializes', ha='left', fontsize=8, style='italic')
    
    # apply_input -> update
    arrow2 = FancyArrowPatch((12.75, 7.2), (9.5, 7),
                             arrowstyle='->', mutation_scale=15,
                             color='orange', linewidth=1.5, alpha=0.6)
    ax.add_patch(arrow2)
    
    # receive_spike -> update
    arrow3 = FancyArrowPatch((12.75, 6.2), (9.5, 6.8),
                             arrowstyle='->', mutation_scale=15,
                             color='orange', linewidth=1.5, alpha=0.6)
    ax.add_patch(arrow3)
    
    # update -> receive_spike (calls on targets)
    arrow4 = FancyArrowPatch((9.5, 6.5), (12.75, 6.5),
                             arrowstyle='->', mutation_scale=15,
                             color='red', linewidth=2, alpha=0.7,
                             linestyle='--')
    ax.add_patch(arrow4)
    ax.text(11, 6.2, 'calls on\nconnected\nneurons', ha='center', fontsize=7, style='italic')
    
    # update -> set_time_step
    arrow5 = FancyArrowPatch((7.75, 6.5), (7.75, 4.5),
                             arrowstyle='->', mutation_scale=15,
                             color='red', linewidth=1.5, alpha=0.6)
    ax.add_patch(arrow5)
    
    # set_time_step -> update_stdp
    arrow6 = FancyArrowPatch((9.5, 4), (16, 6.8),
                             arrowstyle='->', mutation_scale=15,
                             color='purple', linewidth=1.5, alpha=0.6)
    ax.add_patch(arrow6)
    
    # update_stdp -> get_last_spike_time
    arrow7 = FancyArrowPatch((17.75, 6.5), (15.5, 4.5),
                             arrowstyle='->', mutation_scale=15,
                             color='purple', linewidth=1.5, alpha=0.6,
                             linestyle='--')
    ax.add_patch(arrow7)
    
    # External callers section
    external_box = FancyBboxPatch((1, 0.5), 18, 2.5,
                                 boxstyle="round,pad=0.15",
                                 facecolor='mistyrose', 
                                 edgecolor='darkred', linewidth=2)
    ax.add_patch(external_box)
    ax.text(10, 2.5, 'External Callers (from Network class and other code)', 
            ha='center', va='center', fontsize=12, fontweight='bold')
    
    callers = [
        'Network::connect() → add_connection()',
        'Network::update() → update()',
        'Network::update_with_learning() → update(), set_time_step(), update_stdp()',
        'Network::reset() → reset()',
        'Network::get_neuron() → returns Neuron*',
        'main.cpp / train_numbers.cpp → apply_input(), get_potential(), spiked()',
        'export_network.cpp → get_connections(), get_potential(), spiked(), get_spike_count()'
    ]
    
    y_pos = 2.1
    for caller in callers:
        ax.text(1.3, y_pos, f'• {caller}', ha='left', va='top',
               fontsize=9, family='monospace')
        y_pos -= 0.3
    
    # Add legend
    legend_elements = [
        mpatches.Patch(facecolor='lightcyan', edgecolor='blue', label='Constructor'),
        mpatches.Patch(facecolor='lightcoral', edgecolor='red', label='Core Update'),
        mpatches.Patch(facecolor='lightyellow', edgecolor='orange', label='Input Methods'),
        mpatches.Patch(facecolor='plum', edgecolor='purple', label='Learning'),
        mpatches.Patch(facecolor='lightgreen', edgecolor='green', label='Connection Mgmt'),
        mpatches.Patch(facecolor='wheat', edgecolor='brown', label='Utility'),
        mpatches.Patch(facecolor='lavender', edgecolor='indigo', label='Getters'),
    ]
    
    ax.legend(handles=legend_elements, loc='upper right', fontsize=8, 
             bbox_to_anchor=(0.98, 0.98))
    
    return fig

def create_method_call_flow():
    """Create a detailed method call flow diagram"""
    fig = plt.figure(figsize=(16, 12))
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    ax.text(7, 9.5, 'Neuron Method Call Flow', 
            ha='center', fontsize=18, fontweight='bold')
    
    # Main execution flow
    # Step 1: Initialization
    init_box = FancyBboxPatch((1, 7.5), 2.5, 1,
                              boxstyle="round,pad=0.1",
                              facecolor='lightcyan', 
                              edgecolor='blue', linewidth=2)
    ax.add_patch(init_box)
    ax.text(2.25, 8, '1. Neuron()', ha='center', va='center',
            fontsize=11, fontweight='bold')
    ax.text(2.25, 7.6, 'Constructor', ha='center', va='center',
            fontsize=9)
    
    # Step 2: Setup connections
    conn_box = FancyBboxPatch((4.5, 7.5), 2.5, 1,
                             boxstyle="round,pad=0.1",
                             facecolor='lightgreen', 
                             edgecolor='green', linewidth=2)
    ax.add_patch(conn_box)
    ax.text(5.75, 8, '2. add_connection()', ha='center', va='center',
            fontsize=11, fontweight='bold')
    ax.text(5.75, 7.6, 'Setup network', ha='center', va='center',
            fontsize=9)
    
    # Step 3: Apply input
    input_box = FancyBboxPatch((8, 7.5), 2.5, 1,
                               boxstyle="round,pad=0.1",
                               facecolor='lightyellow', 
                               edgecolor='orange', linewidth=2)
    ax.add_patch(input_box)
    ax.text(9.25, 8, '3. apply_input()', ha='center', va='center',
            fontsize=11, fontweight='bold')
    ax.text(9.25, 7.6, 'External input', ha='center', va='center',
            fontsize=9)
    
    # Step 4: Update cycle
    update_box = FancyBboxPatch((11.5, 7.5), 2.5, 1,
                               boxstyle="round,pad=0.1",
                               facecolor='lightcoral', 
                               edgecolor='red', linewidth=2)
    ax.add_patch(update_box)
    ax.text(12.75, 8, '4. update()', ha='center', va='center',
            fontsize=11, fontweight='bold')
    ax.text(12.75, 7.6, 'Main loop', ha='center', va='center',
            fontsize=9)
    
    # Update details
    update_detail_box = FancyBboxPatch((1, 4.5), 12, 2.5,
                                      boxstyle="round,pad=0.15",
                                      facecolor='mistyrose', 
                                      edgecolor='darkred', linewidth=2)
    ax.add_patch(update_detail_box)
    ax.text(7, 6.5, 'update() Internal Flow', ha='center', va='center',
            fontsize=13, fontweight='bold')
    
    steps = [
        '4.1: Reset has_spiked = false',
        '4.2: Check if membrane_potential >= threshold',
        '4.3a: If YES → Spike!',
        '     • Set has_spiked = true',
        '     • Increment spike_count',
        '     • Reset membrane_potential = resting_potential',
        '     • For each connection: target->receive_spike(weight)',
        '4.3b: If NO → Decay',
        '     • membrane_potential = resting + (potential - resting) × decay_factor'
    ]
    
    y_pos = 6.2
    for step in steps:
        ax.text(1.3, y_pos, step, ha='left', va='top',
               fontsize=9, family='monospace')
        y_pos -= 0.25
    
    # Learning flow
    learning_box = FancyBboxPatch((1, 1.5), 12, 2.5,
                                 boxstyle="round,pad=0.15",
                                 facecolor='lavender', 
                                 edgecolor='purple', linewidth=2)
    ax.add_patch(learning_box)
    ax.text(7, 3.5, 'Learning Flow (STDP)', ha='center', va='center',
            fontsize=13, fontweight='bold')
    
    learning_steps = [
        '5. set_time_step(time) - Called after update()',
        '    • If has_spiked: record last_spike_time and add to spike_history',
        '6. update_stdp(current_time, learning_rate)',
        '    • For each connection:',
        '    • Get post-synaptic neuron last_spike_time',
        '    • Calculate Δt = post_time - pre_time',
        '    • If Δt > 0: LTP (strengthen) → weight += learning_rate × exp(-Δt/τ+)',
        '    • If Δt < 0: LTD (weaken) → weight -= learning_rate × exp(Δt/τ-)',
        '    • Clamp weight to [0.0, 1.0]'
    ]
    
    y_pos = 3.2
    for step in learning_steps:
        ax.text(1.3, y_pos, step, ha='left', va='top',
               fontsize=9, family='monospace')
        y_pos -= 0.25
    
    # Arrows
    arrows = [
        ((2.25, 7.5), (5.75, 7.5), 'blue'),
        ((5.75, 7.5), (9.25, 7.5), 'green'),
        ((9.25, 7.5), (12.75, 7.5), 'orange'),
        ((12.75, 7.5), (7, 4.5), 'red'),
        ((7, 4.5), (7, 1.5), 'purple'),
    ]
    
    for (start, end, color) in arrows:
        arrow = FancyArrowPatch(start, end,
                               arrowstyle='->', mutation_scale=20,
                               color=color, linewidth=2, alpha=0.7)
        ax.add_patch(arrow)
    
    return fig

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Visualize neuron.cpp code structure')
    parser.add_argument('--flow', action='store_true',
                       help='Show method call flow diagram')
    parser.add_argument('--save', type=str, default=None,
                       help='Save figure to file')
    
    args = parser.parse_args()
    
    if args.flow:
        fig = create_method_call_flow()
    else:
        fig = create_code_structure_diagram()
    
    if args.save:
        fig.savefig(args.save, dpi=300, bbox_inches='tight')
        print(f"Code structure diagram saved to {args.save}")
    else:
        plt.show()

if __name__ == '__main__':
    main()


