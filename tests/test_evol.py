import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
import numpy as np
import astropy.units as u
from hztrak.evol_calc import calc

@pytest.fixture
def model():
    return calc()

def test_alpha_beta_gamma_low_mass(model):
    alpha, beta, gamma = model.alpha_beta_gamma(0.3 * u.Msun)
    assert alpha == 2.3
    assert beta == 0.1
    assert gamma == 0.05

def test_alpha_beta_gamma_mid_mass(model):
    alpha, beta, gamma = model.alpha_beta_gamma(1.0 * u.Msun)
    assert alpha == 4
    assert beta == 0.4
    assert gamma == 0.1

def test_luminosity_evolve(model):
    L_0 = 1.0 * u.Lsun
    beta = 0.4
    t_f = 10 * u.Gyr
    t = 5 * u.Gyr
    alpha = 4
    L_f = model.luminosity_evolve(L_0, beta, t_f, t, alpha)
    assert L_f.unit == u.Lsun
    assert L_f > L_0  # luminosity should increase

def test_radius_evolve(model):
    R_0 = 1.0 * u.Rsun
    gamma = 0.1
    t_f = 10 * u.Gyr
    t = 5 * u.Gyr
    alpha = 4
    R_f = model.radius_evolve(R_0, gamma, t_f, t, alpha)
    assert R_f.unit == u.Rsun
    assert R_f > R_0

def test_temp_evolve(model):
    T_0 = 5800 * u.K
    L_0 = 1.0 * u.Lsun
    L_f = 1.2 * u.Lsun
    R_0 = 1.0 * u.Rsun
    R_f = 1.1 * u.Rsun
    T_f = model.temp_evolve(T_0, L_f, L_0, R_f, R_0)
    assert T_f.unit == u.K
    assert T_f < T_0  # radius increased more than luminosity -> cooler star

def test_evolve_star_table_output(model):
    L_0 = 1.0 * u.Lsun
    R_0 = 1.0 * u.Rsun
    T_0 = 5800 * u.K
    mass = 1.0 * u.Msun
    age = 10 * u.Gyr
    steps = 5

    result_table = model.evolve_star(L_0, R_0, T_0, mass, t_f=age, steps=steps)

    assert len(result_table) == steps
    assert 'time_yr' in result_table.colnames
    assert result_table['luminosity_Lsun'].unit == u.Lsun
    assert result_table['radius_Rsun'].unit == u.Rsun
    assert result_table['temperature_K'].unit == u.K
