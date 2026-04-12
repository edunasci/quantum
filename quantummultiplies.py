
def mult_out_N(N, wires_a, wires_b, wires_res, wires_aux):
    """
    Perform an outplace modular multiplication of quantum registers 'wires_a' and 'wires_b',
    with the result stored in 'wires_res'. Uses auxiliary wires 'wires_aux'.

    :param N: The modulus.
    :param wires_a: Quantum wires for the first input.
    :param wires_b: Quantum wires for the second input.
    :param wires_res: Quantum wires to store the result.
    :param wires_aux: Auxiliary quantum wires.
    """
    # Join the auxiliary wires to the result wires
    new_wires_res = [wires_aux[0]] + wires_res
    
    # Set the Fourier basis
    qml.QFT(wires=new_wires_res)
    
    for i in range(len(wires_a)):
        new_i = len(wires_a) - i - 1
        for j in range(len(wires_b)):
            new_j = len(wires_b) - j - 1
            value = 2**(new_i + new_j) % N
            qml.ctrl(add_in_k_N, control=[wires_a[i], wires_b[j]])(value, N, new_wires_res, [wires_aux[1]], False)
    
    # Recover the basis
    qml.adjoint(qml.QFT)(wires=new_wires_res)

## Create the device
nWireCount = 11
dev = qml.device("default.qubit", wires=nWireCount, shots=1)

@qml.qnode(dev)
def circuit_mult_out_N(a, b, N, wires_a, wires_b, wires_res, wires_aux):
    qml.BasisEmbedding(a, wires=wires_a)
    qml.BasisEmbedding(b, wires=wires_b)
    mult_out_N(N, wires_a, wires_b, wires_res, wires_aux)
    return qml.sample()

## Set wires
wires_a = list(range(0, 3))
wires_b = list(range(3, 6))
wires_res = list(range(6, 9))
wires_aux = [9, 10]

# Example
N = 7  # Input value between [0, 7]
a = 3  # Input value between [0, N-1]
b = 5  # Input value between [0, N-1]
vOutput = circuit_mult_out_N(a, b, N, wires_a, wires_b, wires_res, wires_aux)
print(a, "*", b, "mod", N, "=", binary_to_integer(vOutput[wires_res]))


def Exp_a_N(a, N, wires_x, wires_res, wires_support, wires_aux):
    """
    Exponential operator for quantum registers 'wires_x' with the result stored in 'wires_res'.
    
    :param a: The base of the exponential.
    :param N: The modulus.
    :param wires_x: Quantum wires for the input.
    :param wires_res: Quantum wires to store the result.
    :param wires_support: Quantum wires for intermediate calculations.
    :param wires_aux: Auxiliary quantum wires.
    """
    # Set wires_res -> |1>
    qml.PauliX(wires=wires_res[len(wires_res) - 1])
    
    # Apply the Mult_in
    n = len(wires_x)
    for i in range(n):
        value = a**(2**(n-i-1))
        qml.ctrl(mult_in_k_N, control=[wires_x[i]])(value, N, wires_res, wires_support, wires_aux)

## Create the device
nWireCount = 11
dev = qml.device("default.qubit", wires=nWireCount, shots=1)

@qml.qnode(dev)
def circuit_exp_a_N(x, a, N, wires_x, wires_res, wires_support, wires_aux):
    qml.BasisEmbedding(x, wires=wires_x)
    Exp_a_N(a, N, wires_x, wires_res, wires_support, wires_aux)
    return qml.sample()

## Set wires
wires_x = list(range(0, 3))
wires_res = list(range(3, 6))
wires_support = list(range(6, 9))
wires_aux = [9, 10]

# Example
N = 7  # Input value between [0, 7]
x = 3  # Input value between [0, N-1]
a = 2  # Input value between [0, N-1]
vOutput = circuit_exp_a_N(x, a, N, wires_x, wires_res, wires_support, wires_aux)
print(a, "**", x, "mod", N, "=", binary_to_integer(vOutput[wires_res]))
print("The expected result is", a**x % N)
