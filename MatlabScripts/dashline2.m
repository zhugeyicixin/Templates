function dashline2(dash_x,dash_y)
    dash_x=x;
    dash_y=y;
    dash_rangeX = max(dash_x) - min(dash_x);
    dash_rangeY = max(dash_y) - min(dash_y);
    dash_Q = [diff(dash_x) / dash_rangeX; diff(dash_y) / dash_rangeY];
    dash_L = [0, cumsum(sqrt(sum(dash_Q .* dash_Q)))];
    dash_L = (length(dash_L) / dash_L(end)) * dash_L;
    dash_a = 5;  % start point
    dash_b = 1;  % gap width
    dash_c = 6; % gap frequency
    index   = rem(round(dash_L) + dash_a, dash_c) <= dash_b;
    yDashed = dash_y;
    yDashed(index) = NaN;
    plot(dash_x, yDashed,'linewidth',2);
end