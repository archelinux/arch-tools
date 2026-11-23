vim.cmd.colorscheme("archevim")
assert(vim.g.colors_name == "archevim")
assert(require("lualine.themes.archevim").normal)
