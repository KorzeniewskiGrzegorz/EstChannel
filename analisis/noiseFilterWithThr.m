function [filtered_x, filtered_y] = noiseFilterWithThr(x,y, threshold)

    s = find(y > threshold);
    filtered_y = y(s);
    filtered_x = x(s);

end

