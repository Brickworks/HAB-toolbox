function volume = V(temperature, pressure, mass, molar_mass)
% V Volume of an ideal gas.
k = 1.38E-23; % [J/K] Boltzmann constant
N_A = 6.022E23; % [1/mol] Avogadro constant
R = k * N_A; % [J/K-mol] Ideal gas constant

volume = (mass ./ molar_mass) .* R .* temperature ./ pressure;
end