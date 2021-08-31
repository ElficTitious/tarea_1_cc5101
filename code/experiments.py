import numpy as np
import matplotlib.pyplot as plt
from simulation_and_utilities import *
from scipy.optimize import curve_fit

if __name__ == "__main__":

    np.random.seed(42)
    
    numbers_for_computing = np.arange(1, 1_001)  # Sequence [1...1.000] for plotting

    # Now we generate the first 1.000 values of the sequence nH_n-1 
    # (theoretical prediction).
    harmonic_generator = first_n_harmonic_numbers_generator(numbers_for_computing[-1])
    tmp_theoretical_prediction_list = []
    for n in numbers_for_computing:
        H_prev = next(harmonic_generator)
        tmp_theoretical_prediction_list.append(n * H_prev)

    # for plotting and curve fitting we start from 10.
    numbers_to_plot = numbers_for_computing[10::]
    theoretical_prediction_arr = np.array(tmp_theoretical_prediction_list)[10::]

    # Now we generate the results obtained via the simulation we wrote in 
    # simulation_and_utilities.py (with the seed imposed here).
    experimental_results_arr = np.array([number_steps_in_queue_simulation(n)
                                         for n in numbers_to_plot])

    # Finally we plot
    plt.clf()
    plt.plot(numbers_to_plot, experimental_results_arr, 'r.', markersize=3,
             label="Resultados experimentales")
    plt.plot(numbers_to_plot, theoretical_prediction_arr, linewidth=2.5, 
             label="Predicción teórica ($nH_{n-1}$)")
    plt.legend()
    plt.xlabel("n (Número de elementos en la cola)")
    plt.ylabel("Número de pasos hasta\nprimer lugar de la cola")
    plt.tight_layout()
    plt.show()

    # Let's now try to fit a polynomial of degree 3 and a logarithmic curve to the 
    # experimental data

    def objective_poly(x, a, b, c, d):
        return a * x**3 + b * x**2 + c * x + d

    def objective_log(x, a, b):
        return a * x * np.log(x-1) + b * x

    params_log, _ = curve_fit(objective_log, numbers_to_plot, experimental_results_arr)
    params_poly, _ = curve_fit(objective_poly, numbers_to_plot, experimental_results_arr)

    print("Fitted logarithmic curve: f(x) = {0:.2f}*xln(x-1) + {1:.2f}*x".format(params_log[0], 
                                                                             params_log[1]))

    print("Fitted degree 3 polynomial is: f(x) = {0:.3e}*x^3 + {1:.3e}*x^2 + "
          "{2:.2f}*x + {3:.2f}".format(params_poly[0], params_poly[1],
                                      params_poly[2], params_poly[3]))
    
    
    fitted_log_curve_data_arr = objective_log(numbers_to_plot, params_log[0], params_log[1])
    fitted_poly_curve_data_arr = objective_poly(numbers_to_plot, params_poly[0], params_poly[1],
                                                params_poly[2], params_poly[3])


    # We now compute and plot the relative difference between the fitted curves
    # and the theoretical prediction nH_n-1.

    relative_difference_log_arr = np.abs((fitted_log_curve_data_arr
                                          - theoretical_prediction_arr)/numbers_to_plot)

    relative_difference_poly_arr = np.abs((fitted_poly_curve_data_arr
                                           - theoretical_prediction_arr)/numbers_to_plot)

    mean_error_log = np.mean(relative_difference_log_arr)
    mean_error_poly = np.mean(relative_difference_poly_arr)

    print("Mean absolute relative error between the theoretical predictions"
          " and the logarithmic fitted curve is {}".format(mean_error_log))
    print("Mean absolute relative error between the theoretical predictions"
          " and the fitted degree 3 polynomial is {}".format(mean_error_poly))


    plt.clf()
    plt.plot(numbers_to_plot, relative_difference_log_arr)
    plt.xlabel("n (Número de elementos en la cola)")
    plt.ylabel(r"$|\frac{F(n)_{log} - nH_{n-1}}{n}|$", fontsize=12)
    plt.tight_layout()
    plt.show()

    plt.clf()
    plt.plot(numbers_to_plot, relative_difference_poly_arr)
    plt.xlabel("n (Número de elementos en la cola)")
    plt.ylabel(r"$|\frac{F(n)_{poly} - nH_{n-1}}{n}|$", fontsize=12)
    plt.tight_layout()
    plt.show()

    print(euler_constant_approx(10))
