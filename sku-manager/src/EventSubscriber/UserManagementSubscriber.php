<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\EventSubscriber;

use App\Dto\ResponseDataDto;
use App\Event\UserManagement\AddUserEvent;
use App\Event\UserManagement\AddUserValidEvent;
use App\Event\UserManagement\DeleteUserEvent;
use App\Event\UserManagement\DeleteUserValidEvent;
use App\Form\UserType;
use App\Service\UserManager;
use App\Validation\ErrorCodes;
use Doctrine\ORM\OptimisticLockException;
use Doctrine\ORM\ORMException;
use Psr\Log\LoggerInterface;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;
use Symfony\Component\Form\FormFactoryInterface;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Mailer\Exception\TransportExceptionInterface;

class UserManagementSubscriber implements EventSubscriberInterface
{
    private LoggerInterface $logger;
    private UserManager $userManager;
    private FormFactoryInterface $formFactory;

    public function __construct(
        LoggerInterface $appLogger,
        UserManager $userManager,
        FormFactoryInterface $formFactory
    ) {
        $this->logger = $appLogger;
        $this->userManager = $userManager;
        $this->formFactory = $formFactory;
    }

    public static function getSubscribedEvents(): array
    {
        return [
            AddUserEvent::class => 'onAddUser',
            AddUserValidEvent::class => 'onAddUserValid',
            DeleteUserEvent::class => 'onDeleteUser',
            DeleteUserValidEvent::class => 'onDeleteUserValid',
        ];
    }

    public function onAddUser(AddUserEvent $event)
    {
        $user = $this->userManager->getNewUser($event->getSystem());
        $user->addRole(UserManager::ROLE_WEB_USER);
        $event->setUser($user);

        $form = $this->formFactory->create(UserType::class, $user);
        $data = json_decode($event->getRequest()->getContent(), true);
        $form->submit($data);

        if (!$form->isValid()) {
            $response = new ResponseDataDto(
                $form->getErrors(true),
                Response::HTTP_BAD_REQUEST
            );
            $event->setResponseData($response);

            return;
        }
    }

    /**
     * @param AddUserValidEvent $event
     *
     * @throws ORMException
     * @throws OptimisticLockException
     * @throws TransportExceptionInterface
     */
    public function onAddUserValid(AddUserValidEvent $event)
    {
        $this->userManager->addUser($event->getUser());
        $this->userManager->sendRegistrationMail($event->getUser());
    }

    public function onDeleteUser(DeleteUserEvent $event)
    {
        $user = $this->userManager->getUser($event->getId(), $event->getSystem());
        $event->setUser($user);
        if (in_array(UserManager::ROLE_ADMIN, $user->getRoles()) ||
            in_array(UserManager::ROLE_MOBILE_USER, $user->getRoles())) {
            $response = new ResponseDataDto(
                ['code' => ErrorCodes::UNAUTHORIZED, 'message' => 'Api user cannot be deleted'],
                Response::HTTP_UNAUTHORIZED
            );
            $event->setResponseData($response);

            return;
        }
        if (!$user) {
            $response = new ResponseDataDto(
                ['message' => 'User not found'],
                Response::HTTP_NOT_FOUND
            );
            $event->setResponseData($response);

            return;
        }
    }

    /**
     * @param DeleteUserValidEvent $event
     *
     * @throws ORMException
     * @throws OptimisticLockException
     */
    public function onDeleteUserValid(DeleteUserValidEvent $event)
    {
        $this->userManager->deleteUser($event->getUser());
    }
}
