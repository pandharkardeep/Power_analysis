import argparse
import os
import sys

# Ensure src modules can be imported
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from netlist_parser import parse_bench
from power_estimator import calculate_probabilities, estimate_power
from visualize import plot_power_distribution

def main():
    parser = argparse.ArgumentParser(description='Estimate switching power from an ISCAS89 .bench netlist.')
    parser.add_argument('netlist', type=str, help='Path to the .bench netlist file')
    parser.add_argument('--vdd', type=float, default=1.0, help='Operating voltage in Volts (default: 1.0)')
    parser.add_argument('--freq', type=float, default=1e9, help='Clock frequency in Hz (default: 1e9)')
    parser.add_argument('--cap', type=float, default=1.0, help='Load capacitance per gate in fF (default: 1.0)')
    parser.add_argument('--save-plot', type=str, help='Optional path to save the plot image', default=None)
    
    args = parser.parse_args()
    
    print(f"Parsing netlist: {args.netlist}")
    G, inputs, outputs = parse_bench(args.netlist)
    
    if G is None:
        print("Failed to parse the circuit.")
        return
        
    print(f"Circuit parsed: {len(G.nodes)} nodes, {len(G.edges)} edges.")
    print(f"Inputs: {inputs}")
    print(f"Outputs: {outputs}")
    
    print("\nCalculating signal probabilities...")
    try:
        probabilities = calculate_probabilities(G, inputs)
    except Exception as e:
        print(f"Error computing probabilities (check for combinational loops): {e}")
        return
        
    print(f"Estimating dynamic power (Vdd={args.vdd}V, Freq={args.freq/1e9}GHz, C={args.cap}fF)...")
    total_power, power_dict = estimate_power(G, probabilities, vdd=args.vdd, freq_hz=args.freq, c_load_fF=args.cap)
    
    print("\n=== Power Estimation Results ===")
    for node, p_uw in power_dict.items():
        print(f"Node '{node:4s}': P_prob={probabilities.get(node, 0.0):.4f}, Power={p_uw:.4f} uW")
        
    print(f"---------------------------------")
    print(f"Total Circuit Dynamic Power: {total_power:.4f} uW")
    
    print("\nGenerating visualization...")
    plot_power_distribution(power_dict, filepath=args.save_plot)

if __name__ == '__main__':
    main()
