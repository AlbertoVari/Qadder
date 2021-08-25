# Importing standard Qiskit libraries and configuring account
from qiskit import QuantumCircuit, execute, Aer, IBMQ, QuantumRegister, ClassicalRegister
from qiskit.compiler import transpile, assemble
from qiskit.tools.jupyter import *
from qiskit.visualization import *
from numpy import pi
import json

# Loading your IBM Q account(s)
IBMQ.load_account()
provider = IBMQ.load_account()

print(provider.backends())
# exit()
backend = provider.get_backend('ibmq_bogota')

status = backend.status()
is_operational = status.operational
jobs_in_queue = status.pending_jobs

print(is_operational,jobs_in_queue)

q0 = input ("Insert Q0 -> ")
q1 = input ("Insert Q1 -> ")
q0 = int(q0)
q1 = int(q1)

qreg_q = QuantumRegister(4, 'q')
creg_c = ClassicalRegister(4, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)

if q0 == 1 :
    circuit.x(qreg_q[0])

if q1 == 1 :
    circuit.x(qreg_q[1])


circuit.ccx(qreg_q[0], qreg_q[1], qreg_q[3])
circuit.cx(qreg_q[0], qreg_q[1])
circuit.ccx(qreg_q[1], qreg_q[2], qreg_q[3])
circuit.cx(qreg_q[1], qreg_q[2])
circuit.cx(qreg_q[0], qreg_q[1])
circuit.measure(qreg_q[0], creg_c[0])
circuit.measure(qreg_q[1], creg_c[1])
circuit.measure(qreg_q[2], creg_c[2])
circuit.measure(qreg_q[3], creg_c[3])

num_shots = 1000

job = execute(circuit, backend, shots=num_shots)

result = job.result()

counts = result.get_counts(circuit)
rescounts = json.dumps(counts)

print("Result : ",result)
print("Counts : ",counts)

max_value = max(rescounts)
print("Result : CARRY SUM Q1 Q0 ")
print(rescounts.index(max_value),max_value)

f = open("Qadder_result.txt", "w")
f.write(rescounts)
f.close()
