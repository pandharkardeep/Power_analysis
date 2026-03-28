import networkx as nx

def calculate_probabilities(G, inputs):
    """
    Traverses the circuit DAG topologically to calculate signal probabilities.
    Assumes standard temporal/spatial independence model.
    """
    prob = {}
    
    # Initialize primary inputs with 0.5 probability (50% duty cycle)
    for node in inputs:
        prob[node] = 0.5
        
    # Process nodes in topological order
    for node in nx.topological_sort(G):
        if node in inputs:
            continue
            
        gate_type = G.nodes[node].get('type', 'BUFF')
        preds = list(G.predecessors(node))
        
        # If no predecessors and not in inputs, default to 0 (shouldn't happen in valid DAG)
        if not preds:
            prob[node] = 0.0
            continue
            
        if gate_type == 'NOT':
            prob[node] = 1.0 - prob[preds[0]]
        elif gate_type == 'BUFF' or gate_type == 'BUF':
            prob[node] = prob[preds[0]]
        elif gate_type == 'AND':
            p = 1.0
            for pred in preds:
                p *= prob[pred]
            prob[node] = p
        elif gate_type == 'NAND':
            p = 1.0
            for pred in preds:
                p *= prob[pred]
            prob[node] = 1.0 - p
        elif gate_type == 'OR':
            p_inv = 1.0
            for pred in preds:
                p_inv *= (1.0 - prob[pred])
            prob[node] = 1.0 - p_inv
        elif gate_type == 'NOR':
            p_inv = 1.0
            for pred in preds:
                p_inv *= (1.0 - prob[pred])
            prob[node] = p_inv
        elif gate_type == 'XOR':
            # Simplified 2-input XOR
            p1 = prob[preds[0]]
            p2 = prob[preds[1]] if len(preds) > 1 else 0.0
            prob[node] = p1*(1.0-p2) + p2*(1.0-p1)
        elif gate_type == 'XNOR':
            p1 = prob[preds[0]]
            p2 = prob[preds[1]] if len(preds) > 1 else 0.0
            prob[node] = p1*p2 + (1.0-p1)*(1.0-p2)
        else:
            # Default fallback for unknown types
            prob[node] = prob[preds[0]]
            
    return prob

def estimate_power(G, probabilities, vdd=1.0, freq_hz=1e9, c_load_fF=1.0):
    """
    Calculates dynamic power for each node based on signal probability.
    P_dyn = 0.5 * C * V^2 * f * alpha
    alpha = 2 * p * (1-p)
    
    Args:
        G: networkx.DiGraph
        probabilities: dict of node signal probabilities
        vdd: Operating voltage in Volts
        freq_hz: Clock frequency in Hertz
        c_load_fF: Load capacitance per gate in femtoFarads
        
    Returns:
        tuple: (total_power_uW, power_dict_uW)
    """
    power_dict = {}
    total_power = 0.0
    
    # Convert fF to Farads for standard watts
    c_load_F = c_load_fF * 1e-15
    
    for node, p in probabilities.items():
        # Toggle rate alpha
        alpha = 2.0 * p * (1.0 - p)
        
        # P = 0.5 * C * V^2 * f * alpha
        power_watts = 0.5 * c_load_F * (vdd ** 2) * freq_hz * alpha
        
        # Convert to microwatts (uW)
        power_uw = power_watts * 1e6
        power_dict[node] = power_uw
        
        # We accumulate power for all elements in the DAG
        total_power += power_uw
        
    return total_power, power_dict
