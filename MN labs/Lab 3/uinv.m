function [U] = uinv(U)
%%% Inversarea unei matrici superior triunghiulare
% INPUTS:
%   U -- matrice aleatoare superior triunghiulara de dimensiune (n,n)
% OUTPUTS:
%   U -- matrice superior triunghiulara 

%% SOLUTION START %%
n = size(U,1);
for j = n:-1:1
    U(j,j) = 1/U(j,j);
    if j == 1
        break;
    end
    for i = j-1:-1:1
        U(i,j) = - dot(U(i,i+1:j),U(i+1:j,j))/U(i,i);
    end
end
%% SOLUTION END %%
end