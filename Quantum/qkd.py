import random
import hashlib
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

class BB84:
    def __init__(self, key_length=29):
        self.key_length = key_length
        self.bases = ['+', '×']
        self.alice_bits = []

    def generate_qubits(self):
        self.alice_bits = [random.randint(0, 1) for _ in range(self.key_length)]
        alice_bases = [random.choice(self.bases) for _ in range(self.key_length)]
        quantum_bits, qc = self.generate_quantum_bits(self.key_length)
        self.analyze_circuit(qc)  # Call analyze_circuit here
        return quantum_bits, alice_bases

    def generate_quantum_bits(self, num_bits):
        qc = QuantumCircuit(num_bits, num_bits)
        for i in range(num_bits):
            qc.h(i)
        qc.measure(range(num_bits), range(num_bits))
        simulator = AerSimulator()
        compiled_circuit = transpile(qc, simulator)
        sim_result = simulator.run(compiled_circuit).result()
        counts = sim_result.get_counts()
        measured_bits = list(counts.keys())[0]
        return [int(bit) for bit in measured_bits], qc  # Return the circuit as well

    def measure_qubits(self, alice_bases):
        bob_bases = [random.choice(self.bases) for _ in range(self.key_length)]
        return bob_bases

    def sift_keys(self, alice_bases, bob_bases):
        return [i for i in range(len(alice_bases)) if alice_bases[i] == bob_bases[i]]

    def generate_final_key(self, sifted_indices):
        sifted_bits = [self.alice_bits[i] for i in sifted_indices]
        sifted_bits = [bit % 256 for bit in sifted_bits]
        final_key = hashlib.sha256(bytes(sifted_bits)).digest()
        return final_key

    def analyze_circuit(self, qc):
        depth = qc.depth()
        single_qubit_gates = ['h', 'x', 'y', 'z', 's', 'sdg', 't', 'tdg', 'id']
        two_qubit_gates = ['cx', 'cz', 'swap', 'ccx', 'cswap']
        sqg_count = {gate: 0 for gate in single_qubit_gates}
        tqg_count = {gate: 0 for gate in two_qubit_gates}
        
        for gate in qc.data:
            gate_name = gate[0].name
            if gate_name in sqg_count:
                sqg_count[gate_name] += 1
            elif gate_name in tqg_count:
                tqg_count[gate_name] += 1
        
        print("Circuit Depth:", depth)
        print("Number of Single Qubit Gates:", sum(sqg_count.values()))
        print("Number of Two Qubit Gates:", sum(tqg_count.values()))
        print("\nGate Counts:")
        print("{:<10} {:<10}".format("Gate Type", "Count"))
        print("-" * 20)
        
        for gate, count in sqg_count.items():
            print("{:<10} {:<10}".format(gate, count))
        
        for gate, count in tqg_count.items():
            print("{:<10} {:<10}".format(gate, count))