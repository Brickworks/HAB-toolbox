function lifting_mass = get_recommended_launch_lifting_mass(altitude, volume_release, molar_mass)
%GET_RECOMMENDED_LAUNCH_HELIUM_MASS Get the LIFTING_MASS (kg) required to
%achieve the volume at release (m^3) at a given ALTITUDE (m).
lifting_mass = mass_from_volume(volume_release, atmo_temp(altitude), atmo_pres(altitude), molar_mass);
end

