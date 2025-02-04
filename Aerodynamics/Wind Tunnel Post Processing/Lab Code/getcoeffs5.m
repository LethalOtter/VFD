function matrix = getcoeffs5(filename)
    [tareavgs, runavgs] = avgs3(filename);
    matrix = zeros(size(runavgs,1), 8);
    for i = 1:size(runavgs,1)
        runavg = runavgs(i,:);
        tareavg = tareavgs(i,:);

    %     tarep = readmatrix('polynomial_tare.txt');
        %input some other basic information in SI units
        %wind tunnel speed in m/s
        rho = 1.1778;
        v = 30; %20;
        crd = .2286; %chord in m
        S = .2286 * 3 * .2286; %wing planform area in m^2(= b*c)
        
        %averages and measurement
        aoa = runavg(13);
    %     tareavg = zeros(1, 17);
    %     for i = 1:12
    %         tareavg(i) = polyval(tarep(i, :), runavg(13))
    %     end
        
        do = deg2rad(aoa);
        po = deg2rad(aoa);
    
        meas = runavg-tareavg;
        
        
        %splitting columns (1 = driver, 2 = passenger)
        fx1 = meas(1);
        fx2 = meas(7);
        fy1 = meas(2);
        fy2 = meas(8);
        fz1 = meas(3);
        fz2 = meas(9);
        qx1 = meas(4);
        qx2 = meas(10);
        qy1 = meas(5);
        qy2 = meas(11);
        qz1 = meas(6);
        qz2 = meas(12);
        fq1 = [fx1 fy1 fz1 qx1 qy1 qz1].';        
        fq2 = [fx2 fy2 fz2 qx2 qy2 qz2].';
      
        c = cos(po);
        s = sin(po);
        map1 = [-c -s 0 0 0 0 ;
                -s c 0 0 0 0 ;
                0  0 -1 0 0 0 ;
                0  0 0 -c -s 0 ;
                0  0 0 -s c 0 ;
                0  0 0 0  0 -1];
        
        pv = map1 * fq1;
        
        c = cos(po);
        s = sin(po);
        map2 = [-c  s 0 0 0 0;
                -s -c 0 0 0 0;
                 0  0 1 0 0 0;
                 0  0 0 -c  s 0;
                 0  0 0 -s c 0;
                 0  0 0  0  0 1];
        dv = map2 * fq2;
        
        L = dv(1) + pv(1);
        D = dv(2) + pv(2); 
        M = dv(6) + pv(6);
        
        CL = L / (.5 * rho * v^2 * S);
        CD = D / (.5 * rho * v^2 * S);
        CM = M / (.5 * rho * v^2 * S * crd);

        aoa = tareavg(13);
    
        vector = [aoa CL CD CM L D M CL/CD];
        matrix(i,:) = vector;
    end
end
