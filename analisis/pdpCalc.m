function [pdp] = pdpCalc(h,Fs,plotMode,k,normalize,noiseThr)

    %%% PDP calculation of each realization
    for i=1:k
        hc=h(i,:)';
        ryy= hc*hc';
        pdpc(i,:) = diag(ryy);
        if normalize == 1
            pdpc(i,:) = pdpc(i,:)/max(pdpc(i,:));
        end
        
    end
    
    %%%%%% data align to first sample above threshold
    for i=1:k
        idx(i) = find(pdpc(i,:) > noiseThr , 1); 
    end


    idxref = 10; % fixed number, distance depended
    if 1==1
       for i=1:k
           if idx(i)>idxref
               pdpc(i,:) = [pdpc(i,idx(i)-idxref+1:end) zeros(1,idx(i)-idxref)];
           else
               pdpc(i,:) = [zeros(1,idxref-idx(i)) pdpc(i,1:end-(idxref-idx(i)) )];
           end
       end
    end

  
    if plotMode == 1 % plot mode for each pdp before mean
          t = 0:1/Fs:length(pdpc(1,:))/Fs -1/Fs;
        leg=cell(1,k);

        figure
        hold on
        grid on
        for i=1:k
                stem(t,pdpc(i,:))
                title('PDP ')
                leg{i} = sprintf('n = %i',i);
        end
        hold off
        legend(leg)
    end
    
%%%% estimating pdp - mean
pdp = mean(pdpc);

pdp = pdp(1:50); % pdp truncate

end

