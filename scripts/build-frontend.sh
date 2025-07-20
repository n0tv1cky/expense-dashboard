#!/bin/bash

# Expense Tracker React App Build Script

echo "🏗️  Building React Frontend for Production..."
echo ""

cd frontend-react

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Build the app
echo "⚛️  Building React app..."
npm run build

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Build completed successfully!"
    echo "📁 Built files are in: frontend-react/dist/"
    echo ""
    echo "🚀 To preview the build locally:"
    echo "   cd frontend-react && npm run preview"
    echo ""
    echo "📂 To serve with a static server:"
    echo "   npx serve -s frontend-react/dist -l 3000"
else
    echo ""
    echo "❌ Build failed! Check the errors above."
    exit 1
fi
