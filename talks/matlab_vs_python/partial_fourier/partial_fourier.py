#%% Imports
import h5py
import matplotlib.pyplot as plt
import numpy as np

#%% Load Data
h = h5py.File('data.mat','r')
img = np.transpose(h.get('img')['real']+1j*h.get('img')['imag'])

#%% 6/8 Partial Fourier sampling
n = np.random.randn(96,96) + 1j*np.random.randn(96,96)
y = np.fft.fftshift(np.fft.fft2(img),axes=0) + n
y[72:,:] = 0

#%% Estimate phase
pad = np.pad(np.hanning(48),24,'constant')[:,None]
phs = np.exp(1j*np.angle(np.fft.ifft2(np.fft.ifftshift(y*pad,axes=0))))

#%% POCS reconstruction
est = np.zeros((96,96))
iters = 10
for i in range(iters):
    est = np.fft.fftshift(np.fft.fft2(est*phs),axes=0)
    est[:72,:] = y[:72,:]
    est = np.maximum(np.real(np.fft.ifft2(np.fft.ifftshift(est,axes=0))*np.conj(phs)),0)

#%% Plot reconstruction
_, ax = plt.subplots(1,2)
ax[0].imshow(np.abs(np.fft.ifft2(np.fft.ifftshift(y,axes=0))),vmin=0,vmax=1)
ax[0].set_title('Zero-filled')
ax[1].imshow(est, vmin=0, vmax=1)
ax[1].set_title('POCS recon')