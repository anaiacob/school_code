% Rezolvare sisteme liniare cu gpc (verificare gpc)
n = 8;
A = randn(n,n);
b = randn(n,1);
B = A;
d = b;
[A,p,q] = gpc(A);
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
for k = n-1:-1:1
    aux = x(k);
    x(k) = x(q(k));
    x(q(k)) = aux;
end
disp('Verificare rezolvare sistem cu gpc: ');
disp(norm(B*x - d));