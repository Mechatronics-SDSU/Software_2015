function [ depth ] = GetPoint( X, Y )
%GetPoint Gets the depth from point X,Y
%   This function gets the depth at point X, Y where X is the length of the
%   pool and Y is the height.  Both are based on the deepest part of the
%   pool being X = 0 and Y = 0

    % The differece in circle radii between the outer 'elipse' and the inner bowl
    ADDITIONAL_RADII = 60;
    
    % The radii of the circle that make up the 'elipse'
    BIG_CIRCLE_RADII = 160; 
    
    yOuter = abs(Y) + ADDITIONAL_RADII;
    
    % Magnitude to determine if we are out of the environment bounds
    magOuter = sqrt(X^2 + yOuter^2);
    
    if (magOuter > BIG_CIRCLE_RADII) % This is outside the pool            
        depth = 0;        
    else % This is within the pool
        % Magnitude to determine what value we should calculate the depth for
        magXY = sqrt(X*X + Y*Y);        
        % Calculate the depth
        depth = GetDepth(magXY);        
    end

end

