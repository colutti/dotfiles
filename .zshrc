export PATH="~/.fzf/bin/:$PATH"


# Enable Powerlevel10k instant prompt. Should stay close to the top of ~/.zshrc.
# Initialization code that may require console input (password prompts, [y/n]
# confirmations, etc.) must go above this block; everything else may go below.
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

if [[ -f "/opt/homebrew/bin/brew" ]] then
  # If you're using macOS, you'll want this enabled
  eval "$(/opt/homebrew/bin/brew shellenv)"
fi

# Set the directory we want to store zinit and plugins
ZINIT_HOME="${XDG_DATA_HOME:-${HOME}/.local/share}/zinit/zinit.git"

# Download Zinit, if it's not there yet
if [ ! -d "$ZINIT_HOME" ]; then
   mkdir -p "$(dirname $ZINIT_HOME)"
   git clone https://github.com/zdharma-continuum/zinit.git "$ZINIT_HOME"
fi

# Source/Load zinit
source "${ZINIT_HOME}/zinit.zsh"

# Add in Powerlevel10k
zinit ice depth=1; zinit light romkatv/powerlevel10k

# Add in zsh plugins
zinit light zsh-users/zsh-syntax-highlighting
zinit light zsh-users/zsh-completions
zinit light zsh-users/zsh-autosuggestions
zinit light Aloxaf/fzf-tab
#
# Load completions
autoload -Uz compinit && compinit

zinit cdreplay -q

# To customize prompt, run p10k configure or edit ~/.p10k.zsh.
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh
# History
HISTSIZE=5000
HISTFILE=~/.zsh_history
SAVEHIST=$HISTSIZE
HISTDUP=erase
setopt appendhistory
setopt sharehistory
setopt hist_ignore_space
setopt hist_ignore_all_dups
setopt hist_save_no_dups
setopt hist_ignore_dups
setopt hist_find_no_dups

# Completion styling
zstyle ':completion:*' matcher-list 'm:{a-z}={A-Za-z}'
zstyle ':completion:*' list-colors "${(s.:.)LS_COLORS}"
zstyle ':completion:*' menu no
zstyle ':fzf-tab:complete:cd:*' fzf-preview 'ls --color $realpath'
zstyle ':fzf-tab:complete:__zoxide_z:*' fzf-preview 'ls --color $realpath'

# Aliases
alias ls='eza --long --header --icons --git --group-directories-first'
alias ll='eza -la --group-directories-first --header --icons --git'
alias vim='nvim'
alias c='clear'


alias temp='(
  echo "=== CPU Temperatures ==="
  sensors | grep -E "^(CPUTIN|Tctl|Core|CPU|SYSTIN)" | awk "{print \$1\": \"\$2}"
  echo
  echo "=== GPU Temperatures ==="
  sensors | grep -E "^(edge|junction|mem)" | awk "{print \$1\": \"\$2}"
  echo
  echo "=== Fan Speeds ==="
  sensors | grep -E "^(fan)" | awk "{print \$1\": \"\$2}"
)'

# Alias para gerenciar sessões tmux com fzf
alias tms='tmux_select_function'

tmux_select_function() {
    # Define a variável DIR como o diretório que você quer listar
    DIR="$HOME/projects/"

    # Lista todas as pastas dentro de DIR e usa fzf para selecionar uma
    selected_folder=$(find "$DIR" -mindepth 1 -maxdepth 1 -type d,l | fzf --height 40% --reverse --border --prompt="Selecione uma pasta: ")

    # Se uma pasta foi selecionada
    if [[ -n "$selected_folder" ]]; then
        folder_name=$(basename "$selected_folder")

        # Verifica se já existe uma sessão tmux com o nome da pasta
        if ! tmux has-session -t "$folder_name" 2>/dev/null; then
            # Cria uma nova sessão tmux com o nome da pasta e anexa a ela
            tmux new-session -s "$folder_name" -c "$selected_folder"
        else
            # Anexa à sessão existente
            tmux attach-session -t "$folder_name"
        fi
    fi
}

# Shell integrations
[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh
eval "$(zoxide init --cmd cd zsh)"
