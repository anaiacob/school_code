% Rezolvare sisteme liniare cu gpp (verificare gpp)
n = 8;
A = randn(n,n);
b = randn(n,1);
B = A;
d = b;
[A,p] = gpp(A);
for k = 1:n-1
    aux = b(k);
    b(k) = b(p(k));
    b(p(k)) = aux;
    for i = k+1:n
        b(i) = b(i) - A(i,k)*b(k);
    end
end
disp('Matricea rezultata dupa pivotare este: ');
disp(triu(A));
disp('Termenii liberi: ');
disp(b);
x = s_sup_tr(triu(A),b);
disp('Verificare solutie GPP: ');
disp(norm(B*x-d));