function g_h = g(altitude)
%G Gravitational acceleration at an ALTITUDE (m) above mean sea level
if nargin < 1 || isempty(altitude)
        % Sample behavior -- no inputs given
        altitude = 0; % [m] altitude
end
g_0 = 9.80665; % [m/s^2] standard gravitational acceleration
R_e = 6371007.2; % [m] mean radius of Earth

g_h = g_0 .* (R_e ./ (R_e + altitude)) .^ 2; % [m/s^2]
end

