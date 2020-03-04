%% Imports

%% Load Data
h = matfile('data.mat');
img = h.img;

%% 6/8 Partial Fourier sampling
n = randn(96) + 1j*randn(96);
y = fftshift(fft2(img),1) + 0*n;
%y(73:end,:) = 0;

%% Estimate phase
pad = padarray(hann(48),24);
phs = exp(1j*angle(ifft2(ifftshift(y.*pad,1))));

%% POCS reconstruction
est = zeros(96);
iters = 10;
for i = 1:iters
    est = fftshift(fft2(est.*phs),1);
    est(1:72,:) = y(1:72,:);
    est = max(real(ifft2(ifftshift(est,1)).*conj(phs)),0);   
end

%% Plot reconstruction
figure();
subplot(1,2,1);
imshow(abs(ifft2(ifftshift(y,1))),[0 1],'colormap',jet);
title('Zero-Filled');
subplot(1,2,2);
imshow(est,[0 1],'colormap',jet);
title('POCS recon');