

% MIGP - MELODIC's Incremental Group-PCA
% Steve Smith, FMRIB, 2012-2013
% not yet finally tweaked/evaluated, or published - please do not pass on.
% adapted by Sean Fitz, 2020

%%%%%%%%%%%%%%%%%%%%%%%%%% USER OPTIONS

INlist=dir('data/cobre/fmri_*.nii.gz');  % list of input 4D NIFTI standard space datasets
INmask='data/brain_mask.nii.gz';       % 3D NIFTI mask image
GO='matMIGP';           % output filename
dPCAint=550;           % internal number of components - typically 2-4 times number of timepoints in each run (if you have enough RAM for that)
dPCAout=100;           % number of eigenvectors to output - should be less than dPCAint and more than the final ICA dimensionality

%%%%%%%%%%%%%%%%%%%%%%%%%% END OF USER OPTIONS

Nsub=length(INlist); [~,r]=sort(rand(Nsub,1));  % will process subjects in random order
mask=read_avw(INmask); 
masksize=size(mask); 
mask=reshape(mask,prod(masksize),1);

demean = @(x) x - repmat(mean(x,1),[size(x,1), 1, 1]);
ss_svds = @(x,n) svds(x, n);

for i = 1:Nsub

    % read data
    filename=[INlist(r(i)).folder, '/', INlist(r(i)).name];
    grot=double(read_avw(filename)); 
    grot=reshape(grot,prod(masksize),size(grot,4)); 
    grot=demean(grot(mask~=0,:)');
    
    % var-norm
    [uu,ss,vv]=ss_svds(grot,30);
    vv(abs(vv)<2.3*std(vv(:)))=0;
    stddevs=max(std(grot-uu*ss*vv'),0.001);
    grot=grot./repmat(stddevs,size(grot,1),1);
    
    
    if (i==1)
        W=demean(grot); clear grot;
    else
        
        % concat
        W=[W; demean(grot)]; clear grot;
        
        % reduce W to dPCAint eigenvectors
        if size(W,1)-10 > dPCAint
            [uu,dd]=eigs(W*W',dPCAint);  
            W=uu'*W; 
            clear uu;
        end

    end
    
end

grot=zeros(prod(masksize),dPCAout); 
grot(mask~=0,:)=W(1:dPCAout,:)'; grot=reshape(grot,[masksize ,dPCAout]);
save_avw(grot,GO,'f',[1 1 1 1]);
system(sprintf('fslcpgeom %s %s -d',filename,GO));

