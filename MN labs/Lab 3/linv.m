function [L] = linv(L)
%%% Calcularea inversei unei matice inferior triunghiulare

% INPUTS:
%   L de dimensiune n x n
% OUTPUTS:
%   inv(L)

%% SOLUTION START %%
n = size(L,1);
for j = 1:n
    L(j,j) = 1 / L(j,j);
    if j == n
        break;
    end
    for i = j+1:n
        L(i,j) = - dot(L(i,j:i-1),L(j:i-1,j))/L(i,i);
    end
end
%% SOLUTION END %%
end