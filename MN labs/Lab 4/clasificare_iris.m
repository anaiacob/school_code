% Clasificare IRIS cu CMMP

load('iris.mat');
N1 = 50;    % numar puncte in prima clasa
N2 = 100;   % numar puncte in a doua clasa
ell = 4;    % dimensiunea vectorilor de clasificat 2*(lungime+latime)

%   tip 1 / tip 2+3

% generare vectori citit din iris.mat
V1 = iris_data(1:50,1:4);
V2 = iris_data(51:150,1:4);
V1 = V1';
V2 = V2';

% formeaza si rezolva problema CMMP
A = [V1' ones(N1,1); V2' ones(N2,1)];
b = [ones(N1,1); -ones(N2,1)];
x = A \ b;      % aici se rezolva problema CMMP 
c = x(1:ell);
d = x(ell+1);

% Verificam cati vectori de antrenare sunt clasificati corect in fiecare clasa
matrice_confuzie = zeros(2);
for i = 1 : N1
  if sign(c'*V1(:,i) + d) == 1
    matrice_confuzie(1,1) = matrice_confuzie(1,1) + 1;
  else
    matrice_confuzie(1,2) = matrice_confuzie(1,2) + 1;
  end
end
for i = 1 : N2
  if sign(c'*V2(:,i) + d) ~= 1
    matrice_confuzie(2,2) = matrice_confuzie(2,2) + 1;
  else
    matrice_confuzie(2,1) = matrice_confuzie(2,1) + 1;
  end
end
disp('Matrice coeziune pentru tip1 / tip2+3: ');
disp(matrice_confuzie); %se observa ca este perfect separat 

%   tip 2 / tip 1+3

% generare vectori citit din iris.mat
V1 = iris_data(51:100,1:4);
V2 = [iris_data(1:50,1:4);iris_data(101:150,1:4)];
V1 = V1';
V2 = V2';

% formeaza si rezolva problema CMMP
A = [V1' ones(N1,1); V2' ones(N2,1)];
b = [ones(N1,1); -ones(N2,1)];
x = A \ b;      % aici se rezolva problema CMMP 
c = x(1:ell);
d = x(ell+1);

% Verificam cati vectori de antrenare sunt clasificati corect in fiecare clasa
matrice_confuzie = zeros(2);
for i = 1 : N1
  if sign(c'*V1(:,i) + d) == 1
    matrice_confuzie(1,1) = matrice_confuzie(1,1) + 1;
  else
    matrice_confuzie(1,2) = matrice_confuzie(1,2) + 1;
  end
end
for i = 1 : N2
  if sign(c'*V2(:,i) + d) ~= 1
    matrice_confuzie(2,2) = matrice_confuzie(2,2) + 1;
  else
    matrice_confuzie(2,1) = matrice_confuzie(2,1) + 1;
  end
end
disp('Matrice coeziune pentru tip2 / tip1+3: ');
disp(matrice_confuzie);

%   tip 2 / tip 1+3

% generare vectori citit din iris.mat
V1 = iris_data(101:150,1:4);
V2 = iris_data(1:100,1:4);
V1 = V1';
V2 = V2';

% formeaza si rezolva problema CMMP
A = [V1' ones(N1,1); V2' ones(N2,1)];
b = [ones(N1,1); -ones(N2,1)];
x = A \ b;      % aici se rezolva problema CMMP 
c = x(1:ell);
d = x(ell+1);

% Verificam cati vectori de antrenare sunt clasificati corect in fiecare clasa
matrice_confuzie = zeros(2);
for i = 1 : N1
  if sign(c'*V1(:,i) + d) == 1
    matrice_confuzie(1,1) = matrice_confuzie(1,1) + 1;
  else
    matrice_confuzie(1,2) = matrice_confuzie(1,2) + 1;
  end
end
for i = 1 : N2
  if sign(c'*V2(:,i) + d) ~= 1
    matrice_confuzie(2,2) = matrice_confuzie(2,2) + 1;
  else
    matrice_confuzie(2,1) = matrice_confuzie(2,1) + 1;
  end
end
disp('Matrice coeziune pentru tip3 / tip1+2: ');
disp(matrice_confuzie);
