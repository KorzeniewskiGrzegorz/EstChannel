function [pdp] = pdpCalc(h,Fs,plotMode,k,normalize,noiseThr,idxref)
%[pdp,piki] = pdpCalc(h,Fs,plotMode,k,normalize,noiseThr,idxref)
    %idxref  fixed number, distance depended
    %%% PDP calculation of each realization
    for i=1:k
        hc=h(i,:)';
        ryy= hc*hc';
        pdpc(i,:) = diag(ryy);
        %piki(i)=max(pdpc(i,:));
        if normalize == 1
            pdpc(i,:) = pdpc(i,:)/max(pdpc(i,:));
        end
        
    end
    
   % piki=max(piki);
    
    for i=1:k
        %[v, idx(i)] = max(pdpc(i,:)); %%%%%% data align to its max

        s = find(pdpc(i,:) > noiseThr); %%%%%% data align to first component over thrs
        idx(i) = s(1);

    end

    preAlignIdx=10;
    for i=1:k
       if idx(i)>preAlignIdx
           pdpc(i,:) = [pdpc(i,idx(i)-preAlignIdx+1:end) zeros(1,idx(i)-preAlignIdx)];
       else
           pdpc(i,:) = [zeros(1,preAlignIdx-idx(i)) pdpc(i,1:end-(preAlignIdx-idx(i)) )];
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
            title('PDP all')
            leg{i} = sprintf('n = %i',i);
        end
        hold off
        legend(leg)
        
        for i=1:k
            figure
            
            pdpcT(i,:) = pdpc(i,1:50);
             t = 0:1/Fs:length(pdpcT(i,:))/Fs -1/Fs;
            stem(t,pdpcT(i,:))
            title('PDP single')
            grid on
        end
        
        
    end
    
%%%% estimating pdp - mean
    pdp = mean(pdpc);

    pdp = pdp(1:50); % pdp truncate

    idx(i) = find(pdp > noiseThr , 1); 

    %idxref  fixed number, distance depended

   if idx(i)>idxref
       pdp = [pdp(idx(i)-idxref+1:end) zeros(1,idx(i)-idxref)];
   else
       pdp = [zeros(1,idxref-idx(i)) pdp(1:end-(idxref-idx(i)) )];
   end



end

