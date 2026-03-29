<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Controller;

use App\Event\UserAuth\PasswordChangeConfirmEvent;
use App\Event\UserAuth\PasswordChangeConfirmValidEvent;
use App\Event\UserAuth\PasswordChangeRequestEvent;
use App\Event\UserAuth\PasswordChangeRequestValidEvent;
use App\Validation\ErrorCodes;
use FOS\RestBundle\Controller\Annotations as Rest;
use Nelmio\ApiDocBundle\Annotation\Security;
use Swagger\Annotations as SWG;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Security\Http\Authentication\AuthenticationSuccessHandlerInterface;
use Symfony\Contracts\EventDispatcher\EventDispatcherInterface;

/**
 * Class SecurityController.
 */
class SecurityController extends AbstractDomainController
{
    /**
     * @Rest\Post("/login")
     *
     * @SWG\Post(
     *     summary="Login",
     *     description="Login",
     *     tags={"Security"},
     *     @SWG\Response(
     *          response=200,
     *          description="Login succesful",
     *          @SWG\Schema(
     *              @SWG\Property(property="token", type="string")
     *          )
     *     ),
     *     @SWG\Response(
     *          response=401,
     *          description="Invalid credentials",
     *          @SWG\Schema(
     *              @SWG\Property(property="message", type="string")
     *          )
     *     ),
     *     @SWG\Response(response=400, description="Request errors", @SWG\Schema(
     *              @SWG\Property(property="code", type="string", enum=ErrorCodes::INVALID_CODES),
     *              @SWG\Property(property="errors", type="array", @SWG\Items(type="string")),
     *      )),
     *     @SWG\Response(response=409, description="Conflict errors", @SWG\Schema(
     *              @SWG\Property(property="code", type="string", enum=ErrorCodes::CONFLICT_CODES),
     *              @SWG\Property(property="errors", type="array", @SWG\Items(type="string")),
     *      )),
     *     @SWG\Response(response=403, description="Forbidden", @SWG\Schema(
     *           @SWG\Property(property="code", type="string", enum=ErrorCodes::FORBIDDEN_CODES),
     *           @SWG\Property(property="message", type="string"),
     *      )),
     * )
     *
     * @SWG\Parameter(
     *     name="data",
     *     in="body",
     *     @SWG\Schema(
     *              @SWG\Property(property="login", type="string"),
     *              @SWG\Property(property="password", type="string")
     *          )
     * )
     *
     * @param Request $request
     */
    public function login(Request $request)
    {
        //handled by lexik_jwt_authentication
    }

    /**
     * @Rest\Post("/password/reset/request")
     *
     * @SWG\Post(
     *     summary="Request password reset mail",
     *     description="Request password reset mail",
     *     tags={"Security"},
     *     @SWG\Response(
     *          response=200,
     *          description="Password reset mail has been sent"
     *     ),
     *     @SWG\Response(response=400, description="Request errors", @SWG\Schema(
     *              @SWG\Property(property="code", type="string",
     *                            enum={ErrorCodes::INVALID_REQUEST, ErrorCodes::RESET_REQUEST_ALREADY_SENT}),
     *              @SWG\Property(property="errors", type="array", @SWG\Items(type="string")),
     *      )),
     *     @SWG\Response(response=403, description="Forbidden", @SWG\Schema(
     *           @SWG\Property(property="code", type="string",
     *                         enum={ErrorCodes::NO_SYSTEM_ASSIGNED_TO_USER, ErrorCodes::SYSTEM_TERMINATED, ErrorCodes::USER_DISABLED}),
     *           @SWG\Property(property="message", type="string"),
     *      )),
     *     @SWG\Response(response=404, description="User not found", @SWG\Schema(
     *           @SWG\Property(property="User not found", type="string"),
     *      )),
     * )
     *
     * @SWG\Parameter(
     *     name="data",
     *     in="body",
     *     @SWG\Schema(
     *              @SWG\Property(property="login", type="string")
     *          )
     * )
     *
     * @param Request                  $request
     * @param EventDispatcherInterface $eventDispatcher
     *
     * @return Response
     */
    public function request(Request $request, EventDispatcherInterface $eventDispatcher): Response
    {
        $passwordChangeRequestEvent = new PasswordChangeRequestEvent($request);

        $eventDispatcher->dispatch($passwordChangeRequestEvent);

        if ($passwordChangeRequestEvent->getResponseData()) {
            return $this->handleEventResponseData($passwordChangeRequestEvent->getResponseData());
        }

        $user = $passwordChangeRequestEvent->getUser();
        $passwordChangeRequestValidEvent = new PasswordChangeRequestValidEvent($user);
        $eventDispatcher->dispatch($passwordChangeRequestValidEvent);

        if ($passwordChangeRequestValidEvent->getResponseData()) {
            return $this->handleEventResponseData($passwordChangeRequestValidEvent->getResponseData());
        }

        return $this->handleView(
            $this->view(['message' => 'Password reset email has been sent'], Response::HTTP_OK)
        );
    }

