<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\EventSubscriber;

use App\Dto\ResponseDataDto;
use App\Entity\User;
use App\Event\UserAuth\PasswordChangeConfirmEvent;
use App\Event\UserAuth\PasswordChangeConfirmValidEvent;
use App\Event\UserAuth\PasswordChangeRequestEvent;
use App\Event\UserAuth\PasswordChangeRequestValidEvent;
use App\Exception\UserAuthException;
use App\Service\UserManager;
use App\Validation\ErrorCodes;
use App\Validation\UserBusinessValidator;
use App\Validation\UserResponseMapper;
use Doctrine\ORM\OptimisticLockException;
use Doctrine\ORM\ORMException;
use Exception;
use Lexik\Bundle\JWTAuthenticationBundle\Event\AuthenticationFailureEvent;
use Lexik\Bundle\JWTAuthenticationBundle\Event\AuthenticationSuccessEvent;
use Lexik\Bundle\JWTAuthenticationBundle\Events;
use Psr\Log\LoggerInterface;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpKernel\Event\ExceptionEvent;
use Symfony\Component\HttpKernel\Exception\HttpException;
use Symfony\Component\HttpKernel\KernelEvents;
use Symfony\Component\Mailer\Exception\TransportExceptionInterface;
use Symfony\Component\Security\Core\Event\AuthenticationFailureEvent as SymfonyAuthenticationFailureEvent;
use Symfony\Component\Security\Core\User\UserCheckerInterface;

/**
 * Class LoginSubscriber.
 */
class UserAuthSubscriber implements EventSubscriberInterface
{
    private LoggerInterface $logger;

    private UserManager $userManager;

    private UserCheckerInterface $userChecker;

    private UserBusinessValidator $userBusinessValidator;

    private UserResponseMapper $userResponseMapper;

    public function __construct(
        LoggerInterface $appLogger,
        UserManager $userManager,
        UserCheckerInterface $userChecker,
        UserBusinessValidator $userBusinessValidator,
        UserResponseMapper $userResponseMapper
    ) {
        $this->logger = $appLogger;
        $this->userManager = $userManager;
        $this->userChecker = $userChecker;
        $this->userBusinessValidator = $userBusinessValidator;
        $this->userResponseMapper = $userResponseMapper;
    }

    public static function getSubscribedEvents(): array
    {
        return [
            Events::AUTHENTICATION_SUCCESS => 'onSuccessfulLogin',
            Events::AUTHENTICATION_FAILURE => 'onLoginFailure',
            SymfonyAuthenticationFailureEvent::class => 'onAuthFailure',
            KernelEvents::EXCEPTION => ['onKernelException', 10],
            PasswordChangeRequestEvent::class => 'onPasswordChangeRequest',
            PasswordChangeRequestValidEvent::class => 'onPasswordChangeRequestValid',
            PasswordChangeConfirmEvent::class => 'onPasswordChangeConfirm',
            PasswordChangeConfirmValidEvent::class => 'onPasswordChangeConfirmValid',
        ];
    }

    /**
     * @param AuthenticationSuccessEvent $event
     *
     * @throws ORMException
     * @throws OptimisticLockException
     */
    public function onSuccessfulLogin(AuthenticationSuccessEvent $event): void
    {
        $user = $event->getUser();
        if ($user instanceof User) {
            $this->userChecker->checkPostAuth($user);
            if ($user->getFailedAttempts()) {
                $this->userManager->resetFailedAttempts($user);
                $this->userManager->updateUser($user);
            }
        }
        $this->logger->info('Login success', ['username' => $user->getEmail()]);
    }

    /**
     * @param AuthenticationFailureEvent $event
     *
     * @throws ORMException
     * @throws OptimisticLockException
     */
    public function onLoginFailure(AuthenticationFailureEvent $event): void
    {
        $userName = $event->getException()->getToken()->getUsername();
        $user = $this->userManager->findByEmail($userName);
        if ($user) {
            $this->userManager->addFailedAttempt($user);
            $this->userManager->updateUser($user);
        }
        $this->logger->info('Login failure', ['username' => $userName]);
    }

