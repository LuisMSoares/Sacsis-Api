rm -rf sacsis.tech
git clone -b builded https://github.com/iguit0/xi-sacsis-website.git sacsis.tech
cp -a ./sacsis.tech/dist/* ./sacsis.tech
rm -rf ./sacsis.tech/dist

rm -rf app.sacsis.tech
git clone -b builded https://github.com/iguit0/xi-sacsis-admin app.sacsis.tech
cp -a ./app.sacsis.tech/dist/* ./app.sacsis.tech
rm -rf ./app.sacsis.tech/dist
