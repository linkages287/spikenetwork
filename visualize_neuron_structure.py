#!/usr/bin/env python3
"""
Visualize the internal structure and components of a spike neuron
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle, Ellipse
import numpy as np

def create_neuron_diagram():
    """Create a detailed diagram of neuron structure"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'Spike Neuron Internal Structure', 
            ha='center', fontsize=20, fontweight='bold')
    
    # Main neuron body (soma)
    neuron_body = Ellipse((5, 5), 2.5, 2.5, 
                         facecolor='lightblue', 
                         edgecolor='black', linewidth=2)
    ax.add_patch(neuron_body)
    ax.text(5, 5, 'NEURON\nSOMA', ha='center', va='center', 
            fontsize=14, fontweight='bold')
    
    # Membrane potential indicator
    potential_box = FancyBboxPatch((1.5, 6.5), 1.2, 0.8,
                                   boxstyle="round,pad=0.1",
                                   facecolor='yellow', 
                                   edgecolor='black', linewidth=1.5)
    ax.add_patch(potential_box)
    ax.text(2.1, 6.9, 'Membrane\nPotential', ha='center', va='center',
            fontsize=10, fontweight='bold')
    ax.text(2.1, 6.3, 'V(t)', ha='center', va='center',
            fontsize=12, style='italic')
    
    # Threshold indicator
    threshold_box = FancyBboxPatch((7.3, 6.5), 1.2, 0.8,
                                  boxstyle="round,pad=0.1",
                                  facecolor='orange', 
                                  edgecolor='black', linewidth=1.5)
    ax.add_patch(threshold_box)
    ax.text(7.9, 6.9, 'Threshold', ha='center', va='center',
            fontsize=10, fontweight='bold')
    ax.text(7.9, 6.3, 'θ', ha='center', va='center',
            fontsize=12, style='italic')
    
    # Spike indicator
    spike_indicator = FancyBboxPatch((3.5, 7.5), 3, 0.6,
                                    boxstyle="round,pad=0.1",
                                    facecolor='red', 
                                    edgecolor='darkred', linewidth=2)
    ax.add_patch(spike_indicator)
    ax.text(5, 7.8, 'SPIKE OUTPUT', ha='center', va='center',
            fontsize=11, fontweight='bold', color='white')
    
    # Decay mechanism
    decay_box = FancyBboxPatch((1.5, 3.5), 1.2, 0.8,
                              boxstyle="round,pad=0.1",
                              facecolor='lightgreen', 
                              edgecolor='black', linewidth=1.5)
    ax.add_patch(decay_box)
    ax.text(2.1, 3.9, 'Decay\nFactor', ha='center', va='center',
            fontsize=10, fontweight='bold')
    ax.text(2.1, 3.3, 'λ', ha='center', va='center',
            fontsize=12, style='italic')
    
    # Resting potential
    resting_box = FancyBboxPatch((7.3, 3.5), 1.2, 0.8,
                                boxstyle="round,pad=0.1",
                                facecolor='lightcoral', 
                                edgecolor='black', linewidth=1.5)
    ax.add_patch(resting_box)
    ax.text(7.9, 3.9, 'Resting\nPotential', ha='center', va='center',
            fontsize=10, fontweight='bold')
    ax.text(7.9, 3.3, 'V_rest', ha='center', va='center',
            fontsize=12, style='italic')
    
    # Input connections (dendrites)
    for i in range(3):
        x_start = 0.5 + i * 0.8
        y_start = 2.0
        
        # Dendrite line
        ax.plot([x_start, 3.5 + i * 0.3], [y_start, 4.0], 
               'k-', linewidth=2, alpha=0.6)
        
        # Synapse
        synapse = Circle((3.5 + i * 0.3, 4.0), 0.15, 
                        facecolor='purple', edgecolor='black')
        ax.add_patch(synapse)
        
        # Weight label
        ax.text(x_start - 0.3, y_start, f'w{i+1}', 
               fontsize=9, style='italic')
        
        # Input arrow
        arrow = FancyArrowPatch((x_start, y_start), 
                               (3.5 + i * 0.3, 4.0),
                               arrowstyle='->', mutation_scale=20,
                               color='blue', linewidth=1.5, alpha=0.7)
        ax.add_patch(arrow)
    
    ax.text(1.5, 1.5, 'INPUT\nCONNECTIONS', ha='center', va='center',
            fontsize=10, fontweight='bold', 
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
    
    # Output connections (axon)
    for i in range(3):
        x_end = 6.5 + i * 0.3
        y_end = 1.5
        
        # Axon line
        ax.plot([6.5 + i * 0.3, x_end], [4.0, y_end], 
               'k-', linewidth=2, alpha=0.6)
        
        # Output synapse
        synapse = Circle((x_end, y_end), 0.15, 
                        facecolor='red', edgecolor='black')
        ax.add_patch(synapse)
        
        # Output arrow
        arrow = FancyArrowPatch((6.5 + i * 0.3, 4.0), 
                               (x_end, y_end),
                               arrowstyle='->', mutation_scale=20,
                               color='red', linewidth=1.5, alpha=0.7)
        ax.add_patch(arrow)
    
    ax.text(8.5, 1.5, 'OUTPUT\nCONNECTIONS', ha='center', va='center',
            fontsize=10, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.5))
    
    # Equations and formulas
    formula_box = FancyBboxPatch((1, 0.2), 8, 0.8,
                                boxstyle="round,pad=0.1",
                                facecolor='wheat', 
                                edgecolor='black', linewidth=1.5)
    ax.add_patch(formula_box)
    
    formulas = [
        "Update: V(t+1) = V_rest + (V(t) - V_rest) × λ + Σ(w_i × spike_i)",
        "Spike: if V(t) ≥ θ then spike = 1, V(t) = V_rest",
        "STDP: Δw = learning_rate × exp(-Δt/τ)  (LTP if pre→post, LTD if post→pre)"
    ]
    
    for i, formula in enumerate(formulas):
        ax.text(5, 0.6 - i * 0.25, formula, ha='center', va='center',
               fontsize=9, family='monospace')
    
    # Legend
    legend_elements = [
        mpatches.Patch(facecolor='lightblue', edgecolor='black', label='Neuron Body (Soma)'),
        mpatches.Patch(facecolor='yellow', label='Membrane Potential'),
        mpatches.Patch(facecolor='orange', label='Threshold'),
        mpatches.Patch(facecolor='red', label='Spike Output'),
        mpatches.Patch(facecolor='purple', label='Input Synapse'),
        mpatches.Patch(facecolor='lightgreen', label='Decay Mechanism'),
    ]
    
    ax.legend(handles=legend_elements, loc='upper right', fontsize=9)
    
    plt.tight_layout()
    return fig, ax

