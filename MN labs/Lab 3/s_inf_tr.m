function [x] = s_inf_tr(A,b)
%%% Rezolvarea unui sistem determinat inferior triunghiular
% INPUTS:
%   A -- matrice aleatoare inferior triunghiular? de dimensiune (n,n)
%   b -- vector aleator de dimensiune (n,1)
%
% OUTPUTS:
%   x -- vectorul solu?ie al sistemului de dimensiune (n,1)

%% SOLUTION START %%
n = size(A,1);
x = zeros(n,1);
for i = 1:n 
    s = b(i);
    for j = 1:i-1
        s = s - A(i,j)*x(j);
    end
    x(i) = s/A(i,i);
end
%% SOLUTION END %%
end
