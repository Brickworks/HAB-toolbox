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

%% Setup
% addpath('../../atmo_model'); % import NASA Earth Atmosphere Model functions
addpath('../../balloon_library'); % import balloon configuration files
clear; % clear workspace variables

% Import balloon parameters
balloon_name = 'HAB-3000';
balloon_parameters = import_balloon(balloon_name);

lift_gas = balloon_parameters.spec.lifting_gas;
m_balloon = balloon_parameters.spec.mass.value; % [kg]
burst_volume = balloon_parameters.spec.volume_burst.value; % [m^3] Mission ends if balloon volume is above this value!
burst_altitude = balloon_parameters.spec.altitude_burst.value; % [m] Mission ends if altitude is above this value! 
release_volume = balloon_parameters.spec.volume_release.value; % [m^3]
M = molar_mass(lift_gas); % [kg/mol] molar mass of lifting gas
Cd = balloon_parameters.spec.drag_coefficient; % coefficient of drag

%% Mass Properties
m_payload     = 2.00; % [kg] mass of the payload, not including ballast
m_ballast     = 0.50; % [kg] initial mass of ballast
m_gas_reserve = 1.91; % [kg] minimum mass of lift gas in the balloon !TODO: find this automatically based on payload mass
m_gas_bleed   = 0.50; % [kg] extra lift gas in the balloon for control

%% Calibrated Parameters
mdot_ballast_max = 0.010; % [kg/dt] max ballast rate
mdot_ballast_min = 0.001; % [kg/dt] min ballast rate
mdot_bleed_max   = 0.010; % [kg/dt] max lift gas bleed rate
mdot_bleed_min   = 0.001; % [kg/dt] max lift gas bleed rate

%% Controller Options
target_altitude = 24000; % [m] target altitude
delay_time = 3000; % [s] time to wait after launch before arming
delay_altitude = target_altitude; % [m] altitude to reach before arming
arm_tolerance = 10000; % [m] disarm if error is larger than this
continuous_mode = true; % use continuous variable control vs on/off switches


%% Model Configuration
dt = 1; % [s] simulation step time
initial_altitude = 1000; % [m] altitude above sea level of launch site
noisy_atmosphere = false; % choose whether to simulate actual atmosphere variations
noisy_measurements = false; % choose whether to simulate noisy measurements

if noisy_atmosphere
    atmo_temp_noise_gain = 1e-2; % [dB] random temperature noise power
    atmo_pres_noise_gain = 1e-5; % [dB] random pressure noise power
    atmo_density_noise_gain = 1e-7; % [dB] random density noise power
else
    atmo_temp_noise_gain = 0; % [dB] random temperature noise power
    atmo_pres_noise_gain = 0; % [dB] random pressure noise power
    atmo_density_noise_gain = 0; % [dB] random density noise power
end

if noisy_measurements
    altimeter_noise_gain = 1000; % [dB] noise in altimeter readings
else
    altimeter_noise_gain = 0; % [dB] noise in altimeter readings
end

%% Vary Kp
figure(1); clf;
Ki = 1e-8; % Integral Gain
Kd = 1e-3; % Derivative Gain
Kn = 1e-0; % Derivative Filter Gain
K_list = [1e-8; 1e-7; 1e-6; 1e-5; 1e-4;];

title(sprintf('Ki=%0.2e | Kd=%0.2e | Kn=%0.2e', Ki, Kd, Kn));
xlabel('Time (s)'); ylabel('Altitude (m)'); hold on; grid on; legend('Location', 'southeast');
yline(target_altitude, 'k:', 'DisplayName', 'Target Altitude');

for i = 1:length(K_list)
    Kp = K_list(i);
    tout = sim('simulink_ascent_model_variable_mass_displayorganization');
    plot(tout, altitude, 'DisplayName', sprintf('Kp = %0.2e',Kp));
end
hold off;

%% Vary Ki
figure(2); clf;
Kp = 1e-6; % Proportional Gain
Kd = 1e-3; % Derivative Gain
Kn = 1e-0; % Derivative Filter Gain
K_list = [1e-11; 1e-10; 1e-9; 1e-8; 1e-7;];

title(sprintf('Kp=%0.2e | Kd=%0.2e | Kn=%0.2e', Kp, Kd, Kn));
xlabel('Time (s)'); ylabel('Altitude (m)'); hold on; grid on; legend('Location', 'southeast');
yline(target_altitude, 'k:', 'DisplayName', 'Target Altitude');

for i = 1:length(K_list)
    Ki = K_list(i);
    tout = sim('simulink_ascent_model_variable_mass_displayorganization');
    plot(tout, altitude, 'DisplayName', sprintf('Ki = %0.2e',Ki));
end
hold off;

%% Vary Kd
figure(3); clf;
Kp = 1e-6; % Proportional Gain
Ki = 1e-8; % Integral Gain
Kn = 1e-0; % Derivative Filter Gain
K_list = [1e-3; 5e-3; 1e-2; 1e-1;];

title(sprintf('Kp=%0.2e | Ki=%0.2e | Kn=%0.2e', Kp, Ki, Kn));
xlabel('Time (s)'); ylabel('Altitude (m)'); hold on; grid on; legend('Location', 'southeast');
yline(target_altitude, 'k:', 'DisplayName', 'Target Altitude');

for i = 1:length(K_list)
    Kd = K_list(i);
    tout = sim('simulink_ascent_model_variable_mass_displayorganization');
    plot(tout, altitude, 'DisplayName', sprintf('Kd = %0.2e',Kd));
end
hold off;

%% Vary Kn
figure(3); clf;
Kp = 1e-6; % Proportional Gain
Ki = 1e-8; % Integral Gain
Kd = 1e-3; % Derivative Gain
K_list = [1e-3; 5e-3; 1e-2; 1e-1;];

title(sprintf('Kp=%0.2e | Ki=%0.2e | Kd=%0.2e', Kp, Ki, Kd));
xlabel('Time (s)'); ylabel('Altitude (m)'); hold on; grid on; legend('Location', 'southeast');
yline(target_altitude, 'k:', 'DisplayName', 'Target Altitude');

for i = 1:length(K_list)
    Kn = K_list(i);
    tout = sim('simulink_ascent_model_variable_mass_displayorganization');
    plot(tout, altitude, 'DisplayName', sprintf('Kn = %0.2e',Kn));
end
hold off;

