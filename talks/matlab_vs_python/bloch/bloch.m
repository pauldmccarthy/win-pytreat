% Plot the pulse sequence
% create figure
figure(); 

% get pulse sequence B-fields from 0-5 ms
pulseq = zeros(1000,3);
for i = 1:1000
    pulseq(i,:) = B_eff(i*0.005); 
end

% plot RF
subplot(2,1,1);
plot(pulseq(:,1));
ylabel('B1');

% plot gradient
subplot(2,1,2);
plot(pulseq(:,3));
ylabel('Gradient');

%% Integrate ODE
T1 = 1500;
T2 = 50;
t0 = 0;
t1 = 5;
dt = 0.005;
M0 = [0; 0; 1];
[t, M] = ode45(@(t,M)bloch_ode(t, M, T1, T2), linspace(t0, t1, (t1-t0)/dt), M0);

%% Plot Results
% create figure
figure();hold on;

% plot x, y and z components of Magnetisation
plot(t, M(:,1), 'linewidth', 2);
plot(t, M(:,2), 'linewidth', 2);
plot(t, M(:,3), 'linewidth', 2);

% add legend and grid
legend({'Mx','My','Mz'});
grid on;

%% define the bloch equation
function dM = bloch_ode(t, M, T1, T2)
    % get effective B-field at time t
    B   =   B_eff(t);                               

    % cross product of M and B, add T1 and T2 relaxation terms
    dM  =  [M(2)*B(3) - M(3)*B(2) - M(1)/T2;        
            M(3)*B(1) - M(1)*B(3) - M(2)/T2;        
            M(1)*B(2) - M(2)*B(1) - (M(3)-1)/T1];   
end

%% define effective B-field
function b = B_eff(t)
    % Do nothing for 0.25 ms
    if t < 0.25             
        b = [0, 0, 0];
    % Sinc RF along x-axis and slice-select gradient on for 1.00 ms
    elseif t < 1.25             
        b = [pi*sinc((t-0.75)*4), 0, pi];
    % Do nothing for 0.25 ms
    elseif t < 1.50             
        b = [0, 0, 0];
    % Slice refocusing gradient on for 1.50 ms
    % Half the area of the slice-select gradient lobe
    elseif t < 3.00             
        b = [0, 0, -(1/3)*pi];
    % pulse sequence finished
    else                       
        b = [0, 0, 0];
    end
end
