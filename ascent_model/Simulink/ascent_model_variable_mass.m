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
addpath('../../../balloon_library'); % import balloon configuration files
clear; % clear workspace variables

% Import balloon parameters
balloon_name = 'HAB-3000';
balloon_parameters = import_balloon(balloon_name);

lift_gas = balloon_parameters.spec.lifting_gas;
m_balloon = balloon_parameters.spec.mass.value; % [kg] mass of the balloon
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
delay_time = 0; % [s] time to wait after launch before arming
delay_altitude = target_altitude; % [m] altitude to reach before arming
arm_tolerance = 1000; % [m] disarm if error is larger than this
continuous_mode = true; % use continuous variable control vs on/off switches

%% Gainz
% gains using phils incorrect controller
% Kp = 0.00000005; % Proportional Gain
% Ki = 0.0; % Integral Gain
% Kd = 0.00001; % Derivative Gain
% Kn = 0.1; % Derivative Filter Gain

% I had tuned it to be great but can't get it back
% Kp = 1e-6; % Proportional Gain
% Ki = 1e-8; % Integral Gain
% Kd = 1e-3; % Derivative Gain
% Kn = 2.5; % Derivative Filter Gain

Kp = 5e-1; % Proportional Gain
Ki = 1.5e-10; % Integral Gain
Kd = 1e-1; % Derivative Gain
Kn = 1e-0; % Derivative Filter Gain

%% Model Configuration
dt = 1; % [s] simulation step time
initial_altitude = 18400; % [m] initial altitude above sea level
initial_velocity = 5.126; % [m/s] initial vertical velocity
noisy_atmosphere = false; % choose whether to simulate actual atmosphere variations
noisy_measurements = true; % choose whether to simulate noisy measurements

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
    altimeter_noise_gain = 100; % [dB] noise in altimeter readings
else
    altimeter_noise_gain = 0; % [dB] noise in altimeter readings
end

%% Simulate!
% simulink
tout = sim('simulink_ascent_model_variable_mass_displayorganization');

%% Plots
figure(1); clf;
subplot(2,2,1);
yyaxis left; grid on;
plot(altitude, atmo_temp);
xlabel('Altitude (m)');
ylabel('Temperature (K)');
text_align_point = 225; 
label_tropo = text(11000/2,text_align_point,'Troposphere'); set(label_tropo,'Rotation',90);
xline(11000); 
label_lstrato = text((25000-11000)/2+11000,text_align_point,'Lower Stratosphere'); set(label_lstrato,'Rotation',90);
xline(25000); 
label_ustrato = text(30000,text_align_point,'Upper Stratosphere'); set(label_ustrato,'Rotation',90);
yyaxis right; grid on;
plot(altitude, atmo_pres);
ylabel('Pressure (Pa)');
title('Earth Atmosphere Model - Temperature & Pressure');

subplot(2,2,2);
yyaxis left; hold on; grid on;
plot(altitude, atmo_density, 'DisplayName', 'Ambient');
plot(altitude, balloon_density, 'DisplayName', lift_gas);
plot(altitude, abs(atmo_density-balloon_density), 'DisplayName', 'Density Diff');
xlabel('Altitude (m)'); ylabel('Density (kg/m^3)'); 
hold off;
yyaxis right; hold on; grid on;
plot(altitude, balloon_volume, 'DisplayName', 'Balloon');
yline(burst_volume, 'k:', 'DisplayName', 'Burst Volume');
ylabel('Volume m^3');
legend();

subplot(2,2,3);
hold on; grid on;
yline(m_payload, 'k--', 'DisplayName', 'Payload');
yline(m_gas_reserve, 'k:', 'DisplayName', 'Reserved Gas');
plot(tout, ballast_remaining_kg, 'DisplayName', 'Ballast Remaining');
plot(tout, gas_remaining_kg, 'DisplayName', 'Gas Remaining');
plot(tout, free_lift_kg, 'DisplayName', 'Free Lift');
xlabel('Time (s)'); ylabel('Mass (kg)');
hold off;
legend();

subplot(2,2,4);
hold on; grid on;
plot(tout, weight, 'DisplayName', 'F_g');
plot(tout, buoyancy_force_N, 'DisplayName', 'F_{buoyancy}');
plot(tout, drag_force_N, 'DisplayName', 'F_{drag}');
plot(tout, net_force_N, 'DisplayName', 'F_{net}');
xlabel('Time (s)'); ylabel('Force (N)');
hold off;
legend();

figure(2); clf;
subplot(5,1,1); hold on;  grid on;
title(sprintf('%s | %s', lift_gas, balloon_name));
plot(tout, altitude, 'DisplayName', 'Altitude');
% yline(delay_altitude, 'g:', 'DisplayName', 'Arm Altitude');
yline(target_altitude, 'k:', 'DisplayName', 'Target Altitude');
yline(burst_altitude, 'r:', 'DisplayName', 'Spec Flight Ceiling');
if balloon_volume(end) >= burst_volume
    plot(tout(end), altitude(end), 'rx', 'DisplayName', 'Burst Event');
end
% xlabel('Time (s)'); 
ylabel('Altitude (m)');
legend();

subplot(5,1,2); hold on; grid on;
plot(tout, ascent_rate);
% xlabel('Time (s)'); 
ylabel('Ascent Rate (m/s)');

subplot(5,1,3); hold on; grid on;
plot(tout, ascent_accel);
xlabel('Time (s)'); 
ylabel('Ascent Acceleration (m/s^2)');

subplot(5,1,4); hold on; grid on;
hold on; grid on;
yyaxis left;
plot(tout, control_effort, 'DisplayName', 'Control Effort');
yline(0, 'b:');
ylabel('Control Effort (kg/s)');
yyaxis right;
plot(tout, control_error, 'DisplayName', 'Control Error');
yline(0, 'r:');
ylabel('Control Error (m)');
% xlabel('Time (s)');
hold off;

subplot(5,1,5); 
hold on; grid on;
plot(tout, controller_armed, 'k:', 'DisplayName', 'Controller Armed');
ylabel('Controller Armed');
xlabel('Time (s)');