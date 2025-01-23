
alfa = 2;
beta = 1;
gamma = 1;
x_adevarat = [alfa; beta; gamma];
x_adevarat = x_adevarat / norm(x_adevarat); 

m = 20;     
s = 0.3;    
if abs(alfa) > abs(beta)
  yy = 6*rand(m,1) - 3; 
  xx = (-gamma - beta*yy)/alfa;
else
  xx = 6*rand(m,1) - 3;
  yy = (-gamma - alfa*xx)/beta;
end

xx = xx + s*randn(m,1);
yy = yy + s*randn(m,1);

plot(xx, yy, '*g', 'LineWidth', 1, 'MarkerSize', 8) 
hold on;
A = [xx yy ones(20,1)];
[U,S,V] = svd(A);
l = V(:,end);
A = [xx ones(20,1)];
rezid = A\yy;  
plot(xx, xx*rezid(1) + rezid(2));        
plot(xx, -1/l(2) * (l(1) * xx + l(3)));  
plot(xx, -1/x_adevarat(2)*(xx*x_adevarat(1) + x_adevarat(3))); 
hold off;
legend('Esantion','Adevarat','CMMP','CMMPT');
