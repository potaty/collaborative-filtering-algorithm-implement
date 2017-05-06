
set encoding=utf8

syntax on 
set number
set ts=4
set sts=4
set sw=4
set ai
set ci 
set si


map <C-F9> :!g++ % -o %:r -g -Wall<CR>
map <C-F10> :!gdb %:r<CR>
