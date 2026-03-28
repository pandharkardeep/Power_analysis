import networkx as nx
import re

def parse_bench(filepath):
    """
    Parses a ISCAS89 .bench format file to extract inputs, outputs, 
    and build a logic circuit Directed Acyclic Graph (DAG).
    
    Args:
        filepath (str): Path to the .bench file.
        
    Returns:
        tuple: (G, inputs, outputs)
            - G: networkx.DiGraph representing the logic circuit
            - inputs: list of primary input node names
            - outputs: list of primary output node names
    """
    G = nx.DiGraph()
    inputs = []
    outputs = []
    
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: The file {filepath} was not found.")
        return None, [], []
        
    # Regular expressions for matching ISCAS89 elements
    re_input = re.compile(r'^\s*INPUT\s*\(\s*(.+?)\s*\)')
    re_output = re.compile(r'^\s*OUTPUT\s*\(\s*(.+?)\s*\)')
    re_gate = re.compile(r'^\s*(.+?)\s*=\s*([A-Za-z0-9]+)\s*\(\s*(.+?)\s*\)')
    
    for line in lines:
        line = line.strip()
        # Skip empty lines or comments
        if not line or line.startswith('#'):
            continue
            
        # Parse inputs
        inp_match = re_input.match(line)
        if inp_match:
            node = inp_match.group(1)
            inputs.append(node)
            G.add_node(node, type='INPUT')
            continue
            
        # Parse outputs
        out_match = re_output.match(line)
        if out_match:
            node = out_match.group(1)
            outputs.append(node)
            # We defer assigning type='OUTPUT' because it's usually defined as a gate later 
            # (e.g. out_node = AND(a,b)) which will overwrite this type. 
            # We already track it in the `outputs` list.
            G.add_node(node)
            continue
            
        # Parse logic gates (e.g., G10 = NAND(G1, G2))
        gate_match = re_gate.match(line)
        if gate_match:
            out_node = gate_match.group(1)
            gate_type = gate_match.group(2).upper()
            in_nodes_str = gate_match.group(3)
            
            # Split inputs and strip whitespace
            in_nodes = [n.strip() for n in in_nodes_str.split(',')]
            
            # Add node and assign the gate's logic type
            G.add_node(out_node, type=gate_type)
            
            # Add connections from inputs to this output
            for in_node in in_nodes:
                G.add_edge(in_node, out_node)
                
    return G, inputs, outputs
