#!/bin/bash

echo "Cleaning old assets."
rm -rf ../invoices/static/invoices/statics
rm -rf ../invoices/static/invoices/assets
rm ../invoices/static/invoices/manifest.json
echo "Copying new assets."
cp build/static/.vite/manifest.json ../invoices/static/invoices/manifest.json
cp -r build/static/assets ../invoices/static/invoices/assets
# copy the image assets to the correct place.
cp -r build/static/static/invoices/static ../invoices/static/invoices/static
echo "Assets copied successfully."
