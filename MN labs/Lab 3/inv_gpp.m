function [A] = inv_gpp(A)
%%% Inversarea unei matrici utilizand eliminarea gaussiana cu pivotare
%%% partiala
% INPUTS:
%   A -- matrice aleatoare de dimensiune (n,n)
% OUTPUTS:
%   A -- matrice de dimensiune (n,n) 

%% SOLUTION START %%
[A,p] = gpp(A);
n = size(A,1);
U = triu(A);
U = uinv(U);
A = tril(A,-1) + U;
for k = n-1:-1:1
    m = zeros(n,1);
    for i = k+1:n
        m(i) = A(i,k);
    end
    for i = 1:k
        A(i,k) = A(i,k) - dot(A(i,k+1:n),m(k+1:n));
    end
    for i = k+1:n
        A(i,k) = - dot(A(i,k+1:n),m(k+1:n));
    end
    if p(k) ~= k
        for i = 1:n
            aux = A(i,k);
            A(i,k) = A(i,p(k));
            A(i,p(k)) = aux;
        end
    end
end
%% SOLUTION END %%
end