function free_lift_kg = free_lift(altitude, balloon_mass, payload_mass)
%FREE_LIFT Get the mass component of the net total force including
%PAYLOAD_MASS (kg) and HELIUM_MASS (kg) at a given ALTITUDE (m).
free_lift_kg = ((gross_lift(altitude, balloon_mass) - (balloon_mass + payload_mass)));
end

