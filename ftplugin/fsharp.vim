" Vim filetype plugin
" Language:     F#
" Last Change:  Fri 18 May 2012 01:59:07 AM CEST
" Maintainer:   Gregor Uhlenheuer <kongo2002@googlemail.com>

if exists('b:did_ftplugin')
    finish
endif
let b:did_ftplugin = 1

python <<EOF
import vim
fsharp_dir = vim.eval("expand('<sfile>:p:h')")
sys.path.append(fsharp_dir)
from fsharpvim import FSAutoComplete
fsautocomplete = FSAutoComplete(fsharp_dir)
EOF

let s:cpo_save = &cpo
set cpo&vim

" enable syntax based folding
setl fdm=syntax

" comment settings
setl formatoptions=croql
setl commentstring=(*%s*)
setl comments=s0:*\ -,m0:*\ \ ,ex0:*),s1:(*,mb:*,ex:*),:\/\/\/,:\/\/

" make ftplugin undo-able
let b:undo_ftplugin = 'setl fo< cms< com< fdm<'

let s:candidates = [ 'fsi',
            \ 'fsi.exe',
            \ 'fsharpi',
            \ 'fsharpi.exe' ]

if !exists('g:fsharp_interactive_bin')
    let g:fsharp_interactive_bin = ''
    for c in s:candidates
        if executable(c)
            let g:fsharp_interactive_bin = c
        endif
    endfor
endif

function! s:launchInteractive(from, to)
    if !executable(g:fsharp_interactive_bin)
        echohl WarningMsg
        echom 'fsharp.vim: no fsharp interactive binary found'
        echom 'fsharp.vim: set g:fsharp_interactive_bin appropriately'
        echohl None
        return
    endif

    let tmpfile = tempname()
    echo tmpfile
    exec a:from . ',' . a:to . 'w! ' . tmpfile
    exec '!' . g:fsharp_interactive_bin '--gui- --nologo --use:"'.tmpfile.'"'
endfunction

com! -buffer -range=% Interactive call s:launchInteractive(<line1>, <line2>)

function! fsharp#Complete(findstart, base)
    if a:findstart == 1
        return col('.')
    else
        python << EOF
b = vim.current.buffer
row, col = vim.current.window.cursor
fsautocomplete.parse(b.name, True, '\n'.join(b))
vim.command("return %s" % fsautocomplete.complete(b.name, row - 1, col))
EOF
    endif
endfunction

let &cpo = s:cpo_save

" vim: sw=4 et sts=4
