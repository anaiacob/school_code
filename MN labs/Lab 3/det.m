function [d] = det(A)
%%% Calcularea determinantului

% INPUTS:
%   A de dimensiune n x n
% OUTPUTS:
%   determinant

%% SOLUTION START %%
n = size(A,1);
[A,p] = gpp(A);
d = 1;
for k = 1:n
    d = d * A(k,k);
end
for k = 1:n-1
    if p(k) ~= k
        d = - d;
    end
end
%% SOLUTION END %%
end