python <<EOF
sys.path.append('.')
from fsharpvim import FSAutoComplete
import vim
fsautocomplete = FSAutoComplete()
EOF

set omnifunc=fsharpcomplete#Complete

function! fsharpcomplete#Complete(findstart, base)
    if a:findstart == 1
        return col('.')
    else
        python vim.command("return %s" % fsautocomplete.complete(vim.eval("expand('%')"), vim.eval("line('.')"), vim.eval("col('.')")))
    endif
endfunction
