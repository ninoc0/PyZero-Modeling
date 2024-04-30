# Input the file directory of your node text file.
input_file_path = '/home/nico/my_code/nodes/commonpath.txt'


# Model Libraries
import numpy as np
from zero import Circuit
from zero.analysis import AcSignalAnalysis
from zero.data import Series, Response

# Data Libraries
import pandas as pd
import matplotlib.pyplot as plt

# Converting your node txt to PyZero format
def convert_text_to_circuit(file_path):
    formatted_circuit_lines = []
    
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('op'):
                parts = line.split()
                if len(parts) >= 6:
                    _, op_name, op_model, n1, n2, n3 = parts
                    formatted_circuit_lines.append(f'circuit.add_library_opamp(name="{op_name}", model="{op_model}", node1="{n1}", node2="{n2}", node3="{n3}")')
                else:
                    formatted_circuit_lines.append(f"Ignoring line: {line} (Invalid format for op-amp)")
            elif line.startswith(('r', 'c')):
                parts = line.split()
                if len(parts) >= 5:
                    elem_type, elem_name, elem_value, n1, n2 = parts
                    if elem_type == 'r':
                        formatted_circuit_lines.append(f'circuit.add_resistor(name="{elem_name}", value="{elem_value}", node1="{n1}", node2="{n2}")')
                    elif elem_type == 'c':
                        formatted_circuit_lines.append(f'circuit.add_capacitor(name="{elem_name}", value="{elem_value}", node1="{n1}", node2="{n2}")')
                else:
                    formatted_circuit_lines.append(f"Ignoring line: {line} (Invalid format for resistor/capacitor)")

    formatted_circuit = '\n'.join(formatted_circuit_lines)
    return formatted_circuit

def convert_text_to_freq(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('freq'):
                parts = line.split()
                if len(parts) == 4 and parts[0] == 'freq':
                    start_val = int(parts[1])
                    stop_val = int(parts[2])
                    interval = int(parts[3])
    return start_val, stop_val, interval

def convert_text_to_test(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('test'):
                parts = line.split()
                if len(parts) == 3 and parts[0] == 'test':
                    nin = (parts[1])
                    nout = (parts[2])
    return nin, nout

formatted_circuit = convert_text_to_circuit(input_file_path)
start_val, stop_val, interval = convert_text_to_freq(input_file_path)
nin, nout = convert_text_to_test(input_file_path)

# PyZero Code
circuit = Circuit()
frequencies = np.logspace(start_val, stop_val, interval)

exec(formatted_circuit)

## Analysis
analysis = AcSignalAnalysis(circuit=circuit)
solution = analysis.calculate(frequencies=frequencies, input_type="voltage", node=nin)

#res = solution.get_response(nin, nout)
#magres = res.db_magnitude
#phares = res.phase

#magnitude_z = np.array(magres)
#phase_z = np.array(phares)

## If you want to plot just PyZero
plot = solution.plot_responses(sink=nout)
plot.show()