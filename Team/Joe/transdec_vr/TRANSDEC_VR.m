% Virtual Map of Environment
% This script was created to show how to calculate a virtual reality
% environment of the TRANSDEC based on a 2D matrix with the value of 
% elements equal to the depth at point X, Y.

% Create the initial map
vr_map = zeros(201, 151);

% Fill in the map
for i = -100:100   
    for j = 0:150        
        vr_map(i+101, j+1) = GetPoint(j, i);        
    end    
end

% get rid of black lines in the 3d plot
opengl software;
%opengl hardware;

% Generate a surface plot
surf(vr_map);

title('TRANDEC VR-MAP');

xlabel('width (ft)') % x-axis label
ylabel('height (ft)') % y-axis label
zlabel('depth (ft)') % x-axis label

colormap winter;