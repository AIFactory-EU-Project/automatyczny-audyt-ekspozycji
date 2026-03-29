<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Event\UserAuth;

use App\Dto\ResponseDataDto;
use App\Entity\User;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Contracts\EventDispatcher\Event;

/**
 * Class PasswordChangeRequestEvent.
 */
class PasswordChangeRequestEvent extends Event
{
    private ?User $user = null;

    private Request $request;

    private ?ResponseDataDto $responseDataDto = null;

    /**
     * PasswordChangeRequestEvent constructor.
     *
     * @param Request $request
     */
    public function __construct(Request $request)
    {
        $this->request = $request;
    }

    /**
     * @return User
     */
    public function getUser(): User
    {
        return $this->user;
    }

    /**
     * @param User $user
     */
    public function setUser(User $user): void
    {
        $this->user = $user;
    }

    /**
     * @return ResponseDataDto|null
     */
    public function getResponseData(): ?ResponseDataDto
    {
        return $this->responseDataDto;
    }

    /**
     * @param ResponseDataDto|null $responseDataDto
     */
    public function setResponseData(?ResponseDataDto $responseDataDto): void
    {
        $this->responseDataDto = $responseDataDto;
    }

    /**
     * @return Request
     */
    public function getRequest(): Request
    {
        return $this->request;
    }
}
