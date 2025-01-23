n = 8;
A = randn(n);
A = A'*A; 
b = randn(n,1);


disp('Crout: ');
B = crout(A);
L = tril(B);
U = triu(B,1) + eye(n);
disp('Matricea L: ');
disp(L);
disp('Matricea U: ');
disp(U);
disp('Verificare corectitudine Crout A = L*U: ');
disp(norm(A - L*U));
disp('Verificare rezolvare sistem liniar cu Ax=b: ');
y = s_inf_tr(L,b);
x = s_sup_tr(U,y);
disp(norm(A*x - b));
D = tril(B) - tril(B,-1);
L = L*inv(D);
disp('Verificare corectitudine A = L*D*U: ');
disp(norm(A - L*D*U));


disp('Cholesky: ');
B = cholesky(A);
L = tril(B);
disp('Matricea L dupa factorizare: ');
disp(L);
disp('Verificare corectitudine rezultat A = L*L^t: ' );
disp(norm(A - L*L'));
disp('Verificare rezolvare sistem liniar cu Ax=b: '); 
y = s_inf_tr(L,b);
x = s_sup_tr(L',y);
disp(norm(A*x - b));

disp(' Inversa U si L: ');
U = triu(A);
L = tril(A);
X = uinv(U);
disp('Verificare inv(U): ');
disp(norm(X - inv(U)));
Y = linv(L);
disp('Verificare inv(L): ');
disp(norm(Y - inv(L)));

disp('Inversa folosind GPP: ');
X = inv_gpp(A);
disp('Verificare corectitudine inversa: ');
disp(norm(X - inv(A)));

disp('Determinantul: ')
B = crout(A);
L = tril(B);
U = triu(B,1) + eye(n);
deU = 1;
for i = 1:n
    deU = deU * U(i,i);
end
deL = 1;
for i = 1:n
    deL = deL*L(i,i);
end
disp('Metoda calcularii cu factorizarea LU: ');
disp(deL*deU);
disp('Metoda calcularii cu GPP: ');
disp(det(A));
disp('Verificarea rezultatului: ')
disp(deL*deU - det(A));
