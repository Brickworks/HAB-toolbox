function mass = mass_from_volume(volume, temperature, pressure, molar_mass)
%MASS_FROM_VOLUME Mass of an ideal gas with a given VOLUME, DENSITY, and
%MOLAR_MASS.
k = 1.38E-23; % [J/K] Boltzmann constant
N_A = 6.022E23; % [1/mol] Avogadro constant
R = k * N_A; % [J/K-mol] Ideal gas constant

mass = volume .* molar_mass ./ R .* pressure ./ temperature; 
end

