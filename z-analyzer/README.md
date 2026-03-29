# PlanogramAnalyzer

### Creating user
php bin/console fos:user:create {{user_login}}

/createClient {POST} - Creating client //TODO can be only by CLI command for 'extra obfuscated security'
{
	"redirect-uri": "redirect.local",
	"grant-type": "password"
}

/oauth/v2/token {POST} - Posting for OAuth 2.0 token
{
	"client_id": "wynik z createClient",
	"client_secret": "wynik z createClient",
	"grant_type": "password",
	"username": "login_uzytkownika",
	"password": "haslo_uzytkownika"
}

/api {GET} - API documentation generated from models