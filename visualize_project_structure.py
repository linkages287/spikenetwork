#!/usr/bin/env python3
"""
Visualize complete project structure - all files and their interconnections
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Ellipse
import numpy as np

def create_project_structure_diagram():
    """Create comprehensive project structure diagram"""
    fig = plt.figure(figsize=(20, 16))
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 22)
    ax.set_ylim(0, 18)
    ax.axis('off')
    
    # Title
    ax.text(11, 17.5, 'Spike Neural Network Project - Complete File Structure', 
            ha='center', fontsize=20, fontweight='bold')
    ax.text(11, 17, 'All Files and Their Interconnections', 
            ha='center', fontsize=14, style='italic')
    
    # Core Library Files (C++ Headers & Implementation)
    core_box = FancyBboxPatch((0.5, 13.5), 6, 3,
                              boxstyle="round,pad=0.2",
                              facecolor='lightblue', 
                              edgecolor='navy', linewidth=3)
    ax.add_patch(core_box)
    ax.text(3.5, 16, 'CORE LIBRARY', ha='center', va='center',
            fontsize=14, fontweight='bold')
    
    # neuron.h
    neuron_h_box = FancyBboxPatch((1, 15), 2.5, 0.8,
                                 boxstyle="round,pad=0.1",
                                 facecolor='white', 
                                 edgecolor='blue', linewidth=2)
    ax.add_patch(neuron_h_box)
    ax.text(2.25, 15.4, 'neuron.h', ha='center', va='center',
            fontsize=11, fontweight='bold', family='monospace')
    
    # neuron.cpp
    neuron_cpp_box = FancyBboxPatch((4, 15), 2.5, 0.8,
                                   boxstyle="round,pad=0.1",
                                   facecolor='lightcyan', 
                                   edgecolor='blue', linewidth=2)
    ax.add_patch(neuron_cpp_box)
    ax.text(5.25, 15.4, 'neuron.cpp', ha='center', va='center',
            fontsize=11, fontweight='bold', family='monospace')
    
    # network.h
    network_h_box = FancyBboxPatch((1, 14), 2.5, 0.8,
                                  boxstyle="round,pad=0.1",
                                  facecolor='white', 
                                  edgecolor='green', linewidth=2)
    ax.add_patch(network_h_box)
    ax.text(2.25, 14.4, 'network.h', ha='center', va='center',
            fontsize=11, fontweight='bold', family='monospace')
    
    # network.cpp
    network_cpp_box = FancyBboxPatch((4, 14), 2.5, 0.8,
                                    boxstyle="round,pad=0.1",
                                    facecolor='lightgreen', 
                                    edgecolor='green', linewidth=2)
    ax.add_patch(network_cpp_box)
    ax.text(5.25, 14.4, 'network.cpp', ha='center', va='center',
            fontsize=11, fontweight='bold', family='monospace')
    
    # Application Programs (C++)
    app_box = FancyBboxPatch((7.5, 13.5), 7, 3,
                            boxstyle="round,pad=0.2",
                            facecolor='lightyellow', 
                            edgecolor='orange', linewidth=3)
    ax.add_patch(app_box)
    ax.text(11, 16, 'APPLICATION PROGRAMS (C++)', ha='center', va='center',
            fontsize=14, fontweight='bold')
    
    apps = [
        ('main.cpp', 8, 15.5),
        ('train_numbers.cpp', 10.5, 15.5),
        ('train_with_animation.cpp', 13, 15.5),
        ('simulate_spiking.cpp', 15.5, 15.5),
        ('export_network.cpp', 8, 14.5),
        ('test_functionality.cpp', 10.5, 14.5),
        ('load_numbers.cpp', 13, 14.5),
    ]
    
    for name, x, y in apps:
        app_file_box = FancyBboxPatch((x, y), 2, 0.7,
                                     boxstyle="round,pad=0.1",
                                     facecolor='white', 
                                     edgecolor='orange', linewidth=1.5)
        ax.add_patch(app_file_box)
        ax.text(x+1, y+0.35, name, ha='center', va='center',
               fontsize=9, family='monospace')
    
    # Python Visualization Scripts
    py_box = FancyBboxPatch((15.5, 13.5), 6, 3,
                           boxstyle="round,pad=0.2",
                           facecolor='lightgreen', 
                           edgecolor='darkgreen', linewidth=3)
    ax.add_patch(py_box)
    ax.text(18.5, 16, 'PYTHON VISUALIZATION', ha='center', va='center',
            fontsize=14, fontweight='bold')
    
    py_scripts = [
        ('visualize_network.py', 16, 15.5),
        ('visualize_3d.py', 18.5, 15.5),
        ('animate_3d_spiking.py', 21, 15.5),
        ('animate_training.py', 16, 14.5),
        ('visualize_neuron_structure.py', 18.5, 14.5),
        ('visualize_neuron_code.py', 21, 14.5),
    ]
    
    for name, x, y in py_scripts:
        py_file_box = FancyBboxPatch((x, y), 2.3, 0.7,
                                    boxstyle="round,pad=0.1",
                                    facecolor='white', 
                                    edgecolor='darkgreen', linewidth=1.5)
        ax.add_patch(py_file_box)
        ax.text(x+1.15, y+0.35, name, ha='center', va='center',
               fontsize=8, family='monospace')
    
    # Build System & Scripts
    build_box = FancyBboxPatch((0.5, 10), 6, 2.5,
                              boxstyle="round,pad=0.2",
                              facecolor='wheat', 
                              edgecolor='brown', linewidth=3)
    ax.add_patch(build_box)
    ax.text(3.5, 12, 'BUILD SYSTEM & SCRIPTS', ha='center', va='center',
            fontsize=14, fontweight='bold')
    
    build_files = [
        ('Makefile', 1, 11.5),
        ('setup_visualization.sh', 4, 11.5),
        ('demo_visualization.sh', 1, 10.5),
        ('push_spike_network.sh', 4, 10.5),
    ]
    
    for name, x, y in build_files:
        build_file_box = FancyBboxPatch((x, y), 2.5, 0.8,
                                        boxstyle="round,pad=0.1",
                                        facecolor='white', 
                                        edgecolor='brown', linewidth=1.5)
        ax.add_patch(build_file_box)
        ax.text(x+1.25, y+0.4, name, ha='center', va='center',
               fontsize=9, family='monospace')
    
    # Data Files
    data_box = FancyBboxPatch((7.5, 10), 7, 2.5,
                             boxstyle="round,pad=0.2",
                             facecolor='lavender', 
                             edgecolor='purple', linewidth=3)
    ax.add_patch(data_box)
    ax.text(11, 12, 'DATA FILES', ha='center', va='center',
            fontsize=14, fontweight='bold')
    
    data_files = [
        ('*.json', 'Network states', 8, 11.5),
        ('requirements.txt', 'Python deps', 11, 11.5),
        ('trained_network.json', 'Trained model', 14, 11.5),
        ('spike_animation_*.json', 'Animation frames', 8, 10.5),
        ('training_epoch*.json', 'Training frames', 11, 10.5),
    ]
    
    for name, desc, x, y in data_files:
        data_file_box = FancyBboxPatch((x, y), 2.5, 0.8,
                                      boxstyle="round,pad=0.1",
                                      facecolor='white', 
                                      edgecolor='purple', linewidth=1.5)
        ax.add_patch(data_file_box)
        ax.text(x+1.25, y+0.5, name, ha='center', va='center',
               fontsize=8, family='monospace', fontweight='bold')
        ax.text(x+1.25, y+0.2, desc, ha='center', va='center',
               fontsize=7, style='italic')
    
    # Documentation
    doc_box = FancyBboxPatch((15.5, 10), 6, 2.5,
                            boxstyle="round,pad=0.2",
                            facecolor='mistyrose', 
                            edgecolor='darkred', linewidth=3)
    ax.add_patch(doc_box)
    ax.text(18.5, 12, 'DOCUMENTATION', ha='center', va='center',
            fontsize=14, fontweight='bold')
    
    doc_files = [
        ('README_visualization.md', 16, 11.5),
        ('README_number_recognition.md', 19, 11.5),
        ('DYNAMIC_CONNECTIONS.md', 16, 10.5),
    ]
    
    for name, x, y in doc_files:
        doc_file_box = FancyBboxPatch((x, y), 2.8, 0.8,
                                      boxstyle="round,pad=0.1",
                                      facecolor='white', 
                                      edgecolor='darkred', linewidth=1.5)
        ax.add_patch(doc_file_box)
        ax.text(x+1.4, y+0.4, name, ha='center', va='center',
               fontsize=8, family='monospace')
    
    # Executables (Compiled)
    exec_box = FancyBboxPatch((0.5, 7), 10, 2,
                             boxstyle="round,pad=0.2",
                             facecolor='lightcoral', 
                             edgecolor='red', linewidth=3)
    ax.add_patch(exec_box)
    ax.text(5.5, 8.5, 'COMPILED EXECUTABLES', ha='center', va='center',
            fontsize=14, fontweight='bold')
    
    executables = [
        ('spike_network', 1, 7.8),
        ('export_network', 3.5, 7.8),
        ('train_numbers', 6, 7.8),
        ('train_with_animation', 8.5, 7.8),
        ('simulate_spiking', 1, 7.2),
        ('test_functionality', 3.5, 7.2),
    ]
    
    for name, x, y in executables:
        exec_file_box = FancyBboxPatch((x, y), 2.2, 0.5,
                                      boxstyle="round,pad=0.1",
                                      facecolor='white', 
                                      edgecolor='red', linewidth=1.5)
        ax.add_patch(exec_file_box)
        ax.text(x+1.1, y+0.25, name, ha='center', va='center',
               fontsize=8, family='monospace', fontweight='bold')
    
    # Dependencies - Core Library
    # neuron.cpp -> neuron.h
    arrow1 = FancyArrowPatch((2.25, 15), (4, 15),
                            arrowstyle='->', mutation_scale=20,
                            color='blue', linewidth=2, alpha=0.7)
    ax.add_patch(arrow1)
    ax.text(3.1, 15.3, 'includes', ha='center', fontsize=7, style='italic')
    
    # network.cpp -> network.h
    arrow2 = FancyArrowPatch((2.25, 14), (4, 14),
                            arrowstyle='->', mutation_scale=20,
                            color='green', linewidth=2, alpha=0.7)
    ax.add_patch(arrow2)
    ax.text(3.1, 14.3, 'includes', ha='center', fontsize=7, style='italic')
    
    # network.h -> neuron.h
    arrow3 = FancyArrowPatch((2.25, 14.4), (2.25, 15),
                            arrowstyle='->', mutation_scale=20,
                            color='navy', linewidth=2, alpha=0.7)
    ax.add_patch(arrow3)
    ax.text(1.5, 14.7, 'includes', ha='center', fontsize=7, style='italic')
    
    # Applications -> Core Library
    for app_x in [9, 11.5, 14, 16.5]:
        arrow = FancyArrowPatch((app_x, 15.2), (5.25, 14.5),
                               arrowstyle='->', mutation_scale=15,
                               color='orange', linewidth=1.5, alpha=0.6,
                               linestyle='--')
        ax.add_patch(arrow)
    
    # Python scripts -> JSON data
    for py_x in [17.15, 19.65, 22.15]:
        arrow = FancyArrowPatch((py_x, 14.5), (11, 11),
                               arrowstyle='->', mutation_scale=15,
                               color='green', linewidth=1.5, alpha=0.6,
                               linestyle='--')
        ax.add_patch(arrow)
    
    # Executables -> Applications
    arrow4 = FancyArrowPatch((2.1, 7.8), (9, 15.2),
                            arrowstyle='->', mutation_scale=15,
                            color='red', linewidth=2, alpha=0.7,
                            linestyle='--')
    ax.add_patch(arrow4)
    ax.text(5, 11.5, 'compiles to', ha='center', fontsize=8, style='italic',
           rotation=45)
    
    # Makefile -> All C++ files
    arrow5 = FancyArrowPatch((3.5, 10), (11, 15),
                            arrowstyle='->', mutation_scale=20,
                            color='brown', linewidth=2, alpha=0.7)
    ax.add_patch(arrow5)
    ax.text(7, 12.5, 'builds', ha='center', fontsize=8, style='italic')
    
    # Data flow annotations
    flow_box = FancyBboxPatch((11.5, 7), 10, 2,
                             boxstyle="round,pad=0.15",
                             facecolor='lightgray', 
                             edgecolor='black', linewidth=2)
    ax.add_patch(flow_box)
    ax.text(16.5, 8.5, 'DATA FLOW', ha='center', va='center',
            fontsize=12, fontweight='bold')
    
    flows = [
        'C++ Programs → Generate JSON → Python Visualizes',
        'Training → Saves Network → Animation Scripts',
        'Makefile → Compiles → Executables → Run → JSON Output'
    ]
    
    y_pos = 8.2
    for flow in flows:
        ax.text(12, y_pos, f'• {flow}', ha='left', va='top',
               fontsize=9, style='italic')
        y_pos -= 0.4
    
    # Legend
    legend_elements = [
        mpatches.Patch(facecolor='lightblue', edgecolor='navy', label='Core Library'),
        mpatches.Patch(facecolor='lightyellow', edgecolor='orange', label='Applications'),
        mpatches.Patch(facecolor='lightgreen', edgecolor='darkgreen', label='Python Scripts'),
        mpatches.Patch(facecolor='wheat', edgecolor='brown', label='Build System'),
        mpatches.Patch(facecolor='lavender', edgecolor='purple', label='Data Files'),
        mpatches.Patch(facecolor='mistyrose', edgecolor='darkred', label='Documentation'),
        mpatches.Patch(facecolor='lightcoral', edgecolor='red', label='Executables'),
    ]
    
    ax.legend(handles=legend_elements, loc='lower left', fontsize=9, 
             bbox_to_anchor=(0.02, 0.02))
    
    # Key relationships text
    key_box = FancyBboxPatch((0.5, 4.5), 21, 2,
                            boxstyle="round,pad=0.15",
                            facecolor='aliceblue', 
                            edgecolor='steelblue', linewidth=2)
    ax.add_patch(key_box)
    ax.text(11, 6, 'KEY RELATIONSHIPS', ha='center', va='center',
            fontsize=13, fontweight='bold')
    
    relationships = [
        'neuron.h/cpp: Core neuron implementation (STDP learning, spike mechanism)',
        'network.h/cpp: Network container managing multiple neurons',
        'main.cpp: Basic network testing and demonstration',
        'train_numbers.cpp: Number recognition training with STDP',
        'simulate_spiking.cpp: Generates animation frames for visualization',
        'Python scripts: Read JSON, visualize network structure and dynamics',
        'Makefile: Builds all executables from source files',
        'JSON files: Intermediate data format for network state export/import'
    ]
    
    y_pos = 5.7
    for rel in relationships:
        ax.text(0.7, y_pos, f'• {rel}', ha='left', va='top',
               fontsize=9)
        y_pos -= 0.25
    
    return fig

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Visualize complete project structure')
    parser.add_argument('--save', type=str, default=None,
                       help='Save figure to file')
    
    args = parser.parse_args()
    
    fig = create_project_structure_diagram()
    
    if args.save:
        fig.savefig(args.save, dpi=300, bbox_inches='tight')
        print(f"Project structure diagram saved to {args.save}")
    else:
        plt.show()

if __name__ == '__main__':
    main()

