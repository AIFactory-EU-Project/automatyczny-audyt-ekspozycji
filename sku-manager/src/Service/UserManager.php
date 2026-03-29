<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Service;

use App\Entity\System;
use App\Entity\User;
use App\Repository\UserRepository;
use App\Service\Mailer\UserMailer;
use DateTime;
use Doctrine\ORM\OptimisticLockException;
use Doctrine\ORM\ORMException;
use Exception;
use Symfony\Component\Mailer\Exception\TransportExceptionInterface;
use Symfony\Component\Security\Core\Encoder\UserPasswordEncoderInterface;
use Symfony\Component\Security\Csrf\TokenGenerator\TokenGeneratorInterface;
use Symfony\Component\Validator\ConstraintViolationListInterface;
use Symfony\Component\Validator\Validator\ValidatorInterface;

/**
 * Class UserService.
 */
class UserManager
{
    public const ROLE_ADMIN = 'ROLE_ADMIN';
    public const ROLE_WEB_USER = 'ROLE_WEB_USER';
    public const ROLE_MOBILE_USER = 'ROLE_MOBILE_USER';

    private UserRepository $repository;

    private ValidatorInterface $validator;

    private UserPasswordEncoderInterface $passwordEncoder;

    private UserMailer $userMailer;

    private TokenGeneratorInterface $tokenGenerator;

    /**
     * UserManager constructor.
     *
     * @param UserRepository               $userRepository
     * @param ValidatorInterface           $validator
     * @param UserPasswordEncoderInterface $passwordEncoder
     * @param UserMailer                   $userMailer
     * @param TokenGeneratorInterface      $tokenGenerator
     */
    public function __construct(
        UserRepository $userRepository,
        ValidatorInterface $validator,
        UserPasswordEncoderInterface $passwordEncoder,
        UserMailer $userMailer,
        TokenGeneratorInterface $tokenGenerator
    ) {
        $this->repository = $userRepository;
        $this->passwordEncoder = $passwordEncoder;
        $this->validator = $validator;
        $this->userMailer = $userMailer;
        $this->tokenGenerator = $tokenGenerator;
    }

    public function getNewUser(System $system): User
    {
        $user = new User();
        $user->setSystem($system);
        $user->setActive(true);
        try {
            $user->setCreatedDate(new DateTime());
            $user->setUpdatedDate(new DateTime());
        } catch (Exception $e) {
        }

        return $user;
    }

    /**
     * @param User $user
     *
     * @throws ORMException
     * @throws OptimisticLockException
     */
    public function updateUser(User $user): void
    {
        if ($user->getPlainPassword()) {
            $this->updatePassword($user);
        }
        $this->repository->save($user);
    }

    /**
     * @param User $user
     */
    public function updatePassword(User $user): void
    {
        $password = $this->passwordEncoder->encodePassword($user, $user->getPlainPassword());
        $user->setPassword($password);
        $user->eraseCredentials();
    }

    /**
     * @param User $user
     *
     * @throws ORMException
     * @throws OptimisticLockException
     */
    public function addUser(User $user)
    {
        if ($user->getPlainPassword()) {
            $this->updatePassword($user);
        }
        $this->repository->save($user);
    }

    /**
     * @param User $user
     *
     * @return ConstraintViolationListInterface
     */
    public function validateUser(User $user): ConstraintViolationListInterface
    {
        return $this->validator->validate($user);
    }

    /**
     * @param string $email
     *
     * @return User|null
     */
    public function findByEmail(string $email): ?User
    {
        return $this->repository->findOneBy(['email' => $email]);
    }

    /**
     * @param string $confirmationToken
     *
     * @return User|null
     */
    public function findByConfirmationToken(string $confirmationToken): ?User
    {
        return $this->repository->findOneBy(['confirmationToken' => $confirmationToken]);
    }

    /**
     * @param User $user
     *
     * @throws TransportExceptionInterface
     */
    public function sendPasswordChangeMail(User $user)
    {
        $user->setConfirmationToken($this->tokenGenerator->generateToken());
        $user->setPasswordRequestedAt(new DateTime());
        $this->userMailer->sendPasswordChangeMail($user);
    }

    /**
     * @param User $user
     *
     * @throws TransportExceptionInterface
     */
    public function sendRegistrationMail(User $user)
    {
        $user->setConfirmationToken($this->tokenGenerator->generateToken());
        $user->setPasswordRequestedAt(new DateTime());
        $this->userMailer->sendRegistrationMail($user);
    }

    /**
     * @param User $user
     */
    public function addFailedAttempt(User $user)
    {
        $user->setFailedAttempts($user->getFailedAttempts() + 1);
    }

    /**
     * @param User $user
     */
    public function resetFailedAttempts(User $user)
    {
        $user->setFailedAttempts(0);
    }

    public function getUser(int $userId, System $system)
    {
        return $this->repository->findOneBy(['id' => $userId, 'active' => true, 'system' => $system]);
    }

    public function getUsers(System $system)
    {
        return $this->repository->findBy(['active' => true, 'system' => $system]);
    }

    /**
     * @param User $user
     *
     * @throws ORMException
     * @throws OptimisticLockException
     */
    public function deleteUser(User $user)
    {
        $user->setActive(false);
        $mailParts = explode('@', $user->getEmail());
        $user->setEmail($mailParts[0].'+deleted'.'+id'.$user->getId().'@'.$mailParts[1]);
        $this->repository->save($user);
    }
}
