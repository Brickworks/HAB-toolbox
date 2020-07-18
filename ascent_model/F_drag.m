function drag_force = F_drag(altitude, ascent_rate, lifting_mass, lift_gas)
%F_DRAG Summary of this function goes here
M = molar_mass(lift_gas);
V_gas = @(altitude, m_gas) (V(atmo_temp(altitude), atmo_pres(altitude), m_gas, M));
rho_gas = @(altitude, m_gas) (rho(atmo_temp(altitude), atmo_pres(altitude), M));
A_balloon = @(altitude, m_gas) ((V_gas(altitude, m_gas) / (4/3 * pi())).^(1/3));
drag_force = Cd/2 .* rho_gas(altitude, lifting_mass) .* - (ascent_rate .^2) .* A_balloon(altitude, lifting_mass);
end

