function [max, idx] = vmax (v)
  # ayuda: vmax(v) devuelve el m�ximo valor de un vector 
  # y la posici�n que ocupa

  idx = 1;
  max = v (1);
  for i = 2:length (v)
    if (v (i) > max)
      max = v (i);
      idx = i;
    endif
  endfor
endfunction
