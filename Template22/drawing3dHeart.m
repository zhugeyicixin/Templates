close all;
x_range=[-0.5:0.002:0.5];
y_range=[-1.5:0.002:1.5];
z_range=[-1:0.02:1.26];
surface=zeros(1e6,3);
index=1;
warning off;
% x=solve('(x^2 + (6*y^2)/4 + z^2 - 1)^3 - x^2*z^3 - (9*y^2*z^3)/80=0');
% for z=z_range
%     z
%     for y=y_range
%         root_x = subs(x);
%         tmp_x=ones(10,1)*10;
%         index2 = 1;
%         for tmp2_x = [1:length(root_x)]
%             if abs(imag(root_x(tmp2_x))) < 1e-4
%                 surface(index,:)=[real(root_x(tmp2_x)),y,z];
%                 index = index + 1;                
%             end
%         end
%     end
% end

y=solve('(x^2 + (6*y^2)/4 + z^2 - 1)^3 - x^2*z^3 - (9*y^2*z^3)/80=0','y');
for z=z_range
    z
    for x=x_range
        root_y = subs(y);
        tmp_y=ones(10,1)*10;
        index2 = 1;
        for tmp2_y = [1:length(root_y)]
            if abs(imag(root_y(tmp2_y))) < 1e-4
                surface(index,:)=[x,real(root_y(tmp2_y)),z];
                index = index + 1;                
            end
        end
    end
end

figure(1);
lenSurface=surface(:,1).^2 + surface(:,2).^2 + surface(:,3).^2;
surface=surface(lenSurface>0,:);
scatter3(surface(:,1),surface(:,2),surface(:,3));

% code to generate blocks
% surface4(:,1)=roundn(surface4(:,1)/2,-2)*2;
% surface4(:,2)=roundn(surface4(:,2)/2,-2)*2;
% surface4=unique(surface4,'rows');
% surface3=surface3(find(surface3(:,1)~=Inf),:);
% surface3=surface3(find(surface3(:,1)~=-Inf),:);

% % figure(2);
% lenSurface=surface2(:,1).^2 + surface2(:,2).^2 + surface2(:,3).^2;
% surface2=surface2(lenSurface>0,:);
% scatter3(surface2(:,1),surface2(:,2),surface2(:,3));

% postreat
% surface3=surface2;
% surface4=surface3;
% for i=[1:size(surface3,1)]
%     if surface3(i,2)~=0
%         surface4(i,:)=[0,0,0];
%     end
% end
% figure(3);
% scatter3(surface4(:,1),surface4(:,2),surface4(:,3));
%%  
% check the completeness of surface
% surface5 is the initial result of calculation on the 0.02-interval grid
x_range=[-1.14:0.02:1.14];
y_range=[-0.84:0.02:0.84];
projection = zeros(1e6,3);
index=1;
for x=x_range
    for y=y_range
        tmp1=find(abs(surface5(:,1)-x)<1e-3);
        tmp2=find(abs(surface5(:,2)-y)<1e-3);
        tmp3=intersect(tmp1, tmp2);
        if length(tmp3)>0
            projection(index,:)=[x,y,max(surface5(tmp3,3))];
            index = index + 1;
        end
    end
end
lenSurface=projection(:,1).^2 + projection(:,2).^2 + projection(:,3).^2;
projection=projection(lenSurface>0,:);
scatter3(projection(:,1),projection(:,2),projection(:,3));

%%
% fullfill the upper surface of the object
tmp5=zeros(1e6,3);
index=1;
for y=y_range
    tmp=projection(find(abs(projection(:,2)-y)<1e-3),:);
    tmp1=tmp(find(tmp(:,3)>0),:);
    tmp2=tmp(find(tmp(:,3)<0),:);
    xx=[roundn(min(tmp),-2):0.02:roundn(max(tmp),-2)]';
    tmp3=[xx,ones(length(xx),1)*y,spline(tmp1(:,1),tmp1(:,3),xx)];
    tmp4=sortrows([tmp1;tmp3],1);
    tmp5(index:index+length(tmp4)-1,:)=tmp4;
    index = index + length(tmp4);
end
lenSurface=tmp5(:,1).^2 + tmp5(:,2).^2 + tmp5(:,3).^2;
tmp5=tmp5(lenSurface>0,:);
tmp5=unique(tmp5,'rows');
surface6=[surface5;tmp5];

%%
% check the completeness of surface
x_range=[-1.14:0.02:1.14];
y_range=[-0.84:0.02:0.84];
projection = zeros(1e6,3);
index=1;
for x=x_range
    for y=y_range
        tmp1=find(abs(surface6(:,1)-x)<1e-3);
        tmp2=find(abs(surface6(:,2)-y)<1e-3);
        tmp3=intersect(tmp1, tmp2);
        if length(tmp3)>0
            projection(index,:)=[x,y,min(surface6(tmp3,3))];
            index = index + 1;
        end
    end
end
lenSurface=projection(:,1).^2 + projection(:,2).^2 + projection(:,3).^2;
projection=projection(lenSurface>0,:);
scatter3(projection(:,1),projection(:,2),projection(:,3));
% projection=projection(find(projection(:,3)>0.8),:);
% scatter3(projection(:,1),projection(:,2),projection(:,3));

%%
% fullfill the bottom surface of the object
tmp5=zeros(1e6,3);
index=1;
for y=y_range
    tmp=projection(find(abs(projection(:,2)-y)<1e-3),:);
    tmp1=tmp(find(tmp(:,3)<1),:);
    tmp2=tmp(find(tmp(:,3)>1),:);
    xx=[roundn(min(tmp),-2):0.02:roundn(max(tmp),-2)]';
    tmp3=[xx,ones(length(xx),1)*y,spline(tmp1(:,1),tmp1(:,3),xx)];
    tmp4=sortrows([tmp1;tmp3],1);
    tmp5(index:index+length(tmp4)-1,:)=tmp4;
    index = index + length(tmp4);
end
lenSurface=tmp5(:,1).^2 + tmp5(:,2).^2 + tmp5(:,3).^2;
tmp5=tmp5(lenSurface>0,:);
tmp5=unique(tmp5,'rows');
surface7=[surface6;tmp5];

%%
% check the completeness of surface
x_range=[-1.14:0.02:1.14];
y_range=[-0.84:0.02:0.84];
projection = zeros(1e6,3);
index=1;
for x=x_range
    for y=y_range
        tmp1=find(abs(surface7(:,1)-x)<1e-3);
        tmp2=find(abs(surface7(:,2)-y)<1e-3);
        tmp3=intersect(tmp1, tmp2);
        if length(tmp3)>0
            projection(index,:)=[x,y,min(surface7(tmp3,3))];
            index = index + 1;
        end
    end
end
lenSurface=projection(:,1).^2 + projection(:,2).^2 + projection(:,3).^2;
projection=projection(lenSurface>0,:);
scatter3(projection(:,1),projection(:,2),projection(:,3));