def create_detailed_neuron_view():
    """Create a more detailed view showing internal processes"""
    fig = plt.figure(figsize=(16, 12))
    
    # Create subplots
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
    
    # Main neuron diagram
    ax1 = fig.add_subplot(gs[0, :])
    ax1.set_xlim(0, 12)
    ax1.set_ylim(0, 8)
    ax1.axis('off')
    
    ax1.text(6, 7.5, 'Spike Neuron - Complete Structure', 
            ha='center', fontsize=18, fontweight='bold')
    
    # Neuron with all components
    # Soma
    soma = Ellipse((6, 4), 3, 2.5, facecolor='lightblue', 
                  edgecolor='navy', linewidth=3)
    ax1.add_patch(soma)
    ax1.text(6, 4, 'NEURON', ha='center', va='center',
            fontsize=16, fontweight='bold')
    
    # Internal components
    # Membrane potential gauge
    gauge_rect = Rectangle((4.5, 3), 3, 1, 
                          facecolor='white', edgecolor='black', linewidth=2)
    ax1.add_patch(gauge_rect)
    ax1.text(6, 3.5, 'Membrane Potential', ha='center', va='center',
            fontsize=11, fontweight='bold')
    
    # Potential level indicator
    potential_level = Rectangle((4.6, 3.1), 1.5, 0.8, 
                               facecolor='green', alpha=0.7)
    ax1.add_patch(potential_level)
    ax1.text(5.35, 3.5, 'V(t)', ha='center', va='center',
            fontsize=12, fontweight='bold')
    
    # Threshold line
    threshold_line = plt.Line2D([7.5, 7.5], [3, 4], 
                               color='red', linewidth=3, linestyle='--')
    ax1.add_line(threshold_line)
    ax1.text(7.7, 3.5, 'θ', ha='left', va='center',
            fontsize=14, fontweight='bold', color='red')
    
    # Spike counter
    spike_counter = FancyBboxPatch((9, 2.5), 2, 1,
                                  boxstyle="round,pad=0.1",
                                  facecolor='red', 
                                  edgecolor='darkred', linewidth=2)
    ax1.add_patch(spike_counter)
    ax1.text(10, 3, 'Spike\nCount', ha='center', va='center',
            fontsize=11, fontweight='bold', color='white')
    
    # Input dendrites with synapses
    for i in range(5):
        angle = np.pi * (i + 1) / 6
        x_start = 6 + 2 * np.cos(angle)
        y_start = 4 + 1.5 * np.sin(angle)
        x_end = 6 + 1.5 * np.cos(angle)
        y_end = 4 + 1.2 * np.sin(angle)
        
        ax1.plot([x_start, x_end], [y_start, y_end], 
               'b-', linewidth=2, alpha=0.6)
        
        synapse = Circle((x_end, y_end), 0.2, 
                        facecolor='purple', edgecolor='black', linewidth=2)
        ax1.add_patch(synapse)
        
        # Weight label
        ax1.text(x_start + 0.3 * np.cos(angle), 
                y_start + 0.3 * np.sin(angle),
                f'w{i+1}', fontsize=8, style='italic')
    
    ax1.text(2, 5.5, 'INPUT\nSYNAPSES', ha='center', va='center',
            fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
    
    # Output axon
    ax1.plot([7.5, 10], [4, 4], 'r-', linewidth=3)
    ax1.plot([10, 11], [4, 4], 'r-', linewidth=4)
    
    # Output synapses
    for i in range(3):
        y_pos = 1.5 + i * 0.8
        ax1.plot([10, 11], [4, y_pos], 'r-', linewidth=2, alpha=0.6)
        synapse = Circle((11, y_pos), 0.15, 
                        facecolor='red', edgecolor='black')
        ax1.add_patch(synapse)
    
    ax1.text(11.5, 2.5, 'OUTPUT\nSYNAPSES', ha='center', va='center',
            fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.7))
    
    # State diagram
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis('off')
    
    ax2.text(5, 9, 'Neuron State Machine', ha='center', 
            fontsize=14, fontweight='bold')
    
    # States
    resting = Circle((3, 7), 1, facecolor='lightgreen', 
                   edgecolor='black', linewidth=2)
    ax2.add_patch(resting)
    ax2.text(3, 7, 'Resting', ha='center', va='center', fontsize=10)
    
    integrating = Circle((7, 7), 1, facecolor='yellow', 
                        edgecolor='black', linewidth=2)
    ax2.add_patch(integrating)
    ax2.text(7, 7, 'Integrating', ha='center', va='center', fontsize=10)
    
    spiking = Circle((5, 4), 1, facecolor='red', 
                    edgecolor='black', linewidth=2)
    ax2.add_patch(spiking)
    ax2.text(5, 4, 'Spiking', ha='center', va='center', 
            fontsize=10, color='white', fontweight='bold')
    
    # Transitions
    ax2.arrow(3.7, 7, 2.6, 0, head_width=0.3, head_length=0.3, 
             fc='blue', ec='blue', linewidth=2)
    ax2.text(5, 7.5, 'V ≥ θ', ha='center', fontsize=9, style='italic')
    
    ax2.arrow(5, 5, 0, 0.3, head_width=0.3, head_length=0.3, 
             fc='blue', ec='blue', linewidth=2)
    ax2.text(5.5, 4.5, 'Reset', ha='left', fontsize=9, style='italic')
    
    ax2.arrow(4.3, 4, -0.6, 2.5, head_width=0.3, head_length=0.3, 
             fc='green', ec='green', linewidth=2)
    ax2.text(2.5, 5.5, 'Decay', ha='center', fontsize=9, style='italic')
    
    # Parameters table
    ax3 = fig.add_subplot(gs[1, 1])
    ax3.axis('off')
    
    ax3.text(0.5, 0.95, 'Neuron Parameters', ha='left', 
            fontsize=14, fontweight='bold', transform=ax3.transAxes)
    
    params = [
        ('Membrane Potential', 'V(t)', 'Current voltage level'),
        ('Threshold', 'θ', 'Spike trigger level'),
        ('Resting Potential', 'V_rest', 'Baseline voltage'),
        ('Decay Factor', 'λ', 'Voltage decay rate (0-1)'),
        ('Connection Weight', 'w', 'Synaptic strength'),
        ('Spike Count', 'N', 'Total spikes fired'),
        ('Last Spike Time', 't_last', 'For STDP learning'),
    ]
    
    y_pos = 0.85
    for name, symbol, desc in params:
        ax3.text(0.05, y_pos, f'{name} ({symbol}):', ha='left',
                fontsize=11, fontweight='bold', transform=ax3.transAxes)
        ax3.text(0.05, y_pos - 0.05, f'  {desc}', ha='left',
                fontsize=9, style='italic', transform=ax3.transAxes)
        y_pos -= 0.12
    
    plt.suptitle('Complete Spike Neuron Architecture', 
                fontsize=20, fontweight='bold', y=0.98)
    
    return fig

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Visualize neuron structure')
    parser.add_argument('--detailed', action='store_true',
                       help='Show detailed view with state machine')
    parser.add_argument('--save', type=str, default=None,
                       help='Save figure to file')
    
    args = parser.parse_args()
    
    if args.detailed:
        fig = create_detailed_neuron_view()
    else:
        fig, ax = create_neuron_diagram()
    
    if args.save:
        fig.savefig(args.save, dpi=300, bbox_inches='tight')
        print(f"Neuron structure diagram saved to {args.save}")
    else:
        plt.show()

if __name__ == '__main__':
    main()


