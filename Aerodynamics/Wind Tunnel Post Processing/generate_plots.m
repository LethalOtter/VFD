clc; close all; clear all;
A = getcoeffs5('Test1_30msDataRun000.txt')


figure(1)
plot(A(:,1), A(:,3), 'k*')
hold on
title('CD')
xlabel('aoa')

figure(2)
plot(A(:,1), A(:,2), 'k*')
hold on
title('CL')
xlabel('aoa')

figure(3)
plot(A(:,1), A(:,4), 'k*')
hold on
title('CM')
xlabel('aoa')

figure(4)
hold on
plot(A(:,1), A(:,8), 'k*')
xlabel('aoa')
title('CL/CD')
