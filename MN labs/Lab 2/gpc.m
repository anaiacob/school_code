function [A, p, q] = gpc(A)
%%% Eliminare Gaussian? cu pivotare complet?
% INPUTS:
%   A -- matrice aleatoare de dimensiune (n,n)
% OUTPUTS:
%   A -- matrice superior triunghiular? cu multiplicatorii gaussieni
%        în triunghiul inferior de dimensiune (n,n)
%   p -- vectorul de permut?ri la nivel de linie
%   q -- vectorul de permut?ri la nivel de coloan?

%% SOLUTION START %%
n = size(A,1);
p = zeros(n,1);
q = zeros(n,1);
for k = 1:n-1
    mx = A(k,k);
    ik = k;
    jk = k;
    for i = k:n
        for j = k:n
            if abs(A(i,j)) > abs(mx)
                mx = A(i,j);
                ik = i;
                jk = j;
            end
        end
    end
    p(k) = ik;
    q(k) = jk;
    for j = k:n
        aux = A(k,j);
        A(k,j) = A(ik,j);
        A(ik,j) = aux;
    end
    for i = 1:n
        aux = A(i,k);
        A(i,k) = A(i,jk);
        A(i,jk) = aux;
    end
    for i = k+1:n
        A(i,k) = A(i,k)/A(k,k);
    end
    for i = k+1:n
        for j = k+1:n
            A(i,j) = A(i,j) - A(i,k)*A(k,j);
        end
    end
end
%% SOLUTION END %%
end