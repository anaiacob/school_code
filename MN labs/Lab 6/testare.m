
k = 10;
compresie_dvs('baboon.bmp', k);
k = 20;
compresie_dvs('baboon.bmp', k);

disp('JQ: ');
m = 10;
n = 7; 
A = randn(m,n);
[f,g,U,V] = JQ(A);
f = [diag(f); zeros(m-n,n)];
g = [diag(g,1); zeros(m-n,n)];
S = f + g;
B = A - U*S*V';
disp('Verificare corectitudine rezultat JQ: ');
disp(norm(B));
