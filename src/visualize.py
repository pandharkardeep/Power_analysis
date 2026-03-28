import matplotlib.pyplot as plt

def plot_power_distribution(power_dict, filepath=None):
    """
    Plots a bar chart of the power distribution across logical nodes.
    
    Args:
        power_dict (dict): Map of node strings to their power values in uW.
        filepath (str, optional): If provided, saves the plot to this file instead of showing it.
    """
    # Sort for better visualization
    sorted_items = sorted(power_dict.items(), key=lambda x: x[1], reverse=True)
    nodes = [item[0] for item in sorted_items]
    powers = [item[1] for item in sorted_items]
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(nodes, powers, color='skyblue', edgecolor='black')
    
    plt.xlabel('Logic Node (Gate / Input)')
    plt.ylabel('Dynamic Power (\u03bcW)')
    plt.title('Estimated Switching Power per Node')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Add values on top of bars
    for bar, power in zip(bars, powers):
        yval = bar.get_height()
        max_height = max(powers) if powers else 1.0
        plt.text(bar.get_x() + bar.get_width()/2, yval + (max_height*0.01), 
                 f'{power:.2f}', ha='center', va='bottom', fontsize=8, rotation=90)
                 
    plt.tight_layout()
    
    if filepath:
        plt.savefig(filepath, dpi=300)
        print(f"Plot saved to {filepath}")
    else:
        plt.show()
