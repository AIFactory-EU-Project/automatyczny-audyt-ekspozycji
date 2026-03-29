<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Event\UserAuth;

use App\Dto\ResponseDataDto;
use App\Entity\User;
use Symfony\Contracts\EventDispatcher\Event;

class PasswordChangeConfirmValidEvent extends Event
{
    private User $user;

    private ?ResponseDataDto $responseDataDto = null;

    private string $newPassword;

    /**
     * PasswordChangeRequestValidEvent constructor.
     *
     * @param User $user
     */
    public function __construct(User $user, string $newPassword)
    {
        $this->user = $user;
        $this->newPassword = $newPassword;
    }

    /**
     * @return User
     */
    public function getUser(): User
    {
        return $this->user;
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
     * @return string
     */
    public function getNewPassword(): string
    {
        return $this->newPassword;
    }
}
