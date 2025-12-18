#!/usr/bin/env bash
set -e

if [ ! -d "mcp-opennutrition" ]; then
    git clone https://github.com/deadletterq/mcp-opennutrition.git
fi

cd mcp-opennutrition
npm install
npm run build