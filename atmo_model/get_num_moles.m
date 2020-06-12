function moles = get_num_moles(mass, molar_mass)
% GET_NUM_MOLES  Get the number of moles for a given amount of mass.
%   MASS        mass of a substance in kilograms.
%   MOLAR_MASS  molar mass of the substance.
moles = mass / molar_mass;
end