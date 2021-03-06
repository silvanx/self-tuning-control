import pickle

import controller as ctrl
import simulation as sim

if __name__ == '__main__':
    steady_state_pad = 1000

    constants = sim.constants_nevado_holgado_healthy
    constants[5] = -0.9
    constants[16] = 10
    constants[17] = 20
    constants[18] = 50

    simulation_time = 3000
    dt = 0.01

    print('Simulations')
    sigma = 0.01
    mi = (750, 10, 50)
    it = [20, 20, 0]
    tau_theta = 5
    prop_theta = 25

    p_controller = ctrl.ProportionalController(gain=prop_theta, dt=dt)
    a_controller = ctrl.AdaptiveController(sigma=sigma, tau_theta=tau_theta, dt=dt)
    history_adaptive = sim.single_simulation(constants, simulation_time, dt, control_mechanism=a_controller,
                                             control_start=200, init_state=it, mid_increase=mi,
                                             steady_state_pad=steady_state_pad)
    history_proportional = sim.single_simulation(constants, simulation_time, dt, control_mechanism=p_controller,
                                                 control_start=200, init_state=prop_theta, mid_increase=mi,
                                                 steady_state_pad=steady_state_pad)

    print('Saving simulation results')
    with open('simulation_results/results_figure_4', 'wb+') as f:
        pickle.dump({
            'proportional': history_proportional[int(steady_state_pad / dt):],
            'adaptive': history_adaptive[int(steady_state_pad / dt):],
            'constants': constants,
            'sigma': sigma,
            'mid_increase': mi,
            'initial_theta': it,
            'simulation_time': simulation_time,
            'dt': dt,
            'tau_theta': tau_theta,
            'prop_theta': prop_theta
        }, f)
