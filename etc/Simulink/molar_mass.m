function M = molar_mass(gas)
%MOLAR_MASS Get the molecular weight (kg/mol) of a dry GAS at sea level.
%   Source: US Standard Atmosphere, 1976
%   --- -------
%   Key Species
%   --- -------
%   He  Helium
%   H2  Hydrogen
%   N2  Nitrogen
%   O2  Oxygen
%   Ar  Argon
%   CO2 Carbon Dioxide
%   Ne  Neon
%   Kr  Krypton
%   Xe  Xenon
%   CH4 Methane
switch lower(gas)
    case {'air'}
        M = 0.02897;
    case {'he', 'helium'}
        M = 0.0040026;
    case {'h2', 'hydrogen'}
        M = 0.00201594;
    case {'n2', 'nitrogen'}
        M = 0.0280134;
    case {'o2', 'oxygen'}
        M = 0.0319988;
    case {'ar', 'argon'}
        M = 0.039948;
    case {'co2', 'carbon dioxide'}
        M = 0.04400995;
    case {'ne', 'neon'}
        M = 0.020183;
    case {'kr', 'krypton'}
        M = 0.08380;
    case {'xe', 'xenon'}
        M = 0.13130;
    case {'ch4', 'methane'}
        M = 0.01604303;
end
end

