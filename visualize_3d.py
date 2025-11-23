#!/usr/bin/env python3
"""
3D visualization of spike neural network structure
Shows neurons as 3D nodes and connections as 3D edges
"""

import json
import sys
import argparse
import numpy as np

# Check for required modules
try:
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    from mpl_toolkits.mplot3d.art3d import Line3DCollection
except ImportError:
    print("ERROR: matplotlib not found.")
    print("Please install it using: pip install matplotlib")
    sys.exit(1)

try:
    import networkx as nx
except ImportError:
    print("ERROR: networkx not found.")
    print("Please install it using: pip install networkx")
    sys.exit(1)


class Network3DVisualizer:
    def __init__(self, json_file=None, data=None):
        """
        Initialize the 3D network visualizer
        
        Args:
            json_file: Path to JSON file with network data
            data: Direct JSON data (dict)
        """
        self.fig = None
        self.ax = None
        self.G = None
        self.pos_3d = None
        self.current_data = None
        
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
    
    def _calculate_3d_layout(self, layout_type='spring'):
        """
        Calculate 3D positions for neurons
        
        Args:
            layout_type: 'spring', 'circular', 'layered', or 'spherical'
        """
        num_nodes = len(self.G.nodes())
        
        if layout_type == 'spring':
            # Use spring layout in 2D, then add z dimension based on layer
            pos_2d = nx.spring_layout(self.G, k=2, iterations=50, seed=42)
            self.pos_3d = {}
            
            # Try to detect layers (input, hidden, output)
            # Simple heuristic: nodes with no incoming edges are input
            # nodes with no outgoing edges are output
            in_degree = dict(self.G.in_degree())
            out_degree = dict(self.G.out_degree())
            
            for node_id in self.G.nodes():
                x, y = pos_2d[node_id]
                # Assign z based on degree (input=0, hidden=1, output=2)
                if in_degree[node_id] == 0:
                    z = 0  # Input layer
                elif out_degree[node_id] == 0:
                    z = 2  # Output layer
                else:
                    z = 1  # Hidden layer
                
                self.pos_3d[node_id] = np.array([x, y, z])
        
        elif layout_type == 'circular':
            # Arrange in a circle in XY plane, stack layers in Z
            angles = np.linspace(0, 2*np.pi, num_nodes, endpoint=False)
            radius = 2.0
            
            in_degree = dict(self.G.in_degree())
            out_degree = dict(self.G.out_degree())
            
            self.pos_3d = {}
            for i, node_id in enumerate(self.G.nodes()):
                x = radius * np.cos(angles[i])
                y = radius * np.sin(angles[i])
                
                if in_degree[node_id] == 0:
                    z = 0
                elif out_degree[node_id] == 0:
                    z = 2
                else:
                    z = 1
                
                self.pos_3d[node_id] = np.array([x, y, z])
        
        elif layout_type == 'layered':
            # Explicit layered layout
            in_degree = dict(self.G.in_degree())
            out_degree = dict(self.G.out_degree())
            
            input_nodes = [n for n in self.G.nodes() if in_degree[n] == 0]
            output_nodes = [n for n in self.G.nodes() if out_degree[n] == 0]
            hidden_nodes = [n for n in self.G.nodes() 
                          if n not in input_nodes and n not in output_nodes]
            
            self.pos_3d = {}
            
            # Input layer (z=0)
            for i, node_id in enumerate(input_nodes):
                x = -2.0 + (i % 7) * 0.6
                y = -1.0 + (i // 7) * 0.6
                self.pos_3d[node_id] = np.array([x, y, 0])
            
            # Hidden layer (z=1)
            for i, node_id in enumerate(hidden_nodes):
                angle = 2 * np.pi * i / len(hidden_nodes)
                radius = 1.5
                self.pos_3d[node_id] = np.array([
                    radius * np.cos(angle),
                    radius * np.sin(angle),
                    1
                ])
            
            # Output layer (z=2)
            for i, node_id in enumerate(output_nodes):
                x = -1.5 + i * 0.3
                y = 2.0
                self.pos_3d[node_id] = np.array([x, y, 2])
        
        elif layout_type == 'spherical':
            # Arrange nodes on a sphere
            phi = np.linspace(0, np.pi, num_nodes)
            theta = np.linspace(0, 2*np.pi, num_nodes)
            radius = 2.0
            
            self.pos_3d = {}
            for i, node_id in enumerate(self.G.nodes()):
                x = radius * np.sin(phi[i]) * np.cos(theta[i])
                y = radius * np.sin(phi[i]) * np.sin(theta[i])
                z = radius * np.cos(phi[i])
                self.pos_3d[node_id] = np.array([x, y, z])
        
        else:
            raise ValueError(f"Unknown layout type: {layout_type}")
    
    def draw_3d_network(self, layout_type='layered', show_labels=True, 
                       node_size_scale=100, edge_width_scale=2):
        """
        Draw the network in 3D
        
        Args:
            layout_type: 'spring', 'circular', 'layered', or 'spherical'
            show_labels: Whether to show neuron labels
            node_size_scale: Scale factor for node sizes
            edge_width_scale: Scale factor for edge widths
        """
        self.fig = plt.figure(figsize=(16, 12))
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        # Calculate 3D positions
        self._calculate_3d_layout(layout_type)
        
        # Prepare node data
        node_colors = []
        node_sizes = []
        node_positions = []
        
        for node_id in self.G.nodes():
            node_data = self.G.nodes[node_id]
            potential = node_data['potential']
            spiked = node_data['spiked']
            spike_count = node_data['spike_count']
            
            pos = self.pos_3d[node_id]
            node_positions.append(pos)
            
            # Color based on state
            if spiked:
                node_colors.append('#FF0000')  # Red for spiked
                node_sizes.append(node_size_scale * 1.5)
            else:
                # Color intensity based on potential
                intensity = min(1.0, max(0.0, potential))
                # Use colormap: blue (low) to green (high)
                node_colors.append(plt.cm.viridis(intensity))
                node_sizes.append(node_size_scale * (0.5 + intensity))
        
        # Draw edges
        edge_positions = []
        edge_colors = []
        edge_widths = []
        
        for u, v in self.G.edges():
            pos_u = self.pos_3d[u]
            pos_v = self.pos_3d[v]
            weight = self.G[u][v]['weight']
            
            edge_positions.append([pos_u, pos_v])
            edge_colors.append(plt.cm.Greys(0.3 + weight * 0.5))  # Darker for stronger weights
            edge_widths.append(weight * edge_width_scale)
        
        # Draw edges as lines
        for i, (edge_pos, color, width) in enumerate(zip(edge_positions, edge_colors, edge_widths)):
            x = [edge_pos[0][0], edge_pos[1][0]]
            y = [edge_pos[0][1], edge_pos[1][1]]
            z = [edge_pos[0][2], edge_pos[1][2]]
            self.ax.plot(x, y, z, color=color, alpha=0.4, linewidth=width)
        
        # Draw nodes
        for i, (pos, color, size) in enumerate(zip(node_positions, node_colors, node_sizes)):
            self.ax.scatter(pos[0], pos[1], pos[2], 
                          c=[color], s=size, alpha=0.8, 
                          edgecolors='black', linewidths=1)
            
            # Add labels
            if show_labels:
                node_id = list(self.G.nodes())[i]
                node_data = self.G.nodes[node_id]
                label = f"{node_id}\n{node_data['potential']:.2f}"
                self.ax.text(pos[0], pos[1], pos[2], label, 
                           fontsize=6, ha='center', va='center')
        
        # Set labels and title
        self.ax.set_xlabel('X', fontsize=12)
        self.ax.set_ylabel('Y', fontsize=12)
        self.ax.set_zlabel('Z (Layer)', fontsize=12)
        self.ax.set_title('3D Spike Neural Network Visualization', 
                         fontsize=14, fontweight='bold')
        
        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            plt.Line2D([0], [0], marker='o', color='w', 
                      markerfacecolor='red', markersize=10, label='Spiked Neuron'),
            plt.Line2D([0], [0], marker='o', color='w', 
                      markerfacecolor='blue', markersize=10, label='Low Potential'),
            plt.Line2D([0], [0], marker='o', color='w', 
                      markerfacecolor='green', markersize=10, label='High Potential'),
        ]
        self.ax.legend(handles=legend_elements, loc='upper left')
        
        # Set equal aspect ratio
        max_range = np.array([
            max([p[0] for p in node_positions]) - min([p[0] for p in node_positions]),
            max([p[1] for p in node_positions]) - min([p[1] for p in node_positions]),
            max([p[2] for p in node_positions]) - min([p[2] for p in node_positions])
        ]).max() / 2.0
        
        mid_x = (max([p[0] for p in node_positions]) + min([p[0] for p in node_positions])) * 0.5
        mid_y = (max([p[1] for p in node_positions]) + min([p[1] for p in node_positions])) * 0.5
        mid_z = (max([p[2] for p in node_positions]) + min([p[2] for p in node_positions])) * 0.5
        
        self.ax.set_xlim(mid_x - max_range, mid_x + max_range)
        self.ax.set_ylim(mid_y - max_range, mid_y + max_range)
        self.ax.set_zlim(mid_z - max_range, mid_z + max_range)
    
    def show(self):
        """Display the 3D visualization"""
        plt.tight_layout()
        plt.show()
    
    def save(self, filename):
        """Save the visualization to file"""
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"3D visualization saved to {filename}")


