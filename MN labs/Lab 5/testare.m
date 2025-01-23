
tol = 10^(-8);
maxiter = 1000;
n = 7;
v = randn(n,1);  
disp('v = ');
disp(v);
A = diag(v);     
T = randn(n);
A = T*A*inv(T);  
y = randn(n,1); 

disp('Metoda puterii: ');
y = MP(A,tol,maxiter,y); 
[U,V] = eig(A);
disp('U = ');            
disp(U);
disp('V = ');            
disp(V);
maxim = 0;               
pozitie = 0;
for i = 1:n
    if abs(V(i,i)) > maxim
        maxim = abs(V(i,i));
        pozitie = i;
    end
end
disp('Pozitie valorii proprii dominante este: ');
disp(pozitie);           
disp('Din MP y = ');
disp(y);
disp('Verificare corectitudine rezultat: ');
disp(norm(abs(U(:,pozitie))-abs(y)));

disp('Metoda puterii inverse: ');
yi = randn(n,1);
yi  = MPI(A,tol,maxiter,yi);
disp('U = ');             
disp(U);
disp('V = ');            
disp(V);
disp('Verificarea rezultatului se face vizual: ');
disp('Din MPI yi = ');
disp(yi);                

disp('Algoritmul HQ: ');
disp('Matrice reala: ');
disp('A = ');
disp(A);
[Q,H]=HQ(A);
disp('Matricea Hessenberg rezultata: ');
disp(H);
disp('Verificare corectitudine rezultat: ');
disp(norm(H-hess(A)));

disp('Matrice complexa: ');
B = complex(randn(n),randn(n));
disp('B = ');
disp(B);
[Q,H]=HQ(B);
disp('Matricea Hessenberg rezultata: ');
disp(H);
disp('Verificare corectitudine rezultat: ');
disp(norm(H-hess(B)));  

disp('QR: ');
S = QR(A,tol,maxiter);
disp('Forma Schur este S = ');
disp(S);
disp('Folosind o functie Matlab: ')
A_s=schur(A);          
disp(A_s);              
disp(norm(abs(S) - abs(A_s)));