    /**
     * @param SymfonyAuthenticationFailureEvent $event
     */
    public function onAuthFailure(SymfonyAuthenticationFailureEvent $event): void
    {
        $this->logger->notice('Auth failure');
    }

    /**
     * @param PasswordChangeRequestEvent $event
     *
     * @throws Exception
     */
    public function onPasswordChangeRequest(PasswordChangeRequestEvent $event): void
    {
        $request = $event->getRequest();

        $data = json_decode($request->getContent(), true);

        $user = $this->userManager->findByEmail($data['login']);
        if (!$user) {
            $event->setResponseData(
                new ResponseDataDto(
                    ['message' => 'User not found'],
                    Response::HTTP_NOT_FOUND
                )
            );

            return;
        }

        $event->setUser($user);

        $businessErrorCode = $this->userBusinessValidator->checkPasswordChangeRequirements($user);
        if ($businessErrorCode) {
            $response = $this->userResponseMapper->mapErrorCode($businessErrorCode);
            if ($response) {
                $event->setResponseData($response);

                return;
            }
        }
    }

    /**
     * @param PasswordChangeRequestValidEvent $event
     *
     * @throws ORMException
     * @throws OptimisticLockException
     * @throws TransportExceptionInterface
     */
    public function onPasswordChangeRequestValid(PasswordChangeRequestValidEvent $event): void
    {
        $user = $event->getUser();
        $this->userManager->sendPasswordChangeMail($user);
        $this->userManager->updateUser($user);
    }

    /**
     * @param ExceptionEvent $event
     */
    public function onKernelException(ExceptionEvent $event): void
    {
        $responseCode = null;
        if ($event->getThrowable() instanceof UserAuthException) {
            $code = $event->getThrowable()->getErrorCode();
            $this->logger->notice('Token auth failure', ['errorCode' => $responseCode]);
            $mappedResponse = $this->userResponseMapper->mapErrorCode($code);
            if ($mappedResponse) {
                $event->setResponse(
                    new JsonResponse($mappedResponse->getContent(), $mappedResponse->getCode())
                );
            }
        } elseif ($event->getThrowable() instanceof HttpException) {
            $this->logger->notice('Http Exception', [
                'exception' => [
                    'message' => $event->getThrowable()->getMessage(),
                    'code' => $event->getThrowable()->getCode(),
                ],
            ]);
        } else {
            $this->logger->warning('Exception', [
                'exception' => [
                    'message' => $event->getThrowable()->getMessage(),
                ],
            ]);
        }
    }

    /**
     * @param PasswordChangeConfirmEvent $event
     *
     * @throws Exception
     */
    public function onPasswordChangeConfirm(PasswordChangeConfirmEvent $event): void
    {
        $request = $event->getRequest();
        $data = json_decode($request->getContent(), true);

        if ($data['password'] !== $data['confirm_password']) {
            $event->setResponseData(
                new ResponseDataDto(
                    ['message' => 'passwords do not match'],
                    Response::HTTP_BAD_REQUEST
                )
            );

            return;
        }

        $user = $this->userManager->findByConfirmationToken($data['token']);
        if (!$user) {
            $event->setResponseData(
                new ResponseDataDto(
                    ['message' => 'Token not found'],
                    Response::HTTP_NOT_FOUND
                )
            );

            return;
        }
        $event->setUser($user);

        if (!$this->userBusinessValidator->checkLastChangePasswordRequestTtl($user)) {
            $event->setResponseData(
                new ResponseDataDto(
                    ['message' => 'Token outdated', 'code' => ErrorCodes::INVALID_RESET_TOKEN],
                    Response::HTTP_UNAUTHORIZED
                )
            );

            return;
        }
    }

    /**
     * @param PasswordChangeConfirmValidEvent $event
     *
     * @throws ORMException
     * @throws OptimisticLockException
     */
    public function onPasswordChangeConfirmValid(PasswordChangeConfirmValidEvent $event)
    {
        $user = $event->getUser();
        $user->setPlainPassword($event->getNewPassword());
        $user->setConfirmationToken(null);
        $this->userManager->resetFailedAttempts($user);
        $this->userManager->updateUser($user);
    }
}
