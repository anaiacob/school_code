%genereaza o matrice dif de mat diag care sa aiba val proprii elementele
%vec v=randn(4,1) valideaza ca val proprii sunt cele corecte

v=randn(4,1)
A=diag(v);
T=randn(4);
A=T*A*inv(T);
disp(A);
