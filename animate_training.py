#!/usr/bin/env python3
"""
Animated visualization of training process showing network learning all digits
"""

import json
import sys
import argparse
import numpy as np
import os
import re
import glob

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


class TrainingAnimator:
    def __init__(self, base_filename):
        """Initialize training animator"""
        self.base_filename = base_filename
        self.time_steps = []
        self.G = None
        self.pos_3d = None
        self.fig = None
        self.ax = None
        self.frame_info = []  # Store info about each frame
        
        self._load_training_frames()
        self._build_graph()
        self._calculate_3d_layout()
    
    def _load_training_frames(self):
        """Load all training frames in order"""
        # Extract pattern from base filename
        # Format: training_epoch0_test_digit0_step0.json
        match = re.search(r'training_epoch(\d+)_test_digit(\d+)_step(\d+)\.json', self.base_filename)
        if not match:
            # Try alternative pattern
            match = re.search(r'training_epoch(\d+)_digit(\d+)_step(\d+)\.json', self.base_filename)
        
        if match:
            base_pattern = "training_epoch{}_test_digit{}_step{}.json"
        else:
            # Try to find any training files in data/json first, then current directory
            training_files = glob.glob("data/json/training_epoch*_test_digit*_step*.json")
            if not training_files:
                training_files = glob.glob("training_epoch*_test_digit*_step*.json")
            if training_files:
                self.base_filename = training_files[0]
                match = re.search(r'training_epoch(\d+)_test_digit(\d+)_step(\d+)\.json', self.base_filename)
        
        if not match:
            raise ValueError(f"Could not parse training file pattern from: {self.base_filename}")
        
        # Find all training files
        dir_path = os.path.dirname(self.base_filename) if os.path.dirname(self.base_filename) else '.'
        if dir_path == '.':
            # Try data/json first
            training_files = glob.glob("data/json/training_epoch*_test_digit*_step*.json")
            if not training_files:
                training_files = glob.glob("training_epoch*_test_digit*_step*.json")
        else:
            training_files = glob.glob(os.path.join(dir_path, "training_epoch*_test_digit*_step*.json"))
        
        # Parse and sort files
        parsed_files = []
        for f in training_files:
            match = re.search(r'training_epoch(\d+)_test_digit(\d+)_step(\d+)\.json', f)
            if match:
                epoch = int(match.group(1))
                digit = int(match.group(2))
                step = int(match.group(3))
                parsed_files.append((epoch, digit, step, f))
        
        # Sort by epoch, then digit, then step
        parsed_files.sort(key=lambda x: (x[0], x[1], x[2]))
        
        if not parsed_files:
            raise ValueError("No training frame files found")
        
        # Load all frames
        for epoch, digit, step, filepath in parsed_files:
            with open(filepath, 'r') as f:
                data = json.load(f)
                self.time_steps.append(data)
                self.frame_info.append({
                    'epoch': epoch,
                    'digit': digit,
                    'step': step,
                    'file': filepath
                })
        
        print(f"Loaded {len(self.time_steps)} training frames")
        print(f"Epochs: {min(f['epoch'] for f in self.frame_info)} to {max(f['epoch'] for f in self.frame_info)}")
        print(f"Digits: 0-9")
    
    def _build_graph(self):
        """Build networkx graph from first frame"""
        self.G = nx.DiGraph()
        data = self.time_steps[0]
        
        for neuron in data['neurons']:
            self.G.add_node(neuron['id'])
        
        for neuron in data['neurons']:
            for conn in neuron['connections']:
                self.G.add_edge(neuron['id'], conn['target'], weight=conn['weight'])
    
    def _calculate_3d_layout(self):
        """Calculate 3D positions (layered layout)"""
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
    
    def _get_neuron_data(self, frame_idx):
        """Get neuron data for a specific frame"""
        data = self.time_steps[frame_idx]
        neuron_map = {n['id']: n for n in data['neurons']}
        return neuron_map
    
    def _draw_frame(self, frame_idx):
        """Draw a single frame"""
        self.ax.clear()
        
        neuron_map = self._get_neuron_data(frame_idx)
        info = self.frame_info[frame_idx]
        
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
            
            if spiked:
                node_colors.append('#FF0000')
                node_sizes.append(300)
            else:
                intensity = min(1.0, max(0.0, potential))
                node_colors.append(plt.cm.viridis(intensity))
                node_sizes.append(100 + intensity * 100)
        
        # Draw edges
        for u, v in self.G.edges():
            pos_u = self.pos_3d[u]
            pos_v = self.pos_3d[v]
            weight = self.G[u][v]['weight']
            
            x = [pos_u[0], pos_v[0]]
            y = [pos_u[1], pos_v[1]]
            z = [pos_u[2], pos_v[2]]
            
            u_data = neuron_map.get(u, {})
            v_data = neuron_map.get(v, {})
            
            if v_data.get('spiked', False):
                self.ax.plot(x, y, z, color='#FF6600', alpha=0.8, 
                           linewidth=weight * 3, linestyle='--')
            else:
                self.ax.plot(x, y, z, color='lightgray', alpha=0.2, 
                           linewidth=weight * 1)
        
        # Draw nodes
        for i, (pos, color, size) in enumerate(zip(node_positions, node_colors, node_sizes)):
            self.ax.scatter(pos[0], pos[1], pos[2], 
                          c=[color], s=size, alpha=0.9, 
                          edgecolors='black', linewidths=1.5)
        
        # Add labels for output neurons with spike counts
        output_nodes = [n for n in self.G.nodes() if self.G.out_degree(n) == 0]
        for node_id in output_nodes:
            pos = self.pos_3d[node_id]
            neuron_data = neuron_map.get(node_id, {})
            spike_count = neuron_data.get('spike_count', 0)
            digit = output_nodes.index(node_id)
            
            # Highlight if this is the current test digit
            if digit == info['digit']:
                self.ax.text(pos[0], pos[1], pos[2] + 0.3, 
                            f"→{digit}←\n({spike_count})", 
                            fontsize=10, ha='center', va='center',
                            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
            else:
                self.ax.text(pos[0], pos[1], pos[2] + 0.2, 
                            f"{digit}\n({spike_count})", 
                            fontsize=8, ha='center', va='center')
        
        # Set labels and title
        self.ax.set_xlabel('X', fontsize=12)
        self.ax.set_ylabel('Y', fontsize=12)
        self.ax.set_zlabel('Z (Layer)', fontsize=12)
        
        title = f"Training Animation - Epoch {info['epoch']}, Testing Digit {info['digit']}, Step {info['step']}"
        self.ax.set_title(title, fontsize=14, fontweight='bold')
        
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
        """Create animated visualization"""
        self.fig = plt.figure(figsize=(16, 12))
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        def update_frame(frame):
            frame_idx = frame % len(self.time_steps) if loop else min(frame, len(self.time_steps) - 1)
            self._draw_frame(frame_idx)
        
        ani = animation.FuncAnimation(self.fig, update_frame, 
                                     interval=interval,
                                     frames=len(self.time_steps) if not loop else None,
                                     repeat=loop,
                                     blit=False,
                                     cache_frame_data=False)
        
        if save_gif:
            print(f"Saving animation to {save_gif}...")
            ani.save(save_gif, writer='pillow', fps=1000/interval)
            print(f"Animation saved!")
        else:
            plt.tight_layout()
            plt.show()
        
        return ani


def main():
    parser = argparse.ArgumentParser(description='Animated visualization of training process')
    parser.add_argument('base_file', nargs='?', 
                       help='Base training file (e.g., training_epoch0_test_digit0_step0.json)')
    parser.add_argument('--interval', type=int, default=300,
                       help='Time between frames in milliseconds (default: 300)')
    parser.add_argument('--no-loop', action='store_true',
                       help='Don\'t loop the animation')
    parser.add_argument('--save', type=str, default=None,
                       help='Save animation as GIF file')
    
    args = parser.parse_args()
    
    if not args.base_file:
        # Try to find training files automatically (check data/json first)
        training_files = glob.glob("data/json/training_epoch*_test_digit*_step*.json")
        if not training_files:
            training_files = glob.glob("training_epoch*_test_digit*_step*.json")
        if training_files:
            args.base_file = training_files[0]
            print(f"Auto-detected training file: {args.base_file}")
        else:
            print("Usage: python animate_training.py <training_file> [options]")
            print("\nOr run train_with_animation first to generate training frames")
            print("Files will be saved to data/json/ directory")
            sys.exit(1)
    
    try:
        animator = TrainingAnimator(args.base_file)
        print(f"Starting training animation with {len(animator.time_steps)} frames...")
        print("Close the window to stop.")
        animator.animate(interval=args.interval, loop=not args.no_loop, save_gif=args.save)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

