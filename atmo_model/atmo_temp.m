%% Earth Atmosphere Model
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

function T = atmo_temp(altitude)
% ATMO_TEMP  Temperature (K) of the atmosphere at a given altitude (m).
if nargin < 1 || isempty(altitude)
    % Sample behavior -- no inputs given
    altitude = 0:85000; % [m] altitude
end

T_model = @(h) ( ... % model in Celsius
    (h < 11000) .* (15.04 - 0.00649 .* h) + ... % troposphere
    (11000 <= h & h < 25000) .* (-56.46) + ... % lower stratosphere
    (25000 <= h & h <= 85000) .* (-131.21 + 0.00299 .* h) ... % upper stratosphere
);
T = C_to_K(arrayfun(T_model,altitude));

if nargin < 1 || isempty(altitude)
    % Sample behavior -- output not assigned to variable
    plot(altitude, T);
    xlabel('Altitude (m)');
    ylabel(['Temperature (' char(176) 'C)']);
    title('Earth Atmosphere Model - Temperature');
    text_align_point = 100; text(11000/2,text_align_point,'Trophosphere');
    xline(11000); text((25000-11000)/2+11000,text_align_point,'Lower Stratosphere');
    xline(25000); text((84852-25000)/2+25000,text_align_point,'Upper Stratosphere');
    set(gca, 'YDir','reverse');
    camorbit(-90,0);
end
end