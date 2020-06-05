
function [A] = hab_pendulum(y,t,l,m)

g=9.81; %m/s^2

theta_dot = y(1);
phi_dot = y(2);
theta = y(3);
phi = y(4);

theta_dd = phi_dot.^2 * cos(theta)*sin(theta) - (g/l)*sin(theta);
phi_dd = (-2)*theta_dot*phi_dot * cot(theta);

A = [theta_dd phi_dd theta_dot phi_dot];
   
end