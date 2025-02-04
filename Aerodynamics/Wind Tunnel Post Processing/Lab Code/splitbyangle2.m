function [bps] = splitbyangle2(fid)
    m = readmatrix(fid);
    bps = 1;
    for i = 1:size(m,1)-1
        if abs(m(i+1,13) - m(i,13)) > 2 && (m(i,15) < 100 && m(i+1,15) < 100)
            bps = [bps i+1];
        end
    end
    bps = [bps size(m,1)];
end