n=3;
A=randn(n);
A1=A;
A2=[1 2 7;3 9 2; 5 5 1];
A3=A2;
A4=A3;
b=rand(n,1);
L=tril(A);
x=s_inf_tr(L,b);
norm(L*x-b)
U=triu(A1);
y=s_sup_tr(U,b);
norm(U*y-b)
z=g(A2);
disp(z);
[A3,p]=gpp(A2)
[A4,p,q]=gpc(A2)
