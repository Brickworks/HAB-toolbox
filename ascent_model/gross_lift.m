function gross_lift_kg = gross_lift(altitude, helium_mass)
%GROSS_LIFT Get the mass component of net buoyancy force from a given
%HELIUM_MASS (kg) at a given ALTITUDE (m).
molar_mass_helium = 0.004002602; % [kg/mol]
[T_a, P_a, rho_a] = atmo_model(altitude) % [K], [Pa], [kg/m^3]
volume = V(T_a, P_a, helium_mass, molar_mass_helium) % [m^3]
density_difference = rho_a - rho(T_a, P_a, molar_mass_helium) % 
gross_lift_kg = volume .* density_difference;
end

