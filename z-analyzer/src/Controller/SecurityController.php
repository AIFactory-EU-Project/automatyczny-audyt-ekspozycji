<?php

namespace App\Controller;

use App\Exception\ApiResponseException;
use OAuth2\OAuth2;
use OAuth2\OAuth2ServerException;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use FOS\OAuthServerBundle\Model\ClientManagerInterface;
use Symfony\Component\Routing\Annotation\Route;

class SecurityController extends BaseController
{
    private ClientManagerInterface $clientManager;
    private OAuth2 $server;

    public function __construct(ClientManagerInterface $clientManager, OAuth2 $server)
    {
        $this->clientManager = $clientManager;
//        $serwer = $this->container->get('fos_oauth_server.server');
        $this->server = $server;
    }
    /**
     * Create Client.
     * @Route("/createClient", name="OAuth2_create_client")
     * @param Request $request
     * @return Response
     *
     * @throws ApiResponseException
     */
    public function AuthenticationAction(Request $request)
    {
        $data = json_decode($request->getContent(), true);
        if (empty($data['redirect-uri']) || empty($data['grant-type'])) {
            return $this->createApiResponse($data, false, 'No redirect-uri or grant-type');
        }
        $clientManager = $this->clientManager;
        $client = $clientManager->createClient();
        $client->setRedirectUris([$data['redirect-uri']]);
        $client->setAllowedGrantTypes([$data['grant-type']]);
        $clientManager->updateClient($client);
        $rows = [
            'client_id' => $client->getPublicId(), 'client_secret' => $client->getSecret()
        ];

        return $this->createApiResponse($rows);
    }


    /**
     * @Route("/oauth/v2/token", name="OAuth2_generate_token")
     * @param Request $request
     *
     * @return Response
     */
    public function tokenAction(Request $request)
    {
        try {
            return $this->server->grantAccessToken($request);
        } catch (OAuth2ServerException $e) {
            return $e->getHttpResponse();
        }
    }
}