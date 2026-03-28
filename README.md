# Power Analysis Tool

A Python-based Electronic Design Automation (EDA) tool that estimates the switching (dynamic) power of a digital logic circuit. 

The tool parses standard ISCAS89 `.bench` netlists, evaluates signal probabilities through a Directed Acyclic Graph (DAG) representation of the circuit, computes toggle rates, and visualizes the power distribution per logic gate using `matplotlib`.

## Features
- **Netlist Parsing**: Supports standard ISCAS89 `.bench` format.
- **Power Estimation**: Computes temporal properties and signal probabilities ($P$) to deduce the toggle rate ($\alpha = 2P(1-P)$).
- **Dynamic Power Model**: Calculates switching power using $P_{dyn} = \frac{1}{2} C_{load} V_{dd}^2 f_{clk} \alpha$.
- **Visualization**: Generates a bar chart detailing power consumption per gate.

## Dependencies
- Python 3.7+
- `networkx` (for DAG generation and topological sorting)
- `matplotlib` (for visual plotting)

## Installation
Clone the repository and install the required dependencies:
```bash
git clone https://github.com/pandharkardeep/Power_analysis.git
cd Power_analysis
pip install -r requirements.txt
```

## Usage
Run the analysis via the CLI `main.py` entry point:
```bash
python main.py example.bench
```

### CLI Arguments
| Argument | Description | Default |
| -------- | ----------- | ------- |
| `netlist` | Path to the `.bench` format netlist. | **Required** |
| `--vdd` | Operating voltage in Volts. | `1.0` |
| `--freq` | Clock frequency in Hertz. | `1e9` (1 GHz) |
| `--cap` | Load capacitance per gate in femtoFarads. | `1.0` |
| `--save-plot` | Optional file path to save the generated graph. | `None` (Opens interactive UI) |

**Example:**
```bash
python main.py example.bench --vdd 1.2 --freq 2e9 --cap 1.5 --save-plot power_plot.png
```

## Project Structure
```text
Power_Analysis/
├── main.py                 # CLI Orchestrator
├── requirements.txt        # Dependencies
├── example.bench           # Sample benchmark circuit
├── src/
│   ├── netlist_parser.py   # Parses .bench format into a NetworkX DAG
│   ├── power_estimator.py  # Computes probabilities, toggle rates, and power
│   └── visualize.py        # Matplotlib visualization generation
```
