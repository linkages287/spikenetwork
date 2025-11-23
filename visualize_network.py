#!/usr/bin/env python3
"""
Dynamic visualization of spike neural network connections
Shows neurons as nodes and connections as edges with real-time state updates
"""

import json
import sys
import time
import argparse

# Check for required modules and provide helpful error messages
try:
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
except ImportError:
    print("ERROR: matplotlib not found.")
    print("Please install it using one of the following:")
    print("  1. Run: ./setup_visualization.sh")
    print("  2. Or: pip install matplotlib")
    print("  3. Or activate venv and: pip install -r requirements.txt")
    sys.exit(1)

try:
    import networkx as nx
except ImportError:
    print("ERROR: networkx not found.")
    print("Please install it using one of the following:")
    print("  1. Run: ./setup_visualization.sh")
    print("  2. Or: pip install networkx")
    print("  3. Or activate venv and: pip install -r requirements.txt")
    sys.exit(1)

try:
    import numpy as np
except ImportError:
    print("ERROR: numpy not found.")
    print("Please install it using one of the following:")
    print("  1. Run: ./setup_visualization.sh")
    print("  2. Or: pip install numpy")
    print("  3. Or activate venv and: pip install -r requirements.txt")
    sys.exit(1)

from matplotlib.patches import FancyBboxPatch

