from qiskit import QuantumCircuit
from qiskit.providers.aer import AerSimulator

sim = AerSimulator()

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
    return result.get_counts() # returns {00||01||10||11 : 1024}

def q_add_iterable(counts): # checks what values were returned
    options = ['00','01','10','11']
    for o in options:
        try:
            counts[o]
            x=o
            break
        except KeyError:
            x=0
    return x
        

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

a = "1101001000110"
b = "10010001101"

print(full_add("1101001000110","10010001101")) # returns 1111011010011

