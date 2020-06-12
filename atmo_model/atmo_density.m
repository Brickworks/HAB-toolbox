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

function rho = atmo_density(altitude)
% ATMO_DENSITY  Density of the atmosphere (kg/m^3) at a given altitude (m).
% Depends on ATMO_PRES in kPa, ATMO_TEMP in K
if nargin < 1 || isempty(altitude)
    % Sample behavior -- no inputs given
    altitude = 0:85000; % [m] altitude
end

rho = (atmo_pres(altitude) ./ 1000) ./ (0.2869 .* atmo_temp(altitude));

if nargin < 1 || isempty(altitude)
    % Sample behavior -- output not assigned to variable
    plot(altitude, atmo_density(altitude))
    xlabel('Altitude (m)');
    ylabel('Density (kg / m^3)')
    title('Earth Atmosphere Model - Density');
    text_align_point = 0.1; 
    label_tropo = text(11000/2,text_align_point,'Trophosphere'); set(label_tropo,'Rotation',90);
    xline(11000); 
    label_lstrato = text((25000-11000)/2+11000,text_align_point,'Lower Stratosphere'); set(label_lstrato,'Rotation',90);
    xline(25000); 
    label_ustrato = text(30000,text_align_point,'Upper Stratosphere'); set(label_ustrato,'Rotation',90);
end
end