class NetworkVisualizer:
    def __init__(self, json_file=None, data=None, update_interval=0.5):
        """
        Initialize the network visualizer
        
        Args:
            json_file: Path to JSON file with network data
            data: Direct JSON data (dict)
            update_interval: Time between updates in seconds
        """
        self.update_interval = update_interval
        self.fig = None
        self.ax = None
        self.G = None
        self.pos = None
        self.current_data = None
        self.time_steps = []  # List of time step data
        self.current_step = 0
        self.previous_data = None  # For detecting active connections
        self.connection_activity = {}  # Track connection usage over time
        
        if json_file:
            self.load_from_file(json_file)
        elif data:
            self.load_data(data)
        else:
            raise ValueError("Either json_file or data must be provided")
    
    def load_from_file(self, json_file):
        """Load network data from JSON file"""
        with open(json_file, 'r') as f:
            self.current_data = json.load(f)
        self._build_graph()
    
    def load_data(self, data):
        """Load network data directly"""
        if isinstance(data, str):
            self.current_data = json.loads(data)
        else:
            self.current_data = data
        self._build_graph()
    
    def _build_graph(self):
        """Build networkx graph from JSON data"""
        self.G = nx.DiGraph()
        
        # Add nodes
        for neuron in self.current_data['neurons']:
            self.G.add_node(neuron['id'], 
                          potential=neuron['potential'],
                          spiked=neuron['spiked'],
                          spike_count=neuron['spike_count'])
        
        # Add edges
        for neuron in self.current_data['neurons']:
            for conn in neuron['connections']:
                self.G.add_edge(neuron['id'], conn['target'], 
                              weight=conn['weight'])
        
        # Calculate layout (circular for better visualization)
        self.pos = nx.spring_layout(self.G, k=2, iterations=50, seed=42)
        # Alternative: circular layout
        # self.pos = nx.circular_layout(self.G)
    
    def update_data(self, data):
        """Update network data and rebuild graph"""
        if isinstance(data, str):
            self.current_data = json.loads(data)
        else:
            self.current_data = data
        self._build_graph()
    
    def _detect_active_connections(self):
        """Detect which connections are active (just transmitted a spike)"""
        active_edges = set()
        
        if self.previous_data is None:
            return active_edges
        
        # Create mapping of previous neuron states
        prev_neurons = {n['id']: n for n in self.previous_data['neurons']}
        curr_neurons = {n['id']: n for n in self.current_data['neurons']}
        
        # Find connections that transmitted spikes
        for neuron in self.current_data['neurons']:
            neuron_id = neuron['id']
            prev_neuron = prev_neurons.get(neuron_id)
            
            if prev_neuron:
                # Check if this neuron just spiked
                if neuron['spiked'] and not prev_neuron['spiked']:
                    # This neuron just spiked, mark all its outgoing connections as active
                    for conn in neuron['connections']:
                        active_edges.add((neuron_id, conn['target']))
                
                # Check if potential increased significantly (received spike)
                potential_increase = neuron['potential'] - prev_neuron['potential']
                if potential_increase > 0.01:  # Threshold for detecting received spike
                    # Find which connection might have caused this
                    for prev_neuron_data in self.previous_data['neurons']:
                        if prev_neuron_data['spiked']:
                            for conn in prev_neuron_data['connections']:
                                if conn['target'] == neuron_id:
                                    active_edges.add((prev_neuron_data['id'], neuron_id))
        
        return active_edges
    
    def draw_network(self, ax=None, step_info=None):
        """Draw the network visualization with dynamic connection highlighting"""
        if ax is None:
            ax = self.ax
        
        ax.clear()
        
        # Detect active connections (just used for spike propagation)
        active_edges = self._detect_active_connections()
        
        # Color nodes based on state
        node_colors = []
        node_sizes = []
        for node_id in self.G.nodes():
            node_data = self.G.nodes[node_id]
            potential = node_data['potential']
            spiked = node_data['spiked']
            
            # Color: red if spiked, intensity based on potential
            if spiked:
                node_colors.append('#FF0000')  # Bright red for spiked
                node_sizes.append(800)
            else:
                # Color intensity based on potential (0-1 range, mapped to blue-green)
                intensity = min(1.0, max(0.0, potential))
                node_colors.append(plt.cm.viridis(intensity))
                node_sizes.append(300 + intensity * 200)
        
        # Draw inactive edges first (background)
        inactive_edges = [(u, v) for u, v in self.G.edges() if (u, v) not in active_edges]
        if inactive_edges:
            edge_widths_inactive = [self.G[u][v]['weight'] * 2 for u, v in inactive_edges]
            nx.draw_networkx_edges(self.G, self.pos, ax=ax,
                                  edgelist=inactive_edges,
                                  width=edge_widths_inactive,
                                  edge_color='lightgray',
                                  alpha=0.3,
                                  arrows=True,
                                  arrowsize=15,
                                  arrowstyle='->',
                                  connectionstyle='arc3,rad=0.1')
        
        # Draw active edges (highlighted, thicker, brighter)
        if active_edges:
            edge_widths_active = [self.G[u][v]['weight'] * 5 for u, v in active_edges]
            nx.draw_networkx_edges(self.G, self.pos, ax=ax,
                                  edgelist=list(active_edges),
                                  width=edge_widths_active,
                                  edge_color='#FF6600',  # Bright orange for active
                                  alpha=0.9,
                                  arrows=True,
                                  arrowsize=25,
                                  arrowstyle='->',
                                  connectionstyle='arc3,rad=0.1',
                                  style='dashed')  # Dashed to make active connections stand out
        
        # Draw nodes
        nx.draw_networkx_nodes(self.G, self.pos, ax=ax,
                              node_color=node_colors,
                              node_size=node_sizes,
                              alpha=0.8,
                              edgecolors='black',
                              linewidths=2)
        
        # Add labels with potential values
        labels = {}
        for node_id in self.G.nodes():
            node_data = self.G.nodes[node_id]
            potential = node_data['potential']
            spike_count = node_data['spike_count']
            labels[node_id] = f"{node_id}\n{potential:.2f}\n({spike_count})"
        
        nx.draw_networkx_labels(self.G, self.pos, labels, ax=ax,
                                font_size=8, font_weight='bold')
        
        # Add edge labels (weights) - only for active edges to reduce clutter
        if active_edges:
            edge_labels = {(u, v): f"{self.G[u][v]['weight']:.2f}" 
                          for u, v in active_edges}
            nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels, ax=ax,
                                         font_size=7, alpha=0.9, font_color='red')
        
        # Title with step information
        title = "Spike Neural Network - Dynamic Connection Visualization"
        if step_info is not None:
            title += f" (Step {step_info})"
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.axis('off')
        ax.set_aspect('equal')
        
        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='red', label='Spiked Neuron'),
            Patch(facecolor='#FF6600', edgecolor='#FF6600', linestyle='--', label='Active Connection'),
            Patch(facecolor='lightgray', label='Inactive Connection')
        ]
        ax.legend(handles=legend_elements, loc='upper left', fontsize=9)
    
    def show_static(self):
        """Show a static visualization"""
        self.fig, self.ax = plt.subplots(figsize=(14, 10))
        self.draw_network()
        plt.tight_layout()
        plt.show()
    
    def load_time_series(self, base_filename, num_steps=None):
        """
        Load multiple time step files for animation
        
        Args:
            base_filename: Base filename (e.g., 'network_step0.json')
            num_steps: Number of steps to load (None = auto-detect)
        """
        import os
        import re
        
        # Extract base path and pattern
        match = re.search(r'(.+)_step\d+\.json$', base_filename)
        if match:
            base_path = match.group(1)
            pattern = f"{base_path}_step(\\d+)\\.json"
        else:
            # Try to find step files
            base_path = base_filename.replace('.json', '')
            pattern = f"{base_path}_step(\\d+)\\.json"
        
        # Find all step files
        step_files = []
        dir_path = os.path.dirname(base_filename) if os.path.dirname(base_filename) else '.'
        for filename in os.listdir(dir_path):
            match = re.match(pattern, filename)
            if match:
                step_num = int(match.group(1))
                step_files.append((step_num, os.path.join(dir_path, filename)))
        
        step_files.sort(key=lambda x: x[0])
        
        if num_steps:
            step_files = step_files[:num_steps]
        
        # Load all time steps
        self.time_steps = []
        for step_num, filepath in step_files:
            with open(filepath, 'r') as f:
                self.time_steps.append(json.load(f))
        
        if not self.time_steps:
            raise ValueError(f"No time step files found matching pattern: {pattern}")
        
        print(f"Loaded {len(self.time_steps)} time steps")
        return len(self.time_steps)
    
    def animate_time_series(self, interval=0.8, loop=True):
        """
        Animate through multiple time steps showing dynamic connections
        
        Args:
            interval: Time between frames in seconds
            loop: Whether to loop the animation
        """
        if not self.time_steps:
            raise ValueError("No time steps loaded. Use load_time_series() first.")
        
        self.fig, self.ax = plt.subplots(figsize=(16, 10))
        
        # Load first step to establish layout
        self.current_data = self.time_steps[0]
        self.previous_data = None
        self._build_graph()
        
        def update_frame(frame):
            try:
                step_idx = frame % len(self.time_steps) if loop else min(frame, len(self.time_steps) - 1)
                
                self.previous_data = self.current_data
                self.current_data = self.time_steps[step_idx]
                self.update_data(self.current_data)
                
                self.draw_network(step_info=step_idx)
                
                # Update connection activity tracking
                active = self._detect_active_connections()
                for edge in active:
                    if edge not in self.connection_activity:
                        self.connection_activity[edge] = 0
                    self.connection_activity[edge] += 1
                
            except Exception as e:
                print(f"Error updating frame: {e}")
        
        ani = animation.FuncAnimation(self.fig, update_frame, 
                                     interval=int(interval * 1000),
                                     blit=False, cache_frame_data=False,
                                     repeat=loop)
        plt.tight_layout()
        plt.show()
        return ani
    
    def animate(self, json_file=None, callback=None):
        """
        Create animated visualization that updates from file or callback
        
        Args:
            json_file: Path to JSON file that gets updated
            callback: Function that returns new JSON data
        """
        self.fig, self.ax = plt.subplots(figsize=(14, 10))
        
        def update_frame(frame):
            try:
                if json_file:
                    # Reload from file
                    with open(json_file, 'r') as f:
                        new_data = json.load(f)
                    self.previous_data = self.current_data
                    self.update_data(new_data)
                elif callback:
                    # Get new data from callback
                    new_data = callback()
                    if new_data:
                        self.previous_data = self.current_data
                        self.update_data(new_data)
                
                self.draw_network()
            except Exception as e:
                print(f"Error updating frame: {e}")
        
        ani = animation.FuncAnimation(self.fig, update_frame, 
                                     interval=int(self.update_interval * 1000),
                                     blit=False, cache_frame_data=False)
        plt.tight_layout()
        plt.show()
        return ani
    
    def show_connection_statistics(self):
        """Print statistics about connection usage"""
        if not self.connection_activity:
            print("No connection activity data available.")
            return
        
        print("\n=== Connection Activity Statistics ===")
        sorted_connections = sorted(self.connection_activity.items(), 
                                   key=lambda x: x[1], reverse=True)
        
        print(f"\nMost Active Connections (used {len(self.time_steps)} time steps):")
        for (from_node, to_node), count in sorted_connections[:10]:
            print(f"  {from_node} -> {to_node}: {count} activations")
        
        print(f"\nTotal unique connections used: {len(self.connection_activity)}")
        print(f"Total activations: {sum(self.connection_activity.values())}")


