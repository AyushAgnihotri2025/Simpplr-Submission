cd frontend

npm install
npm run build
npm run export

mv /out/* ../backend/frontend/out

cd ..

cd backend

python -m backend setupDB
python -m backend