<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Controller;

use App\Entity\Player;
use App\Entity\User;
use App\Event\PlayerManagement\AddPlayerEvent;
use App\Event\PlayerManagement\AddPlayerValidEvent;
use App\Event\PlayerManagement\DeletePlayerEvent;
use App\Event\PlayerManagement\DeletePlayerValidEvent;
use App\Event\PlayerManagement\UpdatePlayerEvent;
use App\Event\PlayerManagement\UpdatePlayerValidEvent;
use App\Form\PlayerType;
use App\Service\PlayerManager;
use App\Validation\ErrorCodes;
use FOS\RestBundle\Context\Context;
use FOS\RestBundle\Controller\Annotations as Rest;
use Nelmio\ApiDocBundle\Annotation\Model;
use Nelmio\ApiDocBundle\Annotation\Security;
use Swagger\Annotations as SWG;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Contracts\EventDispatcher\EventDispatcherInterface;

/**
 * Class PlayerController.
 *
 * @method User getUser()
 */
class PlayerController extends AbstractDomainController
{
    /**
     * @Rest\Get("/player/")
     *
     * @SWG\Get(
     *     summary="List players",
     *     tags={"Player"},
     *     @SWG\Response(
     *          response=200,
     *          description="Player",
     *          @SWG\Schema(
     *              type="array",
     *              @Model(type=Player::class, groups={"list"})
     *          )
     *      ),
     *     @SWG\Response(response=400, description="Request errors", @SWG\Schema(
     *              @SWG\Property(property="code", type="string", enum=ErrorCodes::INVALID_CODES),
     *              @SWG\Property(property="errors", type="array", @SWG\Items(type="string")),
     *      )),
     *     @SWG\Response(response=409, description="Conflict errors", @SWG\Schema(
     *              @SWG\Property(property="code", type="string", enum=ErrorCodes::CONFLICT_CODES),
     *              @SWG\Property(property="errors", type="array", @SWG\Items(type="string")),
     *      )),
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
     * @param PlayerManager $playerManager
     *
     * @return Response
     */
    public function list(PlayerManager $playerManager): Response
    {
        $view = $this->view($playerManager->getPlayers($this->getUser()->getSystem()));

        $context = new Context();
        $context->setGroups(['list']);
        $view->setContext($context);

        return $this->handleView($view);
    }

    /**
     * @Rest\Post("/player/")
     *
     * @SWG\Post(
     *     summary="Create player",
     *     tags={"Player"},
     *     @SWG\Response(
     *          response=201,
     *          description="Created player details",
     *          @Model(type=Player::class)
     *     ),
     *     @SWG\Response(response=400, description="Request errors", @SWG\Schema(
     *              @SWG\Property(property="code", type="string", enum=ErrorCodes::INVALID_CODES),
     *              @SWG\Property(property="errors", type="array", @SWG\Items(type="string")),
     *              @SWG\Property(property="form", type="object")
     *      )),
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
     * @SWG\Parameter(
     *     name="data",
     *     in="body",
     *     description="Player creation parameters",
     *     @Model(type=PlayerType::class)
     * )
     *
     * @param Request                  $request
     * @param EventDispatcherInterface $eventDispatcher
     *
     * @return Response
     *
     * @Security(name="Bearer")
     */
    public function create(Request $request, EventDispatcherInterface $eventDispatcher): Response
    {
        $addEvent = new AddPlayerEvent($request, $this->getUser()->getSystem());
        $eventDispatcher->dispatch($addEvent);
        if ($addEvent->getResponseData()) {
            return $this->handleEventResponseData($addEvent->getResponseData());
        }

        $addValidEvent = new AddPlayerValidEvent($request, $this->getUser()->getSystem());
        $addValidEvent->setPlayer($addEvent->getPlayer());

        $eventDispatcher->dispatch($addValidEvent);
        if ($addValidEvent->getResponseData()) {
            return $this->handleEventResponseData($addValidEvent->getResponseData());
        }

        $view = $this->view($addValidEvent->getPlayer(), Response::HTTP_CREATED);

        $context = new Context();
        $context->setGroups(['details']);
        $view->setContext($context);

        return $this->handleView($view);
    }

    /**
     * @Rest\Get("/player/{id}")
     *
     * @SWG\Get(
     *     summary="Get player details",
     *     tags={"Player"},
     *     @SWG\Response(
     *          response=200,
     *          description="Player details",
     *          @Model(type=Player::class)
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
     *          @SWG\Property(property="code", type="integer", default="401"),
     *          @SWG\Property(property="message", type="string", description="Authorization guard message"),
     *     )),
     *     @SWG\Response(response=403, description="Forbidden", @SWG\Schema(
     *           @SWG\Property(property="code", type="string", enum=ErrorCodes::FORBIDDEN_CODES),
     *           @SWG\Property(property="message", type="string"),
     *      )),
     *     @SWG\Response(response=404, description="Resource not found"),
     * )
     *
     * @param int           $id
     * @param PlayerManager $playerManager
     *
     * @return Response
     *
     * @Security(name="Bearer")
     */
    public function show(int $id, PlayerManager $playerManager): Response
    {
        $player = $playerManager->getPlayer($id, $this->getUser()->getSystem());
        if (!$player) {
            return $this->handleView(
                $this->view(
                    ['message' => 'Player not found'],
                    Response::HTTP_NOT_FOUND
                )
            );
        }

        $view = $this->view($player);

        $context = new Context();
        $context->setGroups(['details']);
        $view->setContext($context);

        return $this->handleView($view);
    }

