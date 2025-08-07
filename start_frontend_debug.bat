@echo off
echo Starting frontend in debug mode...
cd frontend_vite
set VITE_MAIN_JS=src/main_debug.jsx
npm run dev
