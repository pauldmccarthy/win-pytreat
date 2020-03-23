%% Load Data
% get matfile object
h = matfile('data.mat');

% get img variable from the mat-file
img = h.img;

%% 6/8 Partial Fourier sampling
% generate normally-distributed complex noise
n = randn(96) + 1j*randn(96);

% Fourier transform the image and add noise
y = fftshift(fft2(img),1) + n;

% set bottom 24/96 lines to 0
y(73:end,:) = 0;

% show sampling
figure();
imshow(log(abs(fftshift(y,2))), [], 'colormap', jet)

%% Estimate phase
% create zero-padded hanning filter for ky-filtering
filt = padarray(hann(48),24);

% generate low-res image with inverse Fourier transform
low = ifft2(ifftshift(y.*filt,1));

% get phase image
phs = exp(1j*angle(low));

% show phase estimate alongside true phase
figure();
subplot(1,2,1);
imshow(angle(img), [-pi,pi], 'colormap', hsv);
title('True image phase');

subplot(1,2,2);
imshow(angle(phs), [-pi,pi], 'colormap', hsv)
title('Estimated phase');

%% POCS reconstruction
% initialise image estimate to be zeros
est = zeros(96);

% set number of iterations
iters = 10;

% each iteration cycles between projections
for i = 1:iters
% projection onto data-consistent set:
    % use a-priori phase to get complex image
    est = est.*phs;

    % Fourier transform to get k-space
    est = fftshift(fft2(est), 1);

    % replace data with measured lines
    est(1:72,:) = y(1:72,:);

    % inverse Fourier transform to get back to image space
    est = ifft2(ifftshift(est, 1));

% projection onto non-negative reals
    % remove a-priori phase
    est = est.*conj(phs);

    % get real part
    est = real(est);

    % ensure output is non-negative
    est = max(est, 0);
end

%% Display error and plot reconstruction
% compute zero-filled recon
zf = ifft2(ifftshift(y, 1));

% compute rmse for zero-filled and POCS recon
err_zf = norm(zf(:) - img(:));
err_pocs = norm(est(:).*phs(:) - img(:));

% print errors
fprintf(1, 'RMSE for zero-filled recon: %f\n', err_zf);
fprintf(1, 'RMSE for POCS recon: %f\n', err_pocs);

% plot both recons side-by-side
figure();

% plot zero-filled
subplot(2,2,1);
imshow(abs(zf), [0 1]);
title('Zero-Filled');
subplot(2,2,3);
plot(abs(zf(:,48)), 'linewidth', 2);

% plot POCS
subplot(2,2,2);
imshow(est, [0 1]);
title('POCS recon');
subplot(2,2,4);
plot(abs(est(:,48)), 'linewidth', 2);