    /**
     * @Rest\Patch("/player/{id}")
     *
     * @SWG\Patch(
     *     summary="Update player",
     *     tags={"Player"},
     *     @SWG\Response(
     *          response=200,
     *          description="Updated player details",
     *          @Model(type=Player::class)
     *     ),
     *     @SWG\Response(response=400, description="Request errors", @SWG\Schema(
     *              @SWG\Property(property="code", type="string", enum=ErrorCodes::INVALID_CODES),
     *              @SWG\Property(property="errors", type="array", @SWG\Items(type="string")),
     *              @SWG\Property(property="form", type="object")
     *      )),
     *     @SWG\Response(response=401, description="Unauthorized", @SWG\Schema(
     *          @SWG\Property(property="code", type="integer", default="401"),
     *          @SWG\Property(property="message", type="string", description="Authorization guard message"),
     *     )),
     *     @SWG\Response(response=403, description="Forbidden", @SWG\Schema(
     *           @SWG\Property(property="code", type="string", enum=ErrorCodes::FORBIDDEN_CODES),
     *           @SWG\Property(property="message", type="string"),
     *      )),
     *     @SWG\Response(response=404, description="Resource not found"),
     * )
     *
     * @SWG\Parameter(
     *     name="data",
     *     in="body",
     *     description="Player creation parameters",
     *     @Model(type=PlayerType::class)
     * )
     *
     * @param int     $id
     * @param Request $request
     *
     * @Security(name="Bearer")
     *
     * @return Response
     */
    public function update(int $id, Request $request, EventDispatcherInterface $eventDispatcher): Response
    {
        $updateEvent = new UpdatePlayerEvent($request, $this->getUser()->getSystem());
        $updateEvent->setId($id);
        $eventDispatcher->dispatch($updateEvent);
        if ($updateEvent->getResponseData()) {
            return $this->handleEventResponseData($updateEvent->getResponseData());
        }

        $updateValidEvent = new UpdatePlayerValidEvent($request, $this->getUser()->getSystem());
        $updateValidEvent->setPlayer($updateEvent->getPlayer());

        $eventDispatcher->dispatch($updateValidEvent);
        if ($updateValidEvent->getResponseData()) {
            return $this->handleEventResponseData($updateValidEvent->getResponseData());
        }

        $view = $this->view($updateValidEvent->getPlayer(), Response::HTTP_OK);

        $context = new Context();
        $context->setGroups(['details']);
        $view->setContext($context);

        return $this->handleView($view);
    }

    /**
     * @Rest\Delete("/player/{id}")
     *
     * @SWG\Delete(
     *     summary="Delete player",
     *     tags={"Player"},
     *     @SWG\Response(
     *          response=200,
     *          description="Player deleted",
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
     *          @SWG\Property(property="code", type="integer", default="401"),
     *          @SWG\Property(property="message", type="string", description="Authorization guard message"),
     *     )),
     *     @SWG\Response(response=403, description="Forbidden", @SWG\Schema(
     *           @SWG\Property(property="code", type="string", enum=ErrorCodes::FORBIDDEN_CODES),
     *           @SWG\Property(property="message", type="string"),
     *      )),
     *     @SWG\Response(response=404, description="Resource not found"),
     * )
     *
     * @param int                      $id
     * @param Request                  $request
     * @param EventDispatcherInterface $eventDispatcher
     *
     * @return Response
     *
     * @Security(name="Bearer")
     */
    public function delete(int $id, Request $request, EventDispatcherInterface $eventDispatcher): Response
    {
        $deleteEvent = new DeletePlayerEvent($request, $this->getUser()->getSystem());
        $deleteEvent->setId($id);
        $eventDispatcher->dispatch($deleteEvent);
        if ($deleteEvent->getResponseData()) {
            return $this->handleEventResponseData($deleteEvent->getResponseData());
        }

        $deleteValidEvent = new DeletePlayerValidEvent($request, $this->getUser()->getSystem());
        $deleteValidEvent->setPlayer($deleteEvent->getPlayer());

        $eventDispatcher->dispatch($deleteValidEvent);
        if ($deleteValidEvent->getResponseData()) {
            $this->handleEventResponseData($deleteValidEvent->getResponseData());
        }

        $view = $this->view(['message' => 'Player deleted', Response::HTTP_OK]);

        $context = new Context();
        $context->setGroups(['details']);
        $view->setContext($context);

        return $this->handleView($view);
    }
}
