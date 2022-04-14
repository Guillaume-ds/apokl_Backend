from storages.backends.azure_storage import AzureStorage

class AzureMediaStorage(AzureStorage):
    account_name = 'apoklstorage1' # Must be replaced by your <storage_account_name>
    account_key = 'woAbJ3nJB+IOjSQyFDCE62HfnwqJ0PW65FY/qaRFhe1cpuyAOdOI2c2/7nZgGTsT9I76H3117uUw+AStppgzZw==' # Must be replaced by your <storage_account_key>
    azure_container = 'media'
    expiration_secs = None

class AzureStaticStorage(AzureStorage):
    account_name = 'apoklstorage1' # Must be replaced by your storage_account_name
    account_key = 'woAbJ3nJB+IOjSQyFDCE62HfnwqJ0PW65FY/qaRFhe1cpuyAOdOI2c2/7nZgGTsT9I76H3117uUw+AStppgzZw==' # Must be replaced by your <storage_account_key>
    azure_container = 'static'
    expiration_secs = None