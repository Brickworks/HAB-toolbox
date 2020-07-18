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

%% Setup
addpath('../atmo_model'); % import NASA Earth Atmosphere Model functions
addpath('../balloon_library'); % import balloon configuration files
clear; % clear workspace variables

% Import balloon parameters
balloon_name = 'HAB-3000';
balloon_parameters = import_balloon(balloon_name);

lift_gas = balloon_parameters.spec.lifting_gas;
m_balloon = balloon_parameters.spec.mass.value; % [kg]
burst_pressure = balloon_parameters.spec.pressure_burst.value; % [Pa] Mission ends if balloon pressure is below this value! 
burst_volume = balloon_parameters.spec.volume_burst.value; % [m^3] Mission ends if balloon volume is above this value!
release_volume = balloon_parameters.spec.volume_release.value; % [m^3]
M = molar_mass(lift_gas); % [kg/mol] molar mass of lifting gas
Cd = balloon_parameters.spec.drag_coefficient; % coefficient of drag

%% Defining the system of equations
% First compute the ideal gas properties of the balloon filled with gas as
% a function of altitude, assuming the gas inside the balloon has the same
% temperature and pressure as the ambient air.
V_gas = @(altitude, m_gas) (V(atmo_temp(altitude), atmo_pres(altitude), m_gas, M));
rho_gas = @(altitude, m_gas) (rho(atmo_temp(altitude), atmo_pres(altitude), M));
A_balloon = @(altitude, m_gas) ((V_gas(altitude, m_gas) / (4/3 * pi())).^(1/3));

% Next we sum the forces acting on the balloon-payload system.
F_buoyancy = @(altitude, m_gas) (V_gas(altitude, m_gas) .* (rho_gas(altitude, m_gas) - atmo_density(altitude)) .* -g(altitude));
Fg_balloon = @(altitude, m_balloon) (m_balloon .* -g(altitude));
Fg_payload = @(altitude, m_payload) (m_payload .* -g(altitude));

F_net = @(altitude, m_gas, m_balloon, m_payload) (F_buoyancy(altitude, m_gas) + Fg_balloon(altitude, m_balloon) + Fg_payload(altitude, m_payload));

%% Sanity Check - Closed system, check over altitude range
% Now let's sanity check with some plots, assuming a closed system.
% * altitude      estimated vertical flight range
% * m_payload     mass of the payload - CONTROL INPUT
% * m_gas         mass of lifting gas in balloon - CONTROL INPUT
altitude = 0:35000; % [m]
m_payload = 1.5; % [kg] initial mass of the payload
m_gas = get_recommended_launch_lifting_mass(altitude(1), release_volume, M); % [kg] initial lifting mass added to balloon

[T_a, P_a, rho_a] = atmo_model(altitude);
[~,index_closest_altitude_to_burst_pressure] = min(abs(burst_pressure - P_a));
pressure_burst_altitude = altitude(index_closest_altitude_to_burst_pressure);

balloon_volume = V_gas(altitude, m_gas);
[~,index_closest_altitude_to_burst_volume] = min(abs(burst_volume - balloon_volume));
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

%% Ascent rate, drag force, and other parameters as functions of time
F_drag = @(altitude, ascent_rate) (Cd/2 .* rho_gas(altitude, m_gas) .* -(ascent_rate .^2) .* A_balloon(altitude, m_gas));

dt = 0.1; % [s] time step
t = 0:dt:3600; % [s] elapsed time since launch
altitude_0 = 0; % [m] initial altitude
ascent_rate_0 = 0; % [m/s] initial velocity

eq_of_motion = @(t,x) [x(2); (F_buoyancy(x(1), m_gas) + F_drag(x(1), x(2)) + Fg_balloon(x(1), m_balloon) + Fg_payload(x(1), m_payload)) ./ (m_balloon + m_payload + m_gas)];
[t, x] = ode45(eq_of_motion, t, [altitude_0, ascent_rate_0]);
altitude = x(:,1);
ascent_rate = x(:,2);
ascent_accel = (F_buoyancy(altitude, m_gas) + F_drag(altitude, ascent_rate) + Fg_balloon(altitude, m_balloon) + Fg_payload(altitude, m_payload)) ./ (m_balloon + m_payload + m_gas);

[~,index_closest_altitude_to_burst_volume] = min(abs(volume_burst_altitude - altitude));
[~,index_closest_altitude_to_burst_pressure] = min(abs(pressure_burst_altitude - altitude));
burst_index = min(index_closest_altitude_to_burst_volume, index_closest_altitude_to_burst_pressure);

figure(2); clf;
subplot(3,1,1); hold on;  grid on;
title(sprintf('%.2d kg payload | %.2d kg %s | %s', m_payload, m_gas, lift_gas, balloon_name));
plot(t, altitude, 'DisplayName', 'Altitude');
plot(t(burst_index), altitude(burst_index), 'rx', 'DisplayName', 'Burst Event');
yline(pressure_burst_altitude, 'k--', 'DisplayName', 'Pressure Burst Threshold');
yline(volume_burst_altitude, 'k:', 'DisplayName', 'Volume Burst Threshold');
xlabel('Time (s)'); ylabel('Altitude (m)');
legend();
subplot(3,1,2); hold on; grid on;
plot(t, ascent_rate);
xlabel('Time (s)'); ylabel('Ascent Rate (m/s)');
subplot(3,1,3); hold on; grid on;
plot(t, ascent_accel);
xlabel('Time (s)'); ylabel('Ascent Acceleration (m/s^2)');

%% Open system, balloon and payload lose mass over time
%% Control loop with bleeding ballast/lift gas as control inputs