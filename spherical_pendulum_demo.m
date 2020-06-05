function [bodies] = spherical_pendulum_demo()
close all %close all figure
clear all %clear all variables
clc %clear command window 

clear all;
l=1; % length of string (s
t = 3; % runtime (s) longer run = more swoops
dt = .01; % timestep (s

time = 0:dt:t;
[Ig,Mo,Fo,mG,mass] = elements();
y=[0 1 1 0]; % intial conditions [tdd pdd td pd]

xa = []; % xaxis values
ya = []; % y axis values
za = []; % z axis values
%hold;


  for i = time
     y = y + hab_next(y, i, dt,l,mass);
     xa = [xa; l*sin(y(3))*cos(y(4))]; % polar to cartesian transform
     ya = [ya; l*sin(y(3))*sin(y(4))];
     za = [za; -l*cos(y(3))];
     %drawnow();
     %plot3(xa,ya,za); % animate (takes a long time)
     %pause(.001);
  end
plot3(xa,ya,za);

xlim([-1 1]);
ylim([-1 1]);
zlim([-1 1]); 


end