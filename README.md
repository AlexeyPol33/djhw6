docker build . --tag=stocks_products
docker run -d -p 7777:80 stocks_products
