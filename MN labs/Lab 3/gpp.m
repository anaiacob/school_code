function [A, p] = gpp(A)
%%% Eliminare Gaussian? cu pivotare par?ial?
% INPUTS:
%   A -- matrice aleatoare de dimensiune (n,n)
% OUTPUTS:
%   A -- matrice superior triunghiular? cu multiplicatorii gaussieni
%        în triunghiul inferior de dimensiune (n,n)
%   p -- vectorul de permut?ri la nivel de linie

%% SOLUTION START %%
n = size(A,1);
p = zeros(n,1);
for k = 1:n-1
    mx = A(k,k);
    ik = k;
    for i = k+1:n
        if abs(A(i,k)) > abs(mx)
            mx = A(i,k);
            ik = i;
        end
    end
    p(k) = ik;
    for j = k:n
        aux = A(k,j);
        A(k,j) = A(ik,j);
        A(ik,j) = aux;
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

