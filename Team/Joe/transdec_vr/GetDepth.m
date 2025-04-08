function [ depth ] = GetDepth( X )
%GetDepth Gets the depth from the confines of the TRANSDEC
%   This function will return the depth of a point based on the magnitude
%   of the X-Y point.  The magnitude is needed because this will get the
%   value based on a circular profile of depth
    
    % Check to see if this is the 1 foot ridge
    if (X > 77 && X < 80)
        depth = -15;
    % Check if this is the flat area of the TRANSDEC
    elseif (X >= 80)
        depth = -16;      
    else % We are in the inner bowl so we need to calculate the depth
        % Calculate the depth based on the trendline equation (4th order
        % poly)
        tmpVal = -0.0000002 * X ^ 4 + 0.00008 * X * X * X ...
                 - 0.0013 * X * X + 0.0356 * X - 37.993;        
        % Since the pool isn't shallower than 15 feet make it no more than
        % -15 feet
        if (tmpVal > -15)
            depth = -15;
        else
            depth = tmpVal;
        end             
    end
    
end

