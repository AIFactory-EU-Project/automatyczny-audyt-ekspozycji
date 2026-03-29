<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Validation;

use App\Entity\User;
use App\Service\UserManager;
use DateInterval;
use DateTime;
use Exception;

/**
 * Class UserBusinessValidator.
 */
class UserBusinessValidator
{
    private const FAILED_LOGIN_ATTEMPTS_LIMIT = 10;

    private const PASSWORD_CHANGE_REQUEST_TTL = 'PT2H';

    /**
     * @param User $user
     *
     * @return bool
     */
    public function checkActive(User $user): bool
    {
        return $user->getActive();
    }

    /**
     * @param User $user
     *
     * @return bool
     */
    public function checkPasswordSet(User $user): bool
    {
        return !empty($user->getPassword());
    }

    /**
     * @param User $user
     *
     * @return bool
     */
    public function checkSystemAssigned(User $user): bool
    {
        return $user->getSystem() && $user->getSystem()->getActive();
    }

    /**
     * @param User $user
     *
     * @return bool
     */
    public function checkSystemAvailable(User $user): bool
    {
        try {
            $now = new DateTime();
        } catch (Exception $e) {
            return false;
        }

        return $this->checkSystemAssigned($user) && (!$user->getSystem()->getTerminateDate()
                || $user->getSystem()->getTerminateDate() > $now);
    }

    /**
     * @param User $user
     *
     * @return bool
     */
    public function checkFailedAttemptsLimit(User $user): bool
    {
        if (in_array(UserManager::ROLE_MOBILE_USER, $user->getRoles())) {
            return true;
        }

        return $user->getFailedAttempts() < static::FAILED_LOGIN_ATTEMPTS_LIMIT;
    }

    /**
     * @param User $user
     *
     * @return bool
     *
     * @throws Exception
     */
    public function checkLastChangePasswordRequestTtl(User $user): bool
    {
        $passwordChangeInterval = new DateInterval(static::PASSWORD_CHANGE_REQUEST_TTL);

        return $user->getConfirmationToken() && $user->getPasswordRequestedAt()
        && $user->getPasswordRequestedAt() >= (new DateTime())->sub($passwordChangeInterval);
    }

    /**
     * @param User $user
     *
     * @return string|null
     *
     * @throws Exception
     */
    public function checkPasswordChangeRequirements(User $user): ?string
    {
        if (!$this->checkActive($user)) {
            return ErrorCodes::USER_DISABLED;
        }
        if (!$this->checkSystemAssigned($user)) {
            return ErrorCodes::NO_SYSTEM_ASSIGNED_TO_USER;
        }
        if (!$this->checkSystemAvailable($user)) {
            return ErrorCodes::SYSTEM_TERMINATED;
        }
        if ($this->checkLastChangePasswordRequestTtl($user)) {
            return ErrorCodes::RESET_REQUEST_ALREADY_SENT;
        }

        return null;
    }
}
