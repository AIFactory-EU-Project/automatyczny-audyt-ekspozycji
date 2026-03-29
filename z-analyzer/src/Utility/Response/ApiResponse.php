<?php
namespace App\Utility\Response;

use Symfony\Component\HttpFoundation\JsonResponse;

class ApiResponse extends JsonResponse
{
    /**
     * ApiResponse constructor.
     * @param string $data
     * @param bool $status
     * @param int $httpCode
     */
    public function __construct(string $data, bool $status, int $httpCode)
    {
        parent::__construct($data, $httpCode, [], true);
    }
}