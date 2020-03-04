%% Imports

%% Integrate ODE
[t, M] = ode45(@(t,M)bloch_ode(t,M,1500,50),linspace(0,5,1000),[0;0;1]);

%% Plot Results
clf();hold on;
plot(t,M(:,1));
plot(t,M(:,2));
plot(t,M(:,3));

%% Define bloch and b_eff functions
function dM = bloch_ode(t,M,T1,T2)
    B   =   B_eff(t);                               % B-effective
    dM  =  [M(2)*B(3) - M(3)*B(2) - M(1)/T2;        % dMx/dt
            M(3)*B(1) - M(1)*B(3) - M(2)/T2;        % dMy/dt
            M(1)*B(2) - M(2)*B(1) - (M(3)-1)/T1];   % dMz/dt
end

function b = B_eff(t)
    if t < 0.25                 % No B-field
        b = [0, 0, 0];
    elseif t < 1.25             % 1-ms excitation around x-axis
        b = [1.8*sinc(t-0.75), 0, 0];
    elseif t < 1.50             % No B-field
        b = [0, 0, 0];
    elseif t < 3.00             % Gradient in y-direction
        b = [0, 0, 2*pi];
    else                        % No B-field
        b = [0, 0, 0];
    end
end