def main():
    parser = argparse.ArgumentParser(description='Visualize spike neural network')
    parser.add_argument('json_file', nargs='?', help='JSON file with network data')
    parser.add_argument('--animate', action='store_true', 
                       help='Animate visualization (updates from file)')
    parser.add_argument('--time-series', action='store_true',
                       help='Load and animate through multiple time step files')
    parser.add_argument('--interval', type=float, default=0.8,
                       help='Update interval in seconds (default: 0.8)')
    parser.add_argument('--steps', type=int, default=None,
                       help='Number of time steps to load (default: auto-detect)')
    parser.add_argument('--no-loop', action='store_true',
                       help='Don\'t loop the animation')
    parser.add_argument('--stats', action='store_true',
                       help='Show connection activity statistics after animation')
    
    args = parser.parse_args()
    
    if not args.json_file:
        print("Usage: python visualize_network.py <json_file> [options]")
        print("\nOptions:")
        print("  --animate          Animate from single file (updates from file)")
        print("  --time-series      Load and animate through multiple step files")
        print("  --interval <sec>   Update interval in seconds (default: 0.8)")
        print("  --steps <num>      Number of steps to load (default: auto-detect)")
        print("  --no-loop          Don't loop the animation")
        print("  --stats            Show connection statistics after animation")
        print("\nExamples:")
        print("  python visualize_network.py network_step0.json")
        print("  python visualize_network.py network_step0.json --time-series")
        print("  python visualize_network.py network.json --animate --interval 0.5")
        sys.exit(1)
    
    try:
        if args.time_series:
            # Load time series and animate
            # Create visualizer with first file to establish structure
            visualizer = NetworkVisualizer(json_file=args.json_file, 
                                          update_interval=args.interval)
            num_steps = visualizer.load_time_series(args.json_file, args.steps)
            
            print(f"Starting time series animation ({num_steps} steps)...")
            print("Close the window to stop.")
            
            ani = visualizer.animate_time_series(interval=args.interval, 
                                                 loop=not args.no_loop)
            
            if args.stats:
                # Wait for animation to complete (approximate)
                import time
                time.sleep(args.interval * num_steps * (1 if args.no_loop else 3))
                visualizer.show_connection_statistics()
            
        else:
            visualizer = NetworkVisualizer(json_file=args.json_file, 
                                          update_interval=args.interval)
            
            if args.animate:
                print("Starting animated visualization...")
                print("Close the window to stop.")
                visualizer.animate(json_file=args.json_file)
            else:
                print("Showing static visualization...")
                visualizer.show_static()
    
    except FileNotFoundError:
        print(f"Error: File '{args.json_file}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

