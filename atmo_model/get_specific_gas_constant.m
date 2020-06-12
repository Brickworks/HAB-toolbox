function R_specific = get_specific_gas_constant(molar_mass)
% GET_SPECIFIC_GAS_CONSTANT  Get the specific ideal gas constant for a
% given substance.
k = 1.38E-23; % [J/K] Boltzmann constant
N_A = 6.022E23; % [1/mol] Avogadro constant
R = k * N_A; % [J/K-mol] Ideal gas constant
R_specific = R / molar_mass; % [J/kg-K]
end