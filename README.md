# Reclame Aqui Web Scrapper

The goal of this project is to collect "Reclame Aqui" user reviews easily

## How to use

clone this repository using `git clone https://github.com/gutessitore/ReclameAquiScrapper.git`

```python
from scrapper import ReclameAqui
import os

driver_path = os.getcwd() + "/drivers/chromedriver"
mercado_livre = ReclameAqui("mercado-livre", driver_path=driver_path)

# collecting all reviews from page one to max_page (10)
mercado_livre.get_reviews()

# Convert all reviews to a dataframe with "review", "date", "city" and "status" columns
mercado_livre_df = mercado_livre.to_data_frame

print(mercado_livre_df)
```

#### ReclameAqui attributes