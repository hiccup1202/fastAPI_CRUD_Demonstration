#!/bin/bash
# Coverage script for the Product Management API

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔍 Running pytest with coverage...${NC}"

# Activate virtual environment if not already active
if [ -z "$VIRTUAL_ENV" ]; then
    source venv/bin/activate
fi

# Run tests with coverage
python -m pytest tests/ \
    --cov=src \
    --cov-report=term-missing \
    --cov-report=html \
    --cov-report=xml \
    --cov-fail-under=75 \
    -v

echo -e "\n${GREEN}✅ Coverage reports generated:${NC}"
echo -e "${YELLOW}📊 Terminal report: See above${NC}"
echo -e "${YELLOW}🌐 HTML report: htmlcov/index.html${NC}"
echo -e "${YELLOW}📄 XML report: coverage.xml${NC}"

echo -e "\n${BLUE}📱 To view HTML report in browser:${NC}"
echo -e "python -m http.server 8080 --directory htmlcov"
echo -e "Then open: http://localhost:8080"

echo -e "\n${BLUE}🎯 Coverage Summary:${NC}"
python -c "
import xml.etree.ElementTree as ET
try:
    tree = ET.parse('coverage.xml')
    root = tree.getroot()
    line_rate = float(root.get('line-rate', 0)) * 100
    branch_rate = float(root.get('branch-rate', 0)) * 100
    print(f'Line Coverage: {line_rate:.1f}%')
    print(f'Branch Coverage: {branch_rate:.1f}%')
except:
    print('XML report not found')
"