%% Fitting Radial Basis Functions to some data

% Generate a noisy sine wave and plot it
x = linspace(0,10,100);
y = sin(3*x) + randn(size(x))*.5;
    
figure,
plot(x,y)

%% Fit RBF

% This defines a RBF atom function
sig = 2;
rbf = @(x,c)(exp(-(x-c).^2/sig^2));

% design matrix for fitting
xi     = linspace(0,10,20);
desmat = zeros(length(x),length(xi));
for i=1:length(xi)
    % each column is an RBF centered around xi
    desmat(:,i) = rbf(x,xi(i));
end
% fit model
beta = desmat\y';

% plot fit
figure(1),hold on
plot(x,y,'.','markersize',10)
h = plot(x,desmat,'k'); for i =1:20;h(i).Color=[0,0,0,0.2];end
plot(x,desmat*beta,'-','linewidth',2)
% make it a little prettier
grid on
xlabel('x')
ylabel('y')
set(gca,'fontsize',16)
title('RBF fitting')

%% save figure
print -depsc ~/Desktop/RBF.eps 
close(1)
!open  ~/Desktop/RBF.eps

