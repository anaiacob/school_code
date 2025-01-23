function [A, U, beta] = TORT(A)
%% Triangularizare ortogonala cu reflectori
% INPUTS:
%   A -- matrice aleatoare de dimensiune (m, n)
%
% OUTPUT:
%   A -- matrice de dimensiune (m, n) peste care
%        se suprascrie matricea superior triunhiulara R
%   U -- matrice de dimensiune (m, p), unde p = min (m − 1, n)
%   beta -- vector de dimensiune (p, 1), unde p = min (m − 1, n)

%% SOLUTION START %%
[m,n] = size(A);
p = min(m-1,n);
U = zeros(m,p);
beta = zeros(p,1);
for k = 1:p
    sigma = sign(A(k,k))*sqrt(dot(A(k:m,k),A(k:m,k)));
    if sigma == 0
        beta(k) = 0;
    else
        U(k,k) = A(k,k) + sigma;
        for i = k+1:m
            U(i,k) = A(i,k);
        end
        beta(k) = sigma*U(k,k);
        A(k,k) = - sigma;
        for i = k+1:m
            A(i,k) = 0;
        end
        for j = k+1:n
            thau = dot(U(k:m, k),A(k:m, j))/beta(k);
            A(k:m,j) = A(k:m,j) - thau*U(k:m,k);
        end
    end
end
%% SOLUTION END %%
end