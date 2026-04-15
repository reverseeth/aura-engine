#!/bin/bash
SHELL_RC="$HOME/.zshrc"
[ -n "$BASH_VERSION" ] && SHELL_RC="$HOME/.bashrc"
grep -q "alias aura=" "$SHELL_RC" 2>/dev/null || echo "alias aura='cd ~/aura-engine && claude'" >> "$SHELL_RC"
