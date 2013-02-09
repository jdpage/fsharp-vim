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
row = row - 1
print 'parse(%s, True, %s)' % (b.name, b[0])
fsautocomplete.parse(b.name, True, '\n'.join(b))
print 'complete(%s, %d, %d)' % (b.name, row, col)
l = fsautocomplete.complete(b.name, row, col) 
print 'finished: %s' % l
vim.command("return %s" % l)
EOF
    endif
endfunction

