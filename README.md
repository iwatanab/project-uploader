# Service Example

Fork this to create a new service.

## Local development
Install service:

```bash
poetry install
```

Run the service locally with:

```
poetry run uvicorn app.main:app --reload
```
Set up dev pre-commit hooks:

```
poetry run pre-commit install
```

## Dev Notes
Steps to register a service on the platform:
- Confirm you have an account and a workspace.
- Confirm that the user you want to access the service has a workspace (can be the same workspace as above) and
  is listed in the workspace_member table. The row id from workspace_member table will be needed to create a resource.
- Create an entry in the Product table. Select a slug that you can easily use in a URL for the product.
	- `api_url` must be the base url.
  - when you pick a value for the `slug` column, make sure you can easily use it in a URL.
- OPTIONAL Create an entry in the catalog_item table to allow other users to see the product.
- Create a row for the resource_activation table using the `product_id`, `workspace_member_id`, and `workspace_id`. Set `is_restricted` to False/0 for now.
- Create a row in the resource table using `product_id`, `workspace_id`, and `resouce_activation_id`. Set `is_restricted` to False/0. Select a value for `slug` for the resource that you can easily use in a URL.

Steps to run the service:
- Get a JWT token using your API key:
```bash
curl -v -XPOST -d '{"key": <REPLACE_WITH_API_KEY>}' https://api.strangeworks.com/users/token
```
- Use your JWT token to call the service:

For example, if the product slug is `famous-quotes` and the resource slug is `garbanzo1`, and the app/endpoint name is `quote`, the call to the service would look like:
```bash
curl -H "Authorization: Bearer ${JWT_TOKEN}" 'https://api.strangeworks.com/product/famous-quotes/resource/garbanzo1/quote
```

Other considerations:

Set `PRODUCT_LIB_API_KEY` env variable in cloudrun

Make sure libs are up to date.
```
poetry add sw-product-lib@latest
```
