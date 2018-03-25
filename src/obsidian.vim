" Vim syntax file
" Language: Obsidian
" Maintainer: Alex Gajewski
" Latest Revision: 25 March 2018

if exists("b:current_syntax")
  finish
endif

syn keyword obsidianKeyword do end

syn match obsidianNumber '\v-?[0-9]+'
syn match obsidianNumber '\v-?[0-9]+\.[0-9]+'

syn match obsidianString '\v"([^"\\]|\\.)*"'
syn match obsidianString "\v'([^'\\]|\\.)*'"

syn match obsidianSymbol '\v\@[_a-zA-Z][_a-zA-Z0-9]*[?]?'

syn match obsidianIdentifier '\v[_a-zA-Z$][_a-zA-Z0-9]*[?]?'
syn match obsidianBinaryIdentifier '\v\~[_a-zA-Z][_a-zA-Z0-9]*[?]?'

syn keyword obsidianTodo contained TODO FIXME XXX NOTE
syn match obsidianComment '\v#.*$'

let b:current_syntax = "obsidian"

hi def link obsidianKeyword Statement
hi def link obsidianNumber Number
hi def link obsidianString String
hi def link obsidianSymbol Identifier
hi def link obsidianIdentifier Symbol
hi def link obsidianBinaryIdentifier Statement
hi def link obsidianTodo Todo
hi def link obsidianComment Comment
