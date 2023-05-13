% creates a geometry for simulation

%% opening the file
addpath ('../../src/3d2dmask') %pre-precesing libraries
f1 = fopen('input/XZC_134_138_138.raw','r'); %read raw file
fp = fread(f1, 134*138*138,'uint8=>uint8'); %size of model
fp = reshape(fp, 134,138,138); %size of model

%% selecting a smaller subset
fp_printing = fp(1:134, 1:138, 1:138); %size of model
figure();imagesc(fp_printing(:,:,uint8(print_size/2)));
title('Cross-section of the simulation subset')

%% eliminating non-connected regions 
connect = 6; % pixel connectivity 6, 18, 26
fp = eliminate_isolatedRegions(fp, connect); %for better convergence

%% making a computationally efficent domain for sim
name = ['XZC'];
add_mesh   = true; % add a neutral-wet mesh at the end of the domain
num_slices = 1;    % add n empty slices at the beggining and end of domain 
                   % for pressure bcs
swapXZ = false;     % Swap x and z data if needed to ensure Palabos simulation in Z-direction              
scale_2 = false;   % Double the grain (pore) size if needed to prevent single pixel throats
                   % for tight/ low porosity geometries                   

palabos_3Dmat = create_geom_edist(fp_printing,name,num_slices, add_mesh, ...
                                    swapXZ, scale_2);  
                                    %provides a very  efficient 
                                    %geometry for Palabos


% old version
%palabos_3Dmat = mat2dat_4lbm(fp_printing,name,1); %although this function is slow, it 
                                    

%% Mixed Wettability (the user could experiment with this)                                
rng(123)                                    
rnd_array = rand(size(palabos_3Dmat) );

palabos_3Dmat_mixedWet = palabos_3Dmat;
palabos_3Dmat_mixedWet(palabos_3Dmat==1 & rnd_array>0.5)=3;

