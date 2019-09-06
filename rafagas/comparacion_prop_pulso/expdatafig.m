fig = openfig('raf0_1.fig');
fig = gcf;

axObjs = fig.Children;
dataObjs = axObjs.Children;

x = dataObjs(1).XData;
y = dataObjs(1).YData;


figure
plot(x,y)

raf0_1= y;