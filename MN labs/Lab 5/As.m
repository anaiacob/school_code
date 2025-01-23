function [A] = As(u,beta,A)
%% Pasul As din HQ(inmultire la stanga cu un reflector)
% INPUTS:
%   u    -- vectorul definitoriu al reflectorului (n, 1),   
%   beta -- scalarul definitoriu al reflectorului, 
%   A    -- matricea care se inmulteste (n, n)  
%
% OUTPUT:
%   A    -- matricea care se inmulteste (n, n) 

%% SOLUTION START %%
n = size(A,1);
p = size(A,2);
for j = 1:p
    suma = 0;
    for k = 1:n
        suma = suma + u(k)*A(k,j);
    end
    thau = suma/beta;
    for i = 1:n
        A(i,j) = A(i,j)-thau*u(i);
    end
end
%% SOLUTION END %%
end