<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Security;

use App\Entity\User;
use App\Exception\UserAuthException;
use App\Validation\ErrorCodes;
use App\Validation\UserBusinessValidator;
use Symfony\Component\Security\Core\User\UserCheckerInterface;
use Symfony\Component\Security\Core\User\UserInterface;

/**
 * Class UserChecker.
 */
class UserChecker implements UserCheckerInterface
{
    private UserBusinessValidator $userValidator;

    /**
     * UserChecker constructor.
     *
     * @param UserBusinessValidator $userValidator
     */
    public function __construct(UserBusinessValidator $userValidator)
    {
        $this->userValidator = $userValidator;
    }

    /**
     * @param UserInterface $user
     *
     * @throws UserAuthException
     */
    public function checkPreAuth(UserInterface $user)
    {
        if (!$user instanceof User) {
            return;
        }

        if (!$this->userValidator->checkPasswordSet($user)) {
            throw new UserAuthException(ErrorCodes::PASSWORD_CHANGE_REQUIRED);
        }
    }

    /**
     * @param UserInterface $user
     *
     * @throws UserAuthException
     */
    public function checkPostAuth(UserInterface $user)
    {
        if (!$user instanceof User) {
            return;
        }

        if (!$this->userValidator->checkActive($user)) {
            throw new UserAuthException(ErrorCodes::USER_DISABLED);
        }

        if (!$this->userValidator->checkFailedAttemptsLimit($user)) {
            throw new UserAuthException(ErrorCodes::PASSWORD_CHANGE_REQUIRED);
        }

        if (!$this->userValidator->checkSystemAssigned($user)) {
            throw new UserAuthException(ErrorCodes::NO_SYSTEM_ASSIGNED_TO_USER);
        }

        if (!$this->userValidator->checkSystemAvailable($user)) {
            throw new UserAuthException(ErrorCodes::SYSTEM_TERMINATED);
        }
    }
}
