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
        python << EOF
b = vim.current.buffer
row, col = vim.current.window.cursor
fsautocomplete.parse(b.name, True, '\n'.join(b))
vim.command("return %s" % fsautocomplete.complete(b.name, row, col))
EOF
    endif
endfunction

