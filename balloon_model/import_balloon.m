function balloons_params_struct = import_balloon(name)
%IMPORT_BALLOON Import balloon parameters from JSON configuration file.
%   balloons_params_struct = import_balloon('HAB-800');
fname = sprintf('%s.json', name);
fid = fopen(fname); 
raw = fread(fid,inf); 
str = char(raw'); 
fclose(fid);
balloons_params_struct = jsondecode(str);
end

