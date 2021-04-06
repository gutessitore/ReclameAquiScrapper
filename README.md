# Reclame Aqui Web Scrapper

The goal of this project is to collect "Reclame Aqui" user reviews easily

## How to use

```python
from scrapper import ReclameAqui

# Initializing ReclameAqui object
mercado_livre = ReclameAqui("mercado-livre", max_page=10)

# collecting all reviews from page one to max_page (10)
mercado_livre.get_reviews()  # May take some time to run

print(mercado_livre.reviews)  #  Listing all reviews

# Convert all reviews to a dataframe with "review", "date", "city" and "status" columns
mercado_livre_df = mercado_livre.to_data_frame() 

print(mercado_livre_df)
```