function [Ig,Mo,Fo,mG,mass] = elements()
close all %close all figure
clear all %clear all variables
clc %clear command window 

bodies = [];
mass=0;
Ig = [0 0 0;0 0 0;0 0 0];
Mo = [0 0 0];
Fo = [0 0 0];
mG = [0 0 0];

  element1 = struct(
  'name', "box", ... %element name
  'Lcm', [0 1 .5],... %location of center of mass of element m
  'm', 2,... %mass kg
  'Lf', [0,.5,.25],...%mocation of force vector m
  'F' , [0 0 0] ... %force vector N
  );
  element2 = struct(
  'name', "thruster", ... %element name
  'Lcm', [.25 .5 .1],... %m
  'm', 3,... % kg
  'Lf', [0,.5,0],...%m
  'F' , [0 1 .5] ... %N
  );
  
bodies = [element1, element2];

  for i = 1:length(bodies)
    
    mass = mass + bodies(i).m;
     I = [(bodies(i).m*((bodies(i).Lcm(2))^2 + (bodies(i).Lcm(3))^2))... %inertia tesnor calculations
          (bodies(i).m*((bodies(i).Lcm(1)) * (bodies(i).Lcm(2))))...
          (bodies(i).m*((bodies(i).Lcm(1)) * (bodies(i).Lcm(3))));...
          (bodies(i).m*((bodies(i).Lcm(1)) * (bodies(i).Lcm(2))))...
          (bodies(i).m*((bodies(i).Lcm(1))^2 + (bodies(i).Lcm(3))^2))...
          (bodies(i).m*((bodies(i).Lcm(2)) * (bodies(i).Lcm(3))));...
          (bodies(i).m*((bodies(i).Lcm(1)) * (bodies(i).Lcm(3))))...
          (bodies(i).m*((bodies(i).Lcm(3)) * (bodies(i).Lcm(2))))...
          (bodies(i).m*((bodies(i).Lcm(1))^2 + (bodies(i).Lcm(2))^2))...
     ];
     Ig = Ig + I; %kg/m^2
     
     Mo = Mo + cross(bodies(i).Lf, bodies(i).F); %moment about o
     Fo = Fo + bodies(i).F; %sum of forces on o
     mG = mG + bodies(i).m * bodies(i).Lcm;
  end
  mG = mG/mass;% center of mass
  
 
end