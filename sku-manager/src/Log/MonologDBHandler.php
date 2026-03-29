<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Log;

use App\Entity\AppLog;
use App\Repository\AppLogRepository;
use App\Service\UserManager;
use Doctrine\ORM\OptimisticLockException;
use Doctrine\ORM\ORMException;
use Monolog\Handler\AbstractProcessingHandler;
use Monolog\Logger;
use Symfony\Component\HttpFoundation\RequestStack;
use Symfony\Component\Security\Core\Authentication\Token\Storage\TokenStorageInterface;
use Symfony\Component\Security\Core\User\UserInterface;

/**
 * Class MonologDBHandler.
 */
class MonologDBHandler extends AbstractProcessingHandler
{
    protected AppLogRepository $logRepository;

    private TokenStorageInterface $tokenStorage;

    private UserManager $userManager;

    private RequestStack $requestStack;

    /**
     * MonologDBHandler constructor.
     *
     * @param AppLogRepository      $logRepository
     * @param RequestStack          $requestStack
     * @param TokenStorageInterface $tokenStorage
     * @param UserManager           $userManager
     * @param int                   $level
     * @param bool                  $bubble
     */
    public function __construct(
        AppLogRepository $logRepository,
        RequestStack $requestStack,
        TokenStorageInterface $tokenStorage,
        UserManager $userManager,
        $level = Logger::DEBUG,
        $bubble = true
    ) {
        parent::__construct($level, $bubble);
        $this->tokenStorage = $tokenStorage;
        $this->logRepository = $logRepository;
        $this->userManager = $userManager;
        $this->requestStack = $requestStack;
    }

    /**
     * @param array $record
     *
     * @throws ORMException
     * @throws OptimisticLockException
     */
    protected function write(array $record)
    {
        $logEntry = new AppLog();
        $logEntry->setMessage($record['message']);
        $logEntry->setLevel($record['level']);
        $logEntry->setLevelName($record['level_name']);
        $logEntry->setExtra($record['extra']);
        $logEntry->setContext($record['context']);

        $this->addUserContext($logEntry);
        $this->addRequestExtra($logEntry);
        $this->moveSensitiveContextToExtra($logEntry);

        $this->logRepository->save($logEntry);
    }

    private function addUserContext(AppLog $logEntry)
    {
        $context = $logEntry->getContext();
        $user = null;

        if ($this->tokenStorage->getToken()
            && $this->tokenStorage->getToken()->getUser()
            && $this->tokenStorage->getToken()->getUser() instanceof UserInterface) {
            $user = $this->tokenStorage->getToken()->getUser();
        } elseif (!empty($context['username'])) {
            $user = $this->userManager->findByEmail($context['username']);
        }

        if (empty($context['username']) && $user) {
            $context['username'] = $user->getEmail();
        }

        if (empty($context['systemId']) && $user) {
            $context['systemId'] = $user->getSystem() ? $user->getSystem()->getId() : null;
        }
        if (!empty($context['systemId'])) {
            $logEntry->setSystemId((int) $context['systemId']);
            unset($context['systemId']);
        }

        $logEntry->setContext($context);
    }

    private function moveSensitiveContextToExtra(AppLog $logEntry)
    {
        $extra = $logEntry->getExtra();
        $context = $logEntry->getContext();

        if (!empty($context['exception'])) {
            $extra['exception'] = $context['exception'];
            unset($context['exception']);
        }

        $logEntry->setExtra($extra);
        $logEntry->setContext($context);
    }

    private function addRequestExtra(AppLog $logEntry)
    {
        $extra = $logEntry->getExtra();

        $request = $this->requestStack->getMasterRequest();
        $extra['request'] = [
            'uri' => $request->getUri(),
            'pathInfo' => $request->getPathInfo(),
            'queryString' => $request->getQueryString(),
            'route' => $request->get('_route'),
        ];

        $logEntry->setExtra($extra);
    }
}
