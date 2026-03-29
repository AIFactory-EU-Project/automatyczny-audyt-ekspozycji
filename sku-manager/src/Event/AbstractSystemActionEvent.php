<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Event;

use App\Dto\ResponseDataDto;
use App\Entity\System;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Contracts\EventDispatcher\Event;

abstract class AbstractSystemActionEvent extends Event
{
    private Request $request;

    private System $system;

    private ?ResponseDataDto $responseData = null;

    public function __construct(Request $request, System $system)
    {
        $this->request = $request;
        $this->system = $system;
    }

    /**
     * @return ResponseDataDto|null
     */
    public function getResponseData(): ?ResponseDataDto
    {
        return $this->responseData;
    }

    /**
     * @param ResponseDataDto|null $responseDataDto
     */
    public function setResponseData(?ResponseDataDto $responseDataDto): void
    {
        $this->responseData = $responseDataDto;
    }

    /**
     * @return Request
     */
    public function getRequest(): Request
    {
        return $this->request;
    }

    /**
     * @return System
     */
    public function getSystem(): System
    {
        return $this->system;
    }
}
