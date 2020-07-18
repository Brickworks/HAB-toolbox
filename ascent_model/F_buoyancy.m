function buoyancy_force = F_buoyancy(altitude, lifting_mass, lift_gas)
%F_BUOYANCY Force (N) due to air displaced by lifting gas in the balloon.
%   altitude (m)        altitude above sea level
%   lifting_mass (kg)   mass of lifting gas in the balloon
%   lift_gasyavi172317
M = molar_mass(lift_gas);
V_gas = @(altitude, m_gas) (V(atmo_temp(altitude), atmo_pres(altitude), m_gas, M));
rho_gas = @(altitude, m_gas) (rho(atmo_temp(altitude), atmo_pres(altitude), M));
A_balloon = @(altitude, m_gas) ((V_gas(altitude, m_gas) / (4/3 * pi())).^(1/3));

% Next we sum the forces acting on the balloon-payload system.
buoyancy_force =V_gas(altitude, lifting_mass) .* (rho_gas(altitude, lifting_mass) - atmo_density(altitude)) .* -g(altitude);
end