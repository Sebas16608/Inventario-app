#!/bin/bash

# Script de Quick Start para el Frontend

set -e  # Exit on error

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║         🚀 FRONTEND INVENTARIO APP - QUICK START        ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verificar si Node.js está disponible
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js no encontrado!${NC}"
    echo "Descargalo desde: https://nodejs.org/"
    exit 1
fi

echo -e "${GREEN}✅ Node.js $(node --version)${NC}"
echo -e "${GREEN}✅ NPM $(npm --version)${NC}"
echo ""

# Navegar al directorio frontend
cd "$(dirname "$0")/frontend" || exit 1

echo -e "${YELLOW}📦 Paso 1: Instalando dependencias...${NC}"
npm install --legacy-peer-deps
echo -e "${GREEN}✅ Dependencias instaladas${NC}"
echo ""

# Crear .env.local
echo -e "${YELLOW}📝 Paso 2: Configurando variables de entorno...${NC}"
if [ ! -f .env.local ]; then
    cp .env.example .env.local
    echo -e "${GREEN}✅ Archivo .env.local creado${NC}"
else
    echo -e "${YELLOW}⚠️  Archivo .env.local ya existe${NC}"
fi
echo ""

# Mostrar instrucciones
echo "╔════════════════════════════════════════════════════════╗"
echo "║                   ✅ LISTO PARA USAR                    ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo -e "${YELLOW}Para iniciar el servidor:${NC}"
echo -e "${GREEN}npm run dev${NC}"
echo ""
echo -e "${YELLOW}Luego abre:${NC}"
echo -e "${GREEN}http://localhost:3000${NC}"
echo ""
echo -e "${YELLOW}Credenciales de prueba (una vez que te registres):${NC}"
echo -e "${GREEN}Email: tu@email.com${NC}"
echo -e "${GREEN}Contraseña: tu_contraseña${NC}"
echo ""
echo -e "${YELLOW}Recuerda:${NC}"
echo -e "${GREEN}✓ El backend debe estar corriendo en http://localhost:8000${NC}"
echo -e "${GREEN}✓ Abre .env.local si necesitas cambiar URLs${NC}"
echo ""
