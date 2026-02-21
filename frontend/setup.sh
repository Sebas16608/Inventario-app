#!/bin/bash

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   Instalación Frontend Invorax        ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""

# Verificar si Node.js está instalado
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js no está instalado${NC}"
    echo "Por favor instala Node.js 18+ desde https://nodejs.org/"
    exit 1
fi

echo -e "${YELLOW}Node.js encontrado:${NC} $(node --version)"
echo -e "${YELLOW}NPM encontrado:${NC} $(npm --version)"
echo ""

# Entrar al directorio frontend
cd "$(dirname "$0")" || exit 1

echo -e "${YELLOW}📦 Instalando dependencias...${NC}"
npm install

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Dependencias instaladas correctamente${NC}"
else
    echo -e "${RED}❌ Error al instalar dependencias${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}📝 Configurando archivo .env.local...${NC}"

if [ ! -f .env.local ]; then
    cp .env.example .env.local
    echo -e "${GREEN}✅ Archivo .env.local creado${NC}"
else
    echo -e "${YELLOW}⚠️  Archivo .env.local ya existe${NC}"
fi

echo ""
echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   ✅ Instalación completada!          ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}Para iniciar el servidor de desarrollo:${NC}"
echo -e "${GREEN}npm run dev${NC}"
echo ""
echo -e "${YELLOW}La app estará disponible en:${NC}"
echo -e "${GREEN}http://localhost:3000${NC}"
