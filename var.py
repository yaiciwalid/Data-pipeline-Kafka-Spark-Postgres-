MAX_LIMIT = 100
MAX_OFFSET = 10000
TOPIC = "rappel_conso"

URL_API = "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/rappelconso0/records?limit={}&where=date_de_publication%20%3E%20'{}'&order_by=date_de_publication%20ASC&offset={}"
URL_API = URL_API.format(MAX_LIMIT, "{}", "{}")