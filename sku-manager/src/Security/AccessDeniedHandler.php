<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Security;

use App\Validation\ErrorCodes;
use Psr\Log\LoggerInterface;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\RequestStack;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Security\Core\Authentication\Token\Storage\TokenStorageInterface;
use Symfony\Component\Security\Core\Exception\AccessDeniedException;
use Symfony\Component\Security\Http\Authorization\AccessDeniedHandlerInterface;

/**`
 * Class AccessDeniedHandler.
 */
class AccessDeniedHandler implements AccessDeniedHandlerInterface
{
    private LoggerInterface $appLogger;

    private TokenStorageInterface $tokenStorage;

    private RequestStack $requestStack;

    /**
     * AccessDeniedHandler constructor.
     *
     * @param LoggerInterface       $appLogger
     * @param TokenStorageInterface $tokenStorage
     * @param RequestStack          $requestStack
     */
    public function __construct(
        LoggerInterface $appLogger,
        TokenStorageInterface $tokenStorage,
        RequestStack $requestStack
    ) {
        $this->appLogger = $appLogger;
        $this->tokenStorage = $tokenStorage;
        $this->requestStack = $requestStack;
    }

    /**
     * @param Request               $request
     * @param AccessDeniedException $accessDeniedException
     *
     * @return Response|null
     */
    public function handle(
        Request $request,
        AccessDeniedException $accessDeniedException
    ) {
        $context = [];
        $context['exception'] = $accessDeniedException->getAttributes();
        $request = $this->requestStack->getMasterRequest();
        $context['route'] = $request->get('_route');
        $this->appLogger->warning('Access denied', $context);

        return new JsonResponse([
            'code' => ErrorCodes::UNAUTHORIZED,
            'message' => $accessDeniedException->getMessage(),
        ], Response::HTTP_FORBIDDEN);
    }
}
