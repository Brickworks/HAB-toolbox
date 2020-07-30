function balloon_params_struct = import_balloon(name)
%IMPORT_BALLOON Import balloon parameters from JSON configuration file.
%   balloons_params_struct = import_balloon('HAB-800');
fname = sprintf('%s.json', name);
fid = fopen(fname); 
raw = fread(fid,inf); 
str = char(raw'); 
fclose(fid);
balloon_params_struct = jsondecode(str);
balloon_params_struct.spec.volume_burst.value = (4/3) * pi() * (balloon_params_struct.spec.diameter_burst.value / 2)^3; % assume spherical shape
balloon_params_struct.spec.volume_burst.unit = "m^3";
end

