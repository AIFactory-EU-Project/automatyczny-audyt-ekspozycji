<?php

namespace App\Controller;

use App\Exception\ApiResponseException;
use App\Service\NormalizerRetriever;
use App\Utility\Response\ApiResponse;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\Serializer\Encoder\JsonEncoder;
use Symfony\Component\Serializer\Normalizer\ObjectNormalizer;
use Symfony\Component\Serializer\Serializer;
use Symfony\Component\Serializer\SerializerInterface;

abstract class BaseController extends AbstractController
{
    private SerializerInterface $serializer;

    /**
     * @required
     *
     * @param NormalizerRetriever $retriever
     */
    public function setSerializer(NormalizerRetriever $retriever): void
    {
        $normalizerArray = $retriever->getAllNormalizers();
        array_push($normalizerArray, new ObjectNormalizer());
        $serializer = new Serializer(
            $normalizerArray,
            [new JsonEncoder()]
        );
        $this->serializer = $serializer;
    }

    /**
     * @param mixed $data
     * @param bool $status
     * @param string $message
     * @param int $httpCode
     * @param array $context
     * @return ApiResponse
     * @throws ApiResponseException
     */
    public function createApiResponse(
        $data = null,
        bool $status = true,
        string $message = '',
        int $httpCode = 200,
        array $context = []
    ): ApiResponse {
        if ($this->serializer) {
            $data = [
                'status' => [
                    'success' => $status,
                    'message' => $message,
                ],
                'data' => $data,
            ];
            $data = $this->serializer->serialize($data, 'json', array_merge(['groups' => ['API']], $context));

            return new ApiResponse($data, $status, $httpCode);
        }

        throw new ApiResponseException('Serializer is null.');
    }
}
