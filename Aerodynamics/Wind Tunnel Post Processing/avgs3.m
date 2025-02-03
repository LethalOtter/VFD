function [tareavgs, runavgs] = avgs3(file)
    bps = splitbyangle2(file)
    m = readmatrix(file);
    if abs(m(1,13)) < 0.1
        m(:,15) = m(:,15);
    end
    tareavgs = [];
    runavgs = [];
    for i = 1:length(bps)-1
        start = bps(i);
        stop = bps(i+1);
        A = m(start:(stop-1), :)
        marker = mean(A(1:10,15))
        for ii = 1:size(A,1)
            if abs(A(ii, 15)-marker)>300
                disp(A(ii,15))
                bp1 = ii;
                break
            end
        end
        for jj = bp1+1:size(A,1)
            if abs(A(jj, 15)-marker)<300
                disp(A(jj,15))
                bp2 = jj;
                break
            end
        end
        size(A)
        bpss = [bp1 bp2]
        tareavgs1 = mean(A(1:(bp1-1),:));
        tareavgs2 = mean(A(bp2:end,:));
        runavgs(i,:) = mean(A(bp1:bp2-1, :));

        tareavgs(i,:) = (tareavgs1 + tareavgs2) ./2;
    end
end