def main():
    parser = argparse.ArgumentParser(description='3D visualization of spike neural network')
    parser.add_argument('json_file', nargs='?', help='JSON file with network data')
    parser.add_argument('--layout', choices=['spring', 'circular', 'layered', 'spherical'],
                       default='layered', help='3D layout type (default: layered)')
    parser.add_argument('--no-labels', action='store_true',
                       help='Hide neuron labels')
    parser.add_argument('--node-size', type=float, default=100,
                       help='Node size scale (default: 100)')
    parser.add_argument('--edge-width', type=float, default=2,
                       help='Edge width scale (default: 2)')
    parser.add_argument('--save', type=str, default=None,
                       help='Save visualization to file instead of displaying')
    
    args = parser.parse_args()
    
    if not args.json_file:
        print("Usage: python visualize_3d.py <json_file> [options]")
        print("\nOptions:")
        print("  --layout <type>     Layout type: spring, circular, layered, spherical")
        print("  --no-labels         Hide neuron labels")
        print("  --node-size <num>   Node size scale")
        print("  --edge-width <num>  Edge width scale")
        print("  --save <file>       Save to file instead of displaying")
        print("\nExamples:")
        print("  python visualize_3d.py network.json")
        print("  python visualize_3d.py network.json --layout spherical")
        print("  python visualize_3d.py network.json --save network_3d.png")
        sys.exit(1)
    
    try:
        visualizer = Network3DVisualizer(json_file=args.json_file)
        visualizer.draw_3d_network(
            layout_type=args.layout,
            show_labels=not args.no_labels,
            node_size_scale=args.node_size,
            edge_width_scale=args.edge_width
        )
        
        if args.save:
            visualizer.save(args.save)
        else:
            visualizer.show()
    
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

