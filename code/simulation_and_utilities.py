import numpy as np

def number_steps_in_queue_simulation(queue_length):
    curr_position = queue_length - 1
    steps = 0
    while curr_position != 0:
        new_position_for_first_element = np.random.randint(0, queue_length)
        if new_position_for_first_element >= curr_position:
            curr_position -= 1
        steps += 1
    
    return steps

def first_n_harmonic_numbers_generator(n):
    """Method for computing the first n harmonic numbers.
    """ 
    sum = 0
    yield sum  # The first harmonic number H_0 is 0
    for k in range(1, n):
        sum += 1/k
        yield sum

def euler_constant_approx(n):
    H_n = 0
    for k in range(1, n+1):
        H_n += 1/k
    return (H_n - np.log(n) - 1/(2*n) + 1/(12*n**2) - 1/(120*n**4) 
            + 1/(252*n**6))