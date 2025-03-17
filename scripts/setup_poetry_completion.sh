#!/bin/bash
# Script to set up Poetry shell completions for zsh

# Generate completions script
mkdir -p ~/.zfunc
poetry completions zsh > ~/.zfunc/_poetry

# Add to .zshrc if not already there
if ! grep -q "fpath+=~/.zfunc" ~/.zshrc; then
  echo "" >> ~/.zshrc
  echo "# Poetry completions" >> ~/.zshrc
  echo "fpath+=~/.zfunc" >> ~/.zshrc
  echo "autoload -Uz compinit && compinit" >> ~/.zshrc
  echo "Added Poetry completions to ~/.zshrc"
  echo "Please restart your shell or run 'source ~/.zshrc' to activate"
else
  echo "Poetry completions already set up in ~/.zshrc"
fi

echo "Poetry tab completion setup complete!"
echo "Please restart your terminal or run the following commands in zsh:"
echo ""
echo "  fpath+=~/.zfunc"
echo "  autoload -Uz compinit && compinit"