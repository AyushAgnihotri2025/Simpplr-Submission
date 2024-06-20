cd frontend

npm install
npm run build

rm -r ../backend/backend/static
mkdir ../backend/backend/static
mv ./out/* ../backend/backend/static

cd ../backend

pip install -r requirements.txt
python -m backend setupDB
python -m backend