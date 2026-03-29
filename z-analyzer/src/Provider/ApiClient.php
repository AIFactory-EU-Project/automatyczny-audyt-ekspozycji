<?php

namespace App\Provider;

use App\Exception\ApiClientException;
use Symfony\Contracts\HttpClient\Exception\ClientExceptionInterface;
use Symfony\Contracts\HttpClient\Exception\RedirectionExceptionInterface;
use Symfony\Contracts\HttpClient\Exception\ServerExceptionInterface;
use Symfony\Contracts\HttpClient\Exception\TransportExceptionInterface;
use Symfony\Contracts\HttpClient\HttpClientInterface;

class ApiClient
{
    public const METHOD_GET = 'GET';
    public const METHOD_POST = 'POST';
    public const METHOD_PUT = 'PUT';
    public const METHOD_DELETE = 'DELETE';

    private HttpClientInterface $httpClient;

    public function __construct(
        HttpClientInterface $httpClient
    ) {
        $this->httpClient = $httpClient;
    }

    /**
     * @param string $addr
     * @param string $method
     * @param mixed $body
     * @param array $headers
     * @param array $authentication
     * @return string
     * @throws ApiClientException
     */
    public function request(string $addr, string $method, $body = null, $headers = null, $authentication = null): string
    {
        $options = [];

        if (!empty($authentication)) {
            $options['auth_basic'] = [
                $authentication['login'], $authentication['password']
            ];
        }

        if (!empty($body)) {
            $options['body'] = $body;
        }

        if (!empty($headers)) {
            $options['headers'] = $headers;
        }

        try {
            $request = $this->httpClient->request(
                $method,
                $addr,
                $options
            );

            return $request->getContent();
        } catch (
            ClientExceptionInterface |
            RedirectionExceptionInterface |
            ServerExceptionInterface |
            TransportExceptionInterface $e
        ) {
            throw new ApiClientException($e->getMessage());
        }
    }
}
