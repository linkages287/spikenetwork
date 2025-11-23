#!/usr/bin/env python3
"""
3D animated visualization of spike neural network showing spiking process
"""

import json
import sys
import argparse
import numpy as np
import os
import re

try:
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.animation as animation
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


class Spike3DAnimator:
    def __init__(self, base_filename):
        """
        Initialize the 3D spike animator
        
        Args:
            base_filename: Base filename (e.g., 'spike_animation_step0.json')
        """
        self.base_filename = base_filename
        self.time_steps = []
        self.G = None
        self.pos_3d = None
        self.fig = None
        self.ax = None
        self.current_step = 0
        
        self._load_time_series()
        self._build_graph()
        self._calculate_3d_layout()
    
    def _load_time_series(self):
        """Load all time step files"""
        match = re.search(r'(.+)_step\d+\.json$', self.base_filename)
        if match:
            base_path = match.group(1)
            pattern = f"{base_path}_step(\\d+)\\.json"
        else:
            base_path = self.base_filename.replace('.json', '')
            pattern = f"{base_path}_step(\\d+)\\.json"
        
        step_files = []
        dir_path = os.path.dirname(self.base_filename) if os.path.dirname(self.base_filename) else '.'
        
        if not os.path.exists(dir_path):
            dir_path = '.'
        
        for filename in os.listdir(dir_path):
            match = re.match(pattern, filename)
            if match:
                step_num = int(match.group(1))
                filepath = os.path.join(dir_path, filename)
                step_files.append((step_num, filepath))
        
        step_files.sort(key=lambda x: x[0])
        
        if not step_files:
            raise ValueError(f"No time step files found matching pattern: {pattern}")
        
        for step_num, filepath in step_files:
            with open(filepath, 'r') as f:
                self.time_steps.append(json.load(f))
        
        print(f"Loaded {len(self.time_steps)} time steps")
    
    def _build_graph(self):
        """Build networkx graph from first time step"""
        self.G = nx.DiGraph()
        
        # Use first time step to establish structure
        data = self.time_steps[0]
        
        for neuron in data['neurons']:
            self.G.add_node(neuron['id'])
        
        for neuron in data['neurons']:
            for conn in neuron['connections']:
                self.G.add_edge(neuron['id'], conn['target'], weight=conn['weight'])
    
    def _calculate_3d_layout(self):
        """Calculate 3D positions for neurons (layered layout)"""
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
    
    def _get_neuron_data(self, step_idx):
        """Get neuron data for a specific time step"""
        data = self.time_steps[step_idx]
        neuron_map = {n['id']: n for n in data['neurons']}
        return neuron_map
    
    def _draw_frame(self, step_idx):
        """Draw a single frame of the animation"""
        self.ax.clear()
        
        neuron_map = self._get_neuron_data(step_idx)
        
        # Prepare node data
        node_colors = []
        node_sizes = []
        node_positions = []
        
        for node_id in self.G.nodes():
            neuron_data = neuron_map.get(node_id, {})
            potential = neuron_data.get('potential', 0.0)
            spiked = neuron_data.get('spiked', False)
            
            pos = self.pos_3d[node_id]
            node_positions.append(pos)
            
            # Color based on state
            if spiked:
                node_colors.append('#FF0000')  # Bright red for spiked
                node_sizes.append(300)
            else:
                # Color intensity based on potential
                intensity = min(1.0, max(0.0, potential))
                node_colors.append(plt.cm.viridis(intensity))
                node_sizes.append(100 + intensity * 100)
        
        # Draw edges (all edges, lighter)
        for u, v in self.G.edges():
            pos_u = self.pos_3d[u]
            pos_v = self.pos_3d[v]
            weight = self.G[u][v]['weight']
            
            x = [pos_u[0], pos_v[0]]
            y = [pos_u[1], pos_v[1]]
            z = [pos_u[2], pos_v[2]]
            
            # Highlight active connections (if post-synaptic neuron just spiked)
            u_data = neuron_map.get(u, {})
            v_data = neuron_map.get(v, {})
            
            if v_data.get('spiked', False):
                # Active connection - brighter and thicker
                self.ax.plot(x, y, z, color='#FF6600', alpha=0.8, 
                           linewidth=weight * 3, linestyle='--')
            else:
                # Inactive connection
                self.ax.plot(x, y, z, color='lightgray', alpha=0.2, 
                           linewidth=weight * 1)
        
        # Draw nodes
        for i, (pos, color, size) in enumerate(zip(node_positions, node_colors, node_sizes)):
            self.ax.scatter(pos[0], pos[1], pos[2], 
                          c=[color], s=size, alpha=0.9, 
                          edgecolors='black', linewidths=1.5)
        
        # Add labels for output neurons
        output_nodes = [n for n in self.G.nodes() if self.G.out_degree(n) == 0]
        for node_id in output_nodes:
            pos = self.pos_3d[node_id]
            neuron_data = neuron_map.get(node_id, {})
            spike_count = neuron_data.get('spike_count', 0)
            digit = output_nodes.index(node_id)
            self.ax.text(pos[0], pos[1], pos[2] + 0.2, 
                        f"{digit}\n({spike_count})", 
                        fontsize=8, ha='center', va='center')
        
        # Set labels and title
        self.ax.set_xlabel('X', fontsize=12)
        self.ax.set_ylabel('Y', fontsize=12)
        self.ax.set_zlabel('Z (Layer)', fontsize=12)
        self.ax.set_title(f'3D Spike Network Animation - Step {step_idx}/{len(self.time_steps)-1}', 
                         fontsize=14, fontweight='bold')
        
        # Set equal aspect ratio
        if node_positions:
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
    
    def animate(self, interval=200, loop=True, save_gif=None):
        """
        Create animated visualization
        
        Args:
            interval: Time between frames in milliseconds
            loop: Whether to loop the animation
            save_gif: If provided, save animation as GIF file
        """
        self.fig = plt.figure(figsize=(16, 12))
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        def update_frame(frame):
            step_idx = frame % len(self.time_steps) if loop else min(frame, len(self.time_steps) - 1)
            self._draw_frame(step_idx)
        
        ani = animation.FuncAnimation(self.fig, update_frame, 
                                     interval=interval,
                                     frames=len(self.time_steps) if not loop else None,
                                     repeat=loop,
                                     blit=False)
        
        if save_gif:
            print(f"Saving animation to {save_gif}...")
            ani.save(save_gif, writer='pillow', fps=1000/interval)
            print(f"Animation saved!")
        else:
            plt.tight_layout()
            plt.show()
        
        return ani


def main():
    parser = argparse.ArgumentParser(description='3D animated visualization of spiking network')
    parser.add_argument('base_file', help='Base JSON file (e.g., spike_animation_step0.json)')
    parser.add_argument('--interval', type=int, default=200,
                       help='Time between frames in milliseconds (default: 200)')
    parser.add_argument('--no-loop', action='store_true',
                       help='Don\'t loop the animation')
    parser.add_argument('--save', type=str, default=None,
                       help='Save animation as GIF file')
    
    args = parser.parse_args()
    
    try:
        animator = Spike3DAnimator(args.base_file)
        print(f"Starting 3D animation with {len(animator.time_steps)} time steps...")
        print("Close the window to stop.")
        animator.animate(interval=args.interval, loop=not args.no_loop, save_gif=args.save)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