    /**
     * @Rest\Post("/password/reset/confirm")
     *
     * @SWG\Post(
     *     summary="Update password",
     *     description="Update password",
     *     tags={"Security"},
     *     @SWG\Response(
     *          response=200,
     *          description="Password has been updated",
     *          @SWG\Schema(
     *              @SWG\Property(property="token", type="string")
     *          )
     *     ),
     *     @SWG\Response(response=400, description="Request errors", @SWG\Schema(
     *              @SWG\Property(property="code", type="string", enum=ErrorCodes::INVALID_CODES),
     *              @SWG\Property(property="errors", type="array", @SWG\Items(type="string")),
     *      )),
     *     @SWG\Response(response=409, description="Conflict errors", @SWG\Schema(
     *              @SWG\Property(property="code", type="string", enum=ErrorCodes::CONFLICT_CODES),
     *              @SWG\Property(property="errors", type="array", @SWG\Items(type="string")),
     *      )),
     *     @SWG\Response(response=401, description="Unauthorized", @SWG\Schema(
     *          @SWG\Property(property="code", type="integer", enum={ErrorCodes::INVALID_RESET_TOKEN}),
     *          @SWG\Property(property="message", type="string"),
     *     )),
     *     @SWG\Response(response=403, description="Forbidden", @SWG\Schema(
     *           @SWG\Property(property="code", type="string",
     *                         enum={ErrorCodes::SYSTEM_TERMINATED, ErrorCodes::USER_DISABLED}),
     *           @SWG\Property(property="message", type="string"),
     *      )),
     * )
     *
     * @SWG\Parameter(
     *     name="data",
     *     in="body",
     *     @SWG\Schema(
     *              @SWG\Property(property="token", type="string"),
     *              @SWG\Property(property="password", type="string"),
     *              @SWG\Property(property="confirm_password", type="string")
     *          )
     * )
     *
     * @param Request                               $request
     * @param EventDispatcherInterface              $eventDispatcher
     * @param AuthenticationSuccessHandlerInterface $authenticationSuccessHandler
     *
     * @return Response
     */
    public function reset(
        Request $request,
        EventDispatcherInterface $eventDispatcher,
        AuthenticationSuccessHandlerInterface $authenticationSuccessHandler
    ) {
        $data = json_decode($request->getContent(), true);

        $passwordChangeConfirmEvent = new PasswordChangeConfirmEvent($request);

        $eventDispatcher->dispatch($passwordChangeConfirmEvent);

        if ($passwordChangeConfirmEvent->getResponseData()) {
            return $this->handleEventResponseData($passwordChangeConfirmEvent->getResponseData());
        }

        $user = $passwordChangeConfirmEvent->getUser();
        $passwordChangeConfirmValidEvent = new PasswordChangeConfirmValidEvent($user, $data['password']);
        $eventDispatcher->dispatch($passwordChangeConfirmValidEvent);

        if ($passwordChangeConfirmValidEvent->getResponseData()) {
            return $this->handleEventResponseData($passwordChangeConfirmValidEvent->getResponseData());
        }

        return $authenticationSuccessHandler->handleAuthenticationSuccess($user);
    }

    /**
     * @Rest\Post("/refresh_token")
     *
     * @SWG\Post(
     *     summary="Refresh token",
     *     tags={"Security"},
     *     @SWG\Response(
     *          response=200,
     *          description="New token has been issued",
     *          @SWG\Schema(
     *              @SWG\Property(property="token", type="string")
     *          )
     *     ),
     *     @SWG\Response(response=401, description="Unauthorized", @SWG\Schema(
     *          @SWG\Property(property="code", type="integer", default="401"),
     *          @SWG\Property(property="message", type="string", description="Authorization guard message"),
     *     )),
     *     @SWG\Response(response=403, description="Forbidden", @SWG\Schema(
     *           @SWG\Property(property="code", type="string", enum=ErrorCodes::FORBIDDEN_CODES),
     *           @SWG\Property(property="message", type="string"),
     *      )),
     * )
     *
     * @Security(name="Bearer")
     *
     * @return Response
     */
    public function refreshToken(AuthenticationSuccessHandlerInterface $authenticationSuccessHandler)
    {
        return $authenticationSuccessHandler->handleAuthenticationSuccess($this->getUser());
    }
}
