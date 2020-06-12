%% Ascent Model
% Philip Linden

%% Assumptions
% * Helium in balloon behaves as an ideal gas
% * Atmosphere is homogenous and uniform composition at all altitudes
% * Atmosphere is a static fluid (no convection or winds)
% * Gas in the balloon is the same temperature and pressure as the
%   atmosphere
% * Balloon maintains a uniform spherical shape over the whole flight
% * Ignore stretching of balloon, assume internal pressure is the same as
%   ambient pressure.
% * Ignore dynamics of the balloon-payload system and treat it as a blob

%% Resources
% * https://www.grc.nasa.gov/www/k-12/Numbers/Math/Mathematical_Thinking/designing_a_high_altitude.htm
% * https://www.grc.nasa.gov/WWW/K-12/airplane/atmosmet.html
% * https://www.kaymont.com/habphotography

%% Definitions   
%   m_payload     mass of the payload - CONTROL INPUT
%   m_helium      mass of helium in balloon - CONTROL INPUT
%   n_helium      number of moles of helium in balloon
%   vol_balloon   volume of air displaced by the balloon
%   rho_helium    density of helium in balloon
%   temp_helium   temperature of helium in balloon
%   pres_helium   pressure of helium in balloon
%   rho_air       density of air around balloon as a function of altitude
%   temp_air      temperature of air around balloon as a function of altitude
%   pres_air      pressure of air around balloon as a function of altitutde

%% Setup
addpath('../atmo_model'); % import NASA Earth Atmosphere Model functions
addpath('../balloon_model'); % import balloon configuration files
clear; % clear workspace variables

% Import balloon parameters
balloon_name = 'HAB-800';
balloon_parameters = import_balloon(balloon_name);

lift_gas = balloon_parameters.spec.lifting_gas;
m_balloon = balloon_parameters.spec.mass.value; % [kg]
balloon_burst_pressure = balloon_parameters.spec.pressure_burst.value; % [Pa] Mission ends if balloon pressure is below this value! 
balloon_burst_diameter = balloon_parameters.spec.diameter_burst.value; % [m] Mission ends if balloon diameter is above this value!
balloon_burst_volume = (4/3) * pi() * (balloon_burst_diameter / 2)^3; % [m^3]
balloon_release_volume = balloon_parameters.spec.volume_release.value; % [m^3]
M = molar_mass(lift_gas); % [kg/mol] molar mass of lifting gas
%% Defining the system of equations
% First compute the ideal gas properties of the balloon filled with gas as
% a function of altitude, assuming the gas inside the balloon has the same
% temperature and pressure as the ambient air.
V_gas = @(altitude, m_gas) (V(atmo_temp(altitude), atmo_pres(altitude), m_gas, M));
rho_gas = @(altitude, m_gas) (rho(atmo_temp(altitude), atmo_pres(altitude), M));

% Next we sum the forces acting on the balloon-payload system.
F_buoyancy = @(altitude, m_gas) (V_gas(altitude, m_gas) .* (rho_gas(altitude, m_gas) - atmo_density(altitude)) .* -g(altitude));
Fg_balloon = @(altitude, m_balloon) (m_balloon .* -g(altitude));
Fg_payload = @(altitude, m_payload) (m_payload .* -g(altitude));

F_net = @(altitude, m_gas, m_balloon, m_payload) (F_buoyancy(altitude, m_gas) + Fg_balloon(altitude, m_balloon) + Fg_payload(altitude, m_payload));

%% Sanity Check
% Now let's sanity check with some plots, assuming a closed system.
altitude = 0:35000; % [m]
m_payload = 2; % [kg] initial mass of the payload
m_gas = get_recommended_launch_lifting_mass(altitude(1), balloon_release_volume, M); % [kg] initial helium mass

[T_a, P_a, rho_a] = atmo_model(altitude);
[~,index_closest_altitude_to_burst_pressure] = min(abs(balloon_burst_pressure - P_a));
pressure_burst_altitude = altitude(index_closest_altitude_to_burst_pressure);

balloon_volume = V_gas(altitude, m_gas);
[~,index_closest_altitude_to_burst_volume] = min(abs(balloon_burst_volume - balloon_volume));
volume_burst_altitude = altitude(index_closest_altitude_to_burst_volume);

figure(1); clf;
subplot(2,1,1);
yyaxis left; hold on;
plot(altitude, atmo_density(altitude), 'DisplayName', 'Ambient');
plot(altitude, rho_gas(altitude, m_gas), 'DisplayName', lift_gas);
plot(altitude, atmo_density(altitude)-rho_gas(altitude, m_gas), 'DisplayName', 'diff');
xlabel('Altitude'); ylabel('Density (kg/m^3)');
hold off;
yyaxis right; hold on;
plot(altitude, F_buoyancy(altitude, m_gas), 'DisplayName', 'F_{buoyancy}');
plot(altitude, F_net(altitude, m_gas, m_balloon, m_payload), 'DisplayName', 'F_{net}');
xlabel('Altitude'); ylabel('Force (N)');
hold off;
legend();

subplot(2,1,2);
yyaxis left;
hold on;
xline(pressure_burst_altitude, 'b--', 'DisplayName', 'Pressure Burst Threshold');
plot(altitude, P_a, 'b', 'DisplayName', 'Balloon Pressure');
xlabel('Altitude'); ylabel('Pressure (Pa)');
hold off;
yyaxis right;
hold on;
xline(volume_burst_altitude, 'r--', 'DisplayName', 'Volume Burst Threshold');
plot(altitude, balloon_volume, 'r', 'DisplayName', 'Balloon Volume');
xlabel('Altitude'); ylabel('Volume (m^3)');
hold off;
legend();
