function density = rho(temperature, pressure, molar_mass)
% RHO Density of an ideal gas.
k = 1.38E-23; % [J/K] Boltzmann constant
N_A = 6.022E23; % [1/mol] Avogadro constant
R = k * N_A; % [J/K-mol] Ideal gas constant

density = molar_mass .* pressure ./ (R .* temperature);
end