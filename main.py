# Textbook used: https://learn.qiskit.org/course/introduction/the-atoms-of-computation

import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.providers.aer import AerSimulator

sim = AerSimulator()


# To do addition we need an XOR gate and an AND gate in classical logic
# In quantum computers, these are managed by a controlled-NOT gate (CNOT/CX) and a Toffoli gate respectively (CCX)
# The right bit (Digit) is handled by the CNOT gate and the left (Carry) by the Toffoli gate


def q_add(q0, q1, q2): # n1[i],n2[i],carry
    test_circuit = QuantumCircuit(5, 2)
    if q0 == 1:
        test_circuit.x(0)
    if q1 == 1:
        test_circuit.x(1)
    if q2 == 1:
        test_circuit.x(2)

    #Digit
    test_circuit.cx(0, 3)  # sets q3 to the value of q0
    test_circuit.cx(1, 3)  # CNOT controlled by q1 targeting q3 (i.e. q0)
    test_circuit.cx(2, 3)  # CNOT controlled by q2 targeting q3 (classically -> q3=q0⊕q1⊕q2)
    
    # Carry
    test_circuit.ccx(0, 1, 4)  # Toffoli controlled by 0,1 targeting 4
    test_circuit.cx(0,1)
    test_circuit.ccx(1,2,4)
    
    test_circuit.measure([3, 4], [0, 1])  # measures q3 and q4 and assigns them to bit0 and bit1 respectively

    result = sim.run(test_circuit).result()
    return result.get_counts() # returns {00||01||11 : 1024}

def q_add_iterable(counts):
    try:
        counts['00']
        return '00'
    except KeyError:
        try:
            counts['01']
            return '01'
        except KeyError:
            try:
                counts['10']
                return '10'
            except KeyError:    
                try:
                    counts['11']
                    return '11'
                except KeyError:
                    return 0

def full_add(n1,n2):
    if len(n1)<len(n2):
        n1 = "0"*(len(n2)-len(n1)) + n1
    if len(n2)<len(n1):
        n2 = "0"*(len(n1)-len(n2)) + n2
    carry = 0
    answer = ""


    for i in range(len(n1)):
        addition = q_add_iterable(q_add( int(n1[-1-i]) , int(n2[-1-i]) , carry ))
        digit = addition[1]
        carry = int(addition[0])
        answer = digit + answer

    return answer

n1 = "1101001000110"
n2 = "10010001101"

print(full_add("1101001000110","10010001101"))

