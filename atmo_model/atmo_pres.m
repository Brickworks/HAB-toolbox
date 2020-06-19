%% US Standard Atmosphere Model
% ----------------------------------------------------------------------- %
% Aerodynamic forces directly depend on the air density. To help aircraft
% designers, it is useful to define a standard atmosphere model of the
% variation of properties through the atmosphere. There are actually
% several different models available--a standard or average day, a hot day,
% a cold day, and a tropical day. The models are updated every few years to
% include the latest atmospheric data. The model was developed from
% atmospheric measurements that were averaged and curve fit to produce the
% given equations. The model assumes that the pressure and temperature
% change only with altitude.
% ----------------------------------------------------------------------- %
% https://www.grc.nasa.gov/WWW/K-12/airplane/atmosmet.html
% -------------------------------------------------------------------------
% Zone  Name                Altitude Range (meters)
% 0     Troposphere         [0,     11000)
% 1     Lower Stratosphere  [11000, 25000) 
% 2     Upper Stratosphere  [25000, 85000)
% -------------------------------------------------------------------------
%% Assumptions
% * Atmosphere is homogenous and uniform composition each discrete layer
% * Atmosphere is a static fluid (no convection or winds)
% * Atmospheric conditions only vary with altitude

function p = atmo_pres(altitude)
% ATMO_PRES  Pressure (Pa) of the atmosphere at a given altitude (m).
% Depends on ATMO_TEMP
if nargin < 1 || isempty(altitude)
    % Sample behavior -- no inputs given
    altitude = 0:85000; % [m] altitude
end

p_model = @(h) ( ... % model in kPa
    (h < 11000) .* (101.29 * ((atmo_temp(h) / 288.08) ^ 5.256)) + ... % troposphere
    (11000 <= h & h < 25000) .* (22.65 * exp(1.73 - 0.000157 * h)) + ... % lower stratosphere
    (25000 <= h & h <= 85000) .* (2.488 * ((atmo_temp(h) / 216.6) ^ -11.388)) ... % upper stratosphere
);
p = arrayfun(p_model,altitude) * 1000;

if nargin < 1 || isempty(altitude)
    % Sample behavior -- output not assigned to variable
    plot(altitude, p);
    xlabel('Altitude (m)');
    ylabel('Pressure (Pa)');
    title('Earth Atmosphere Model - Pressure');
    text_align_point = -1500; 
    text(11000/2,text_align_point,'Trophosphere');
    xline(11000); text((25000-11000)/2+11000,text_align_point,'Lower Stratosphere');
    xline(25000); text((99999-25000)/2+25000,text_align_point,'Upper Stratosphere');
end
end