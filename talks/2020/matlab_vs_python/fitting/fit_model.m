%% Play with model fitting

% experimental parameters
TEs = [10 40 50 60 80];
TRs = [.8 1 1.5 2];
[TEs,TRs] = meshgrid(TEs,TRs);
TEs = TEs(:)'; TRs = TRs(:)';

% forward model
forward = @(p)( p(1)*exp(-p(3)*TEs).*(1-exp(-p(2)*TRs)));

% simulate data

true_p    = [100,1/.8,1/50];
data      = forward(true_p);
snr       = 50;
noise_std = 100/snr;
noise     = randn(size(data))*noise_std;
data      = data+noise;

plot(data)

%%
% cost function is mean squared error (MSE)
cf = @(x)( mean( (forward(x)-data).^2 ) );

% initial guess
p0 = [200,1/1,1/70];


% using fminsearch (Nelder-Mead)
p  = fminsearch(@(x) cf(x),p0);

% plot result
figure,hold on
plot(data,'.')
plot(forward(p))

%% The below uses fminunc, which allows morre flexibility 
% (like choosing the algorithm or providing gradients and Hessians)

options  = optimoptions('fminunc','Display','off','Algorithm','quasi-newton'); 

[x,fval] = fminunc(cf,p0,options);

figure,hold on
plot(data,'.')
plot(forward(x